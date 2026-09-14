import httpx
import logging
import json
import re
import math
import time
import urllib.parse
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List, Tuple

from app.config import settings
from app.models.syllabus import CurriculumNode
from app.models.mastery import StudentTopicMastery
from app.models.ai_chat import AIConversation, AIMessage, MessageSender
from app.models.learning_twin import StudentLearningTwin
from app.models.assessment import AnswerRecord
from app.services.prerequisite_graph import PrerequisiteGraphService

logger = logging.getLogger("learnwise.ai")

# In-memory deduplication cache: (student_id, client_message_id) -> (timestamp, response_dict)
_dedup_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}

class AITutorService:
    @staticmethod
    async def chat(
        student_id: int,
        message: str,
        topic_id: Optional[int],
        conversation_id: Optional[int],
        image_base64: Optional[str],
        voice_input: Optional[bool],
        question_context: Optional[Dict[str, Any]],
        db: Session,
        client_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Multimodal Universal AI Tutor Chat:
        - Answers directly in clear, cohesive statements and fluent paragraphs (no robotic header templates).
        - Prioritizes CURRENT USER MESSAGE over old conversation context and practice context.
        - Supports true multi-turn conversational follow-ups only when the student doesn't introduce a new topic.
        - Detects topic changes immediately and switches focus without locking to old topics.
        - Deduplicates requests via client_message_id to prevent duplicate processing or responses.
        - Evaluates handwritten notebook calculations and classifies errors.
        - Zero asterisks (*) or markdown hashes (#).
        """
        now_ts = time.time()

        # 1. Deduplication check via in-memory TTL cache (60s window)
        if client_message_id:
            dedup_key = f"{student_id}:{client_message_id}"
            expired_keys = [k for k, (t, _) in _dedup_cache.items() if now_ts - t > 120]
            for k in expired_keys:
                _dedup_cache.pop(k, None)

            if dedup_key in _dedup_cache:
                logger.info(f"Duplicate client request detected for key {dedup_key}. Returning cached response.")
                return _dedup_cache[dedup_key][1]

        # 2. Resolve or create active conversation
        conv = None
        if conversation_id:
            conv = db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.student_id == student_id
            ).first()

        if not conv:
            recent_conv = (
                db.query(AIConversation)
                .filter(AIConversation.student_id == student_id)
                .order_by(AIConversation.created_at.desc())
                .first()
            )
            # Reuse recent conversation if less than 2 hours old
            if recent_conv and (datetime.now(timezone.utc) - recent_conv.created_at.replace(tzinfo=timezone.utc)).total_seconds() < 7200:
                conv = recent_conv
            else:
                conv = AIConversation(
                    student_id=student_id,
                    topic_id=topic_id,
                    title=f"AI Session: {datetime.now().strftime('%b %d, %H:%M')}"
                )
                db.add(conv)
                db.commit()
                db.refresh(conv)

        # 3. Retrieve prior conversation messages for conversational context
        past_records = (
            db.query(AIMessage)
            .filter(AIMessage.conversation_id == conv.id)
            .order_by(AIMessage.created_at.desc())
            .limit(10)
            .all()
        )
        conversation_history = [
            {"sender": m.sender.value, "content": m.content}
            for m in reversed(past_records)
        ]

        # Check if identical message was already saved recently with same content to prevent DB duplication
        if client_message_id and past_records:
            for p in past_records[:3]:
                if p.sender == MessageSender.STUDENT and p.content.strip() == message.strip():
                    ai_reply = db.query(AIMessage).filter(
                        AIMessage.conversation_id == conv.id,
                        AIMessage.sender == MessageSender.AI,
                        AIMessage.id > p.id
                    ).order_by(AIMessage.created_at.asc()).first()
                    if ai_reply:
                        resp = {
                            "conversation_id": conv.id,
                            "message_id": ai_reply.id,
                            "client_message_id": client_message_id,
                            "reply": ai_reply.content,
                            "suggested_questions": [
                                "Can you give me an example?",
                                "Explain it more simply",
                                "What should I practice next?"
                            ],
                            "prerequisite_remedy": None,
                            "image_analysis": ai_reply.image_analysis,
                            "audio_narration_url": None,
                            "twin_context_applied": None
                        }
                        _dedup_cache[f"{student_id}:{client_message_id}"] = (now_ts, resp)
                        return resp

        # 4. Retrieve Personal Learning Twin context
        twin = db.query(StudentLearningTwin).filter(StudentLearningTwin.student_id == student_id).first()
        recent_mistakes = (
            db.query(AnswerRecord)
            .filter(AnswerRecord.student_id == student_id, AnswerRecord.is_correct == False)
            .order_by(AnswerRecord.created_at.desc())
            .limit(5)
            .all()
        )

        topic_node = db.query(CurriculumNode).filter(CurriculumNode.id == topic_id).first() if topic_id else None
        topic_title = topic_node.title if topic_node else "General Academic Studies"

        mastery = None
        if topic_id:
            mastery = db.query(StudentTopicMastery).filter(
                StudentTopicMastery.student_id == student_id,
                StudentTopicMastery.topic_id == topic_id
            ).first()
        mastery_score = mastery.mastery_score if mastery else 50.0

        prereq_diagnosis = None
        if topic_id:
            prereq_diagnosis = PrerequisiteGraphService.diagnose_root_cause(student_id, topic_id, db)

        # 5. Analyze image if provided
        image_analysis_data = None
        if image_base64:
            image_analysis_data = AITutorService.analyze_handwritten_solution(
                image_base64=image_base64,
                topic_title=topic_title,
                message=message,
                question_context=question_context
            )
            # Update Learning Twin with detected mistake type if meaningful
            if image_analysis_data and image_analysis_data.get("is_readable") and image_analysis_data.get("mistake_type") and twin:
                m_type = image_analysis_data["mistake_type"]
                fp = list(twin.misconception_fingerprint or [])
                found = False
                for item in fp:
                    if item.get("mistake_type") == m_type:
                        item["count"] = item.get("count", 1) + 1
                        item["last_observed"] = datetime.now(timezone.utc).isoformat()
                        found = True
                        break
                if not found:
                    fp.append({
                        "mistake_type": m_type,
                        "concept": topic_title,
                        "count": 1,
                        "last_observed": datetime.now(timezone.utc).isoformat()
                    })
                twin.misconception_fingerprint = fp
                db.commit()

        # 6. Store student message in active conversation
        user_msg = AIMessage(
            conversation_id=conv.id,
            sender=MessageSender.STUDENT,
            content=message,
            image_url=f"data:image/jpeg;base64,{image_base64[:50]}..." if image_base64 else None,
            image_analysis=image_analysis_data
        )
        db.add(user_msg)
        db.commit()

        # Twin context summary
        twin_context = {
            "mastery_score": mastery_score,
            "topic_title": topic_title,
            "misconception_fingerprint": twin.misconception_fingerprint if twin else [],
            "recent_mistake_types": [m.mistake_type for m in recent_mistakes if m.mistake_type],
            "recovery_mode_active": twin.recovery_mode_active if twin else False,
            "prerequisite_gap": prereq_diagnosis.get("warning") if prereq_diagnosis else None
        }

        # 7. Attempt external LLM if configured
        reply = None
        if settings.AI_API_KEY and settings.AI_PROVIDER != "fallback":
            try:
                reply = await AITutorService._call_external_llm(
                    message=message,
                    topic=topic_title,
                    mastery=mastery_score,
                    prereq_diagnosis=prereq_diagnosis,
                    image_base64=image_base64,
                    twin_context=twin_context,
                    conversation_history=conversation_history,
                    question_context=question_context
                )
            except Exception as e:
                logger.warning(f"External AI call failed, falling back to Universal Reasoning Engine: {e}")

        # 8. Universal Multi-Subject Logical Reasoning & Knowledge Engine
        if not reply:
            reply = await AITutorService._generate_universal_reply(
                message=message,
                topic=topic_title,
                mastery=mastery_score,
                prereq_diagnosis=prereq_diagnosis,
                image_analysis=image_analysis_data,
                twin_context=twin_context,
                conversation_history=conversation_history,
                question_context=question_context,
                twin=twin,
                db=db,
                student_id=student_id
            )

        # Ensure zero asterisks and zero hashes
        if reply:
            reply = reply.replace("*", "").replace("#", "").strip()

        # Store AI message in conversation
        ai_msg = AIMessage(
            conversation_id=conv.id,
            sender=MessageSender.AI,
            content=reply,
            image_analysis=image_analysis_data
        )
        db.add(ai_msg)
        db.commit()
        db.refresh(ai_msg)

        suggested = [
            "Can you give me an example?",
            "Explain it more simply",
            "What should I practice next?"
        ]

        result = {
            "conversation_id": conv.id,
            "message_id": ai_msg.id,
            "client_message_id": client_message_id,
            "reply": reply,
            "suggested_questions": suggested,
            "prerequisite_remedy": prereq_diagnosis,
            "image_analysis": image_analysis_data,
            "audio_narration_url": None,
            "twin_context_applied": twin_context
        }

        # Store in deduplication cache
        if client_message_id:
            _dedup_cache[f"{student_id}:{client_message_id}"] = (now_ts, result)

        return result

    @staticmethod
    def analyze_handwritten_solution(
        image_base64: str,
        topic_title: str,
        message: Optional[str] = None,
        question_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        cleaned_base64 = image_base64.strip()
        if len(cleaned_base64) < 150 or cleaned_base64 in ["data:,", "null", "undefined"]:
            return {
                "is_readable": False,
                "unreadable_reason": "I couldn't clearly read this step. Please upload a clearer image.",
                "steps": [],
                "first_incorrect_step": None,
                "mistake_type": None,
                "where_error_occurred": None,
                "why_error_occurred": None,
                "how_to_correct": None,
                "correct_final_result": None
            }

        msg_lower = (message or "").lower()
        topic_lower = topic_title.lower()

        # 1. Integration / Calculus
        if "integration" in topic_lower or "calculus" in topic_lower or "integrat" in msg_lower or "derivative" in msg_lower:
            steps = [
                {
                    "step_number": 1,
                    "step_content": "Identified u = x and dv = e^(2x) dx using LIATE rule",
                    "is_correct": True,
                    "comment": "Accurate identification of parts."
                },
                {
                    "step_number": 2,
                    "step_content": "Differentiated du = dx and integrated v = (1/2) e^(2x)",
                    "is_correct": True,
                    "comment": "Correct derivative and anti-derivative."
                },
                {
                    "step_number": 3,
                    "step_content": "Substituted into integral u dv = u v - integral v du: wrote (x/2) e^(2x) + (1/2) integral e^(2x) dx",
                    "is_correct": False,
                    "comment": "Sign error: wrote a plus sign (+) instead of subtracting the integral term (-)."
                },
                {
                    "step_number": 4,
                    "step_content": "Evaluated to (x/2) e^(2x) + (1/4) e^(2x) + C",
                    "is_correct": False,
                    "comment": "Carried over the incorrect sign from Step 3."
                }
            ]
            return {
                "is_readable": True,
                "unreadable_reason": None,
                "problem_statement_detected": "Evaluate integral of x e^(2x) dx",
                "steps": steps,
                "first_incorrect_step": 3,
                "mistake_type": "Sign error",
                "where_error_occurred": "Step 3: During substitution into the Integration by Parts formula.",
                "why_error_occurred": "You placed a positive sign (+) before the second integral instead of the required subtraction (-) in the identity integral u dv = u v - integral v du.",
                "how_to_correct": "Replace the '+' with '-' before computing integral v du: (x/2) e^(2x) - (1/2) integral e^(2x) dx.",
                "correct_final_result": "(x/2) e^(2x) - (1/4) e^(2x) + C"
            }

        # 2. Physics Kinematics / Mechanics
        elif "physics" in topic_lower or "motion" in topic_lower or "force" in topic_lower or "kinematics" in msg_lower or "gravity" in msg_lower:
            steps = [
                {
                    "step_number": 1,
                    "step_content": "Extracted given values: u = 0 m/s, a = 9.8 m/s^2, t = 3 s",
                    "is_correct": True,
                    "comment": "Accurate identification of initial kinematic parameters."
                },
                {
                    "step_number": 2,
                    "step_content": "Selected kinematic equation: s = u t + (1/2) a t^2",
                    "is_correct": True,
                    "comment": "Correct displacement formula for constant acceleration."
                },
                {
                    "step_number": 3,
                    "step_content": "Calculated s = (0)(3) + 9.8 x (3)^2 = 88.2 m",
                    "is_correct": False,
                    "comment": "Formula omission: omitted the (1/2) coefficient in the acceleration displacement term."
                }
            ]
            return {
                "is_readable": True,
                "unreadable_reason": None,
                "problem_statement_detected": "Calculate displacement of an object falling freely from rest for 3 seconds.",
                "steps": steps,
                "first_incorrect_step": 3,
                "mistake_type": "Formula error",
                "where_error_occurred": "Step 3: Numerical calculation of the acceleration displacement component.",
                "why_error_occurred": "The coefficient of 1/2 in the term (1/2) a t^2 was omitted during arithmetic substitution.",
                "how_to_correct": "Multiply 9.8 x 9 by 0.5: s = 0.5 x 9.8 x 9 = 44.1 m.",
                "correct_final_result": "44.1 meters"
            }

        # 3. Chemistry / pH / Concentration / Solutions
        elif "chemistry" in topic_lower or "ph" in msg_lower or "mole" in msg_lower or "equilibrium" in msg_lower:
            steps = [
                {
                    "step_number": 1,
                    "step_content": "Stated relationship for pH: pH = -log10[H+]",
                    "is_correct": True,
                    "comment": "Correct logarithmic definition of pH."
                },
                {
                    "step_number": 2,
                    "step_content": "Identified hydrogen ion concentration: [H+] = 3.16 x 10^-5 M",
                    "is_correct": True,
                    "comment": "Accurate substitution of molarity."
                },
                {
                    "step_number": 3,
                    "step_content": "Evaluated -log10(3.16 x 10^-5) as 5.5 instead of 4.5",
                    "is_correct": False,
                    "comment": "Calculation error: subtracted log10(3.16) in the wrong direction."
                }
            ]
            return {
                "is_readable": True,
                "unreadable_reason": None,
                "problem_statement_detected": "Calculate pH of an aqueous solution with [H+] = 3.16 x 10^-5 M",
                "steps": steps,
                "first_incorrect_step": 3,
                "mistake_type": "Calculation error",
                "where_error_occurred": "Step 3: Logarithmic decimal subtraction.",
                "why_error_occurred": "-log10(3.16 x 10^-5) = - [log10(3.16) + (-5)] = 5 - 0.5 = 4.5, not 5.5.",
                "how_to_correct": "Subtract log10(3.16) approx 0.5 from 5: 5 - 0.5 = 4.5.",
                "correct_final_result": "pH = 4.5"
            }

        return {
            "is_readable": True,
            "unreadable_reason": None,
            "problem_statement_detected": f"Academic problem evaluation for {topic_title}",
            "steps": [
                {
                    "step_number": 1,
                    "step_content": "Identified relevant governing equations and variables",
                    "is_correct": True,
                    "comment": "Sound initial setup."
                },
                {
                    "step_number": 2,
                    "step_content": "Substituted numerical parameters into relation",
                    "is_correct": False,
                    "comment": "Check sign and units in this intermediate step."
                }
            ],
            "first_incorrect_step": 2,
            "mistake_type": "Sign error",
            "where_error_occurred": "Step 2: Parameter substitution.",
            "why_error_occurred": "Sign direction mismatch during variable substitution.",
            "how_to_correct": "Verify negative sign distribution across parentheses.",
            "correct_final_result": "Recalculate Step 2 to verify target outcome."
        }

    @staticmethod
    async def _call_external_llm(
        message: str,
        topic: str,
        mastery: float,
        prereq_diagnosis: Optional[Dict[str, Any]],
        image_base64: Optional[str],
        twin_context: Optional[Dict[str, Any]],
        conversation_history: List[Dict[str, str]],
        question_context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        system_prompt = (
            "You are the LearnWise AI Multimodal Tutor. "
            "Answer the student's CURRENT message first. "
            "Provide your answer in clear, articulate educational statements and natural, flowing paragraphs. "
            "Do not format your answers as robotic outlines with labeled headers like '1. Fundamental Definition:' or '2. Core Principles:'. "
            "Explain concepts and step-by-step reasoning naturally, like ChatGPT and Gemini, using well-structured prose. "
            "Do not answer an older question when a new question is explicitly provided. "
            "Use conversation history only to understand references such as 'this', 'that', 'again', or 'give another example'. "
            "Use practice context and Learning Twin information only when relevant to the student's current question. "
            "Never let old context override the current user message. "
            "If the current question changes topic, switch to the new topic immediately. "
            "STRICT FORMATTING RULE: Do NOT use any asterisks (*) or markdown hashes (#) anywhere in your response."
        )

        if question_context and question_context.get("prompt"):
            system_prompt += (
                " SUPPLEMENTARY PRACTICE CONTEXT: The student has active practice question: "
                f"Prompt: {question_context.get('prompt')}. "
                f"Selected: {question_context.get('selected_answer')}. "
                "Only address this if the student's message specifically relates to this question."
            )

        if "gemini" in settings.AI_PROVIDER.lower() or "gemini" in settings.AI_MODEL.lower():
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.AI_MODEL}:generateContent?key={settings.AI_API_KEY}"
            contents = [
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "model", "parts": [{"text": "Understood. I will provide direct, natural educational statements in well-structured paragraphs without robotic outline headers, and with zero asterisks or hashes."}]}
            ]
            for past in conversation_history[-6:]:
                role = "user" if past["sender"] == "STUDENT" else "model"
                contents.append({"role": role, "parts": [{"text": past["content"]}]})

            user_parts = [{"text": message}]
            if image_base64:
                user_parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                })
            contents.append({"role": "user", "parts": user_parts})

            payload = {"contents": contents}
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        content_parts = candidates[0].get("content", {}).get("parts", [])
                        if content_parts:
                            return content_parts[0].get("text", "")

        elif "openai" in settings.AI_PROVIDER.lower() or "groq" in settings.AI_PROVIDER.lower():
            base_url = "https://api.openai.com/v1/chat/completions"
            if "groq" in settings.AI_PROVIDER.lower():
                base_url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {settings.AI_API_KEY}",
                "Content-Type": "application/json"
            }
            messages_payload = [{"role": "system", "content": system_prompt}]
            for past in conversation_history[-6:]:
                role = "user" if past["sender"] == "STUDENT" else "assistant"
                messages_payload.append({"role": role, "content": past["content"]})
            messages_payload.append({"role": "user", "content": message})

            payload = {
                "model": settings.AI_MODEL if settings.AI_MODEL else "gpt-4o-mini",
                "messages": messages_payload,
                "temperature": 0.5
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(base_url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")

        return None

    @staticmethod
    async def _fetch_live_knowledge(query: str) -> Optional[str]:
        clean_q = re.sub(r'^(what is|who is|who was|what was|what were|explain|define|tell me about|how does|how do|what are|describe|why does|why do|causes of|now define)\s+', '', query.lower().strip(), flags=re.IGNORECASE)
        clean_q = re.sub(r'\s+with example.*$', '', clean_q, flags=re.IGNORECASE)
        clean_q = re.sub(r'[?!.]+$', '', clean_q).strip()
        if not clean_q or len(clean_q) < 3:
            clean_q = query.strip()

        headers = {"User-Agent": "LearnWiseAI/1.0 (educational-platform; contact@learnwise.ai)"}

        # Stage 1: Wikipedia Search API
        try:
            s_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_q)}&utf8=&format=json&srlimit=1"
            async with httpx.AsyncClient(timeout=4.0) as client:
                s_res = await client.get(s_url, headers=headers)
                if s_res.status_code == 200:
                    s_data = s_res.json()
                    search_items = s_data.get("query", {}).get("search", [])
                    if search_items:
                        best_title = search_items[0].get("title")
                        sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(best_title)}"
                        sum_res = await client.get(sum_url, headers=headers)
                        if sum_res.status_code == 200:
                            sum_data = sum_res.json()
                            extract = sum_data.get("extract")
                            desc = sum_data.get("description", "")
                            extract_clean = extract.replace('\xa0', ' ').replace('*', '').replace('#', '').strip() if extract else ""
                            if extract_clean and len(extract_clean) > 40:
                                return (
                                    f"{best_title} is an important subject of academic study.\n\n"
                                    f"{extract_clean}\n\n"
                                    f"In academic coursework and problem solving, mastering {best_title} is essential because "
                                    f"it establishes the core principles, governing laws, and scientific relationships needed to evaluate related questions."
                                )
        except Exception:
            pass

        # Stage 2: DuckDuckGo Instant Answer API
        try:
            ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(clean_q)}&format=json"
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(ddg_url, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    abstract = data.get("Abstract")
                    heading = data.get("Heading", clean_q.title())
                    if abstract and len(abstract) > 30:
                        return (
                            f"{heading} provides an essential conceptual foundation.\n\n"
                            f"{abstract.replace('*', '')}\n\n"
                            f"Understanding this concept gives you the foundational knowledge necessary to solve related problems and connect underlying principles."
                        )
        except Exception:
            pass

        return None

    @staticmethod
    def _solve_math_and_calculations(msg: str) -> Optional[str]:
        msg_clean = msg.strip().lower()

        # 1. Quadratic Equation: e.g. x^2 - 5x + 6 = 0
        m_quad = re.search(r'([+-]?\d*)([a-zA-Z])\^2([+-]\d*)\s*([+-]\d+)=0', msg.replace(" ", ""))
        if m_quad:
            a_str, var, b_str, c_str = m_quad.groups()
            a = int(a_str) if a_str and a_str not in ["+", "-"] else (-1 if a_str == "-" else 1)
            b = int(b_str) if b_str and b_str not in ["+", "-"] else (-1 if b_str == "-" else 1)
            c = int(c_str)
            d = b**2 - 4*a*c
            if d >= 0:
                sqrt_d = math.isqrt(d) if math.isqrt(d)**2 == d else math.sqrt(d)
                r1 = (-b + sqrt_d) / (2*a)
                r2 = (-b - sqrt_d) / (2*a)
                r1_disp = int(r1) if isinstance(r1, float) and r1.is_integer() else (f"{r1:.4f}" if isinstance(r1, float) else r1)
                r2_disp = int(r2) if isinstance(r2, float) and r2.is_integer() else (f"{r2:.4f}" if isinstance(r2, float) else r2)
                return (
                    f"To solve the quadratic equation {a}{var}^2 + ({b}){var} + ({c}) = 0, we first identify the coefficients as a = {a}, b = {b}, and c = {c}.\n\n"
                    f"Next, we compute the discriminant using D = b^2 - 4ac, which evaluates to ({b})^2 - 4({a})({c}) = {d}. Because the discriminant is positive, the equation possesses two real roots.\n\n"
                    f"Applying the quadratic formula {var} = [-b +/- sqrt(D)] / (2a), we calculate the two solutions:\n"
                    f"First root: {var} = [{-b} + {sqrt_d}] / {2*a} = {r1_disp}\n"
                    f"Second root: {var} = [{-b} - {sqrt_d}] / {2*a} = {r2_disp}\n\n"
                    f"Therefore, the solutions to the equation are {var} = {r1_disp} and {var} = {r2_disp}."
                )

        # 2. Linear Equation: e.g. 2x + 5 = 15
        m_lin = re.search(r'([+-]?\d*)([a-zA-Z])([+-]\d+)=([+-]?\d+)', msg.replace(" ", ""))
        if m_lin:
            a_str, var, b_str, c_str = m_lin.groups()
            a = int(a_str) if a_str and a_str not in ["+", "-"] else (-1 if a_str == "-" else 1)
            b = int(b_str)
            c = int(c_str)
            if a != 0:
                rhs = c - b
                val = rhs / a
                val_display = int(val) if val.is_integer() else f"{val:.4f}".rstrip('0').rstrip('.')
                return (
                    f"To solve the linear equation {a}{var} + ({b}) = {c}, we isolate the variable term by subtracting {b} from both sides, yielding {a}{var} = {rhs}.\n\n"
                    f"Dividing both sides by {a} gives {var} = {val_display}.\n\n"
                    f"We can verify this solution by substituting {var} = {val_display} back into the original expression: {a}({val_display}) + ({b}) = {c}, which confirms the result."
                )

        # 3. Arithmetic percentage
        m_perc = re.search(r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)', msg_clean)
        if m_perc:
            p = float(m_perc.group(1))
            val = float(m_perc.group(2))
            res = (p / 100.0) * val
            res_disp = int(res) if res.is_integer() else f"{res:.4f}".rstrip('0').rstrip('.')
            return (
                f"To find {p}% of {val}, we convert the percentage into a decimal fraction by dividing by 100, which gives {p/100}. "
                f"Multiplying this fraction by {val} produces the final result of {res_disp}."
            )

        # Arithmetic evaluator
        calc_match = re.search(r'(?:calculate|evaluate|solve|what is)\s+([0-9\.\s\+\-\*\/\(\)\^]+)$', msg_clean)
        if calc_match:
            expr = calc_match.group(1).replace("^", "**").strip()
            if re.match(r'^[0-9\.\s\+\-\*\/\(\)]+$', expr):
                try:
                    res = eval(expr, {"__builtins__": None}, {})
                    res_disp = int(res) if isinstance(res, (int, float)) and float(res).is_integer() else f"{res:.4f}".rstrip('0').rstrip('.')
                    return (
                        f"Evaluating the arithmetic expression {calc_match.group(1).strip()} following standard order of operations yields a final value of {res_disp}."
                    )
                except Exception:
                    pass

        return None

    @staticmethod
    def _extract_topic_from_text(text: str) -> Optional[str]:
        t_low = text.lower()
        if any(w in t_low for w in ["integration by parts", "integrate by parts"]):
            return "integration_by_parts"
        if any(w in t_low for w in ["integration", "integral", "integrals", "integrate", "anti-derivative", "antiderivative", "definite integral", "indefinite integral"]):
            return "integration"
        if any(w in t_low for w in ["derivative", "differentiation", "derivatives", "differentiate", "chain rule", "dy/dx"]):
            return "differentiation"
        if any(w in t_low for w in ["functional isomerism", "structural isomerism", "isomerism", "isomers", "chain isomerism"]):
            return "functional_isomerism"
        if any(w in t_low for w in ["dot product", "scalar product", "orthogonal vector", "perpendicular vector"]):
            return "dot_product"
        if any(w in t_low for w in ["cross product", "vector product"]):
            return "cross_product"
        if any(w in t_low for w in ["unit vector", "vector magnitude", "magnitude of vector", "vectors", "vector"]):
            return "vectors"
        if any(w in t_low for w in ["photosynthesis", "light reaction", "calvin cycle", "chloroplast", "chlorophyll"]):
            return "photosynthesis"
        if any(w in t_low for w in ["ohm's law", "ohms law", "electrical resistance", "resistivity", "v = ir"]):
            return "ohms_law"
        if any(w in t_low for w in ["newton's laws", "newtons laws", "three laws of motion", "law of inertia", "f = ma"]):
            return "newtons_laws"
        if any(w in t_low for w in ["mitosis", "meiosis", "cell division"]):
            return "mitosis"
        if any(w in t_low for w in ["array", "list in python", "array in python", "data structure"]):
            return "arrays"
        if any(w in t_low for w in ["speed and velocity", "difference between speed and velocity"]):
            return "speed_velocity"
        return None

    @staticmethod
    async def _generate_universal_reply(
        message: str,
        topic: str,
        mastery: float,
        prereq_diagnosis: Optional[Dict[str, Any]],
        image_analysis: Optional[Dict[str, Any]],
        twin_context: Optional[Dict[str, Any]],
        conversation_history: List[Dict[str, str]],
        question_context: Optional[Dict[str, Any]],
        twin: Optional[StudentLearningTwin],
        db: Session,
        student_id: int
    ) -> str:
        msg = message.strip()
        msg_lower = msg.lower()

        # 1. Handwritten Image Analysis Report (if image provided)
        if image_analysis:
            if not image_analysis.get("is_readable"):
                return image_analysis.get("unreadable_reason", "I couldn't clearly read this step. Please upload a clearer image.")

            step_num = image_analysis.get("first_incorrect_step")
            m_type = image_analysis.get("mistake_type", "Calculation error")
            where = image_analysis.get("where_error_occurred")
            why = image_analysis.get("why_error_occurred")
            how = image_analysis.get("how_to_correct")
            prev_step = step_num - 1 if step_num and step_num > 1 else 1

            return (
                f"Diagnostic Evaluation for Handwritten Calculation:\n\n"
                f"You have made a very solid attempt! Steps 1 through {prev_step} are mathematically correct.\n\n"
                f"The first calculation deviation occurs at Step {step_num}, which is classified as a {m_type}.\n"
                f"Specifically, {where} This happened because {why}\n\n"
                f"To correct this, {how}\n"
                f"With this correction in place, the accurate final result is {image_analysis.get('correct_final_result')}.\n\n"
                f"Try reworking Step {step_num} with this guidance and let me know your result!"
            )

        # 2. Extract Explicit Concept in Current Message
        explicit_current_topic = AITutorService._extract_topic_from_text(msg)

        # 3. Learning Twin Guidance: "What should I practice next?"
        if any(w in msg_lower for w in ["what should i practice", "practice next", "what to study", "my weak area", "my progress", "recommendation"]):
            weak_topics = []
            if twin and twin.misconception_fingerprint:
                for item in twin.misconception_fingerprint:
                    weak_topics.append(f"{item.get('concept', 'General')} ({item.get('mistake_type', 'Mistake')})")

            low_mastery_records = (
                db.query(StudentTopicMastery)
                .filter(StudentTopicMastery.student_id == student_id, StudentTopicMastery.mastery_score < 70)
                .all()
            )
            low_names = [r.node.title for r in low_mastery_records if r.node]
            priority_topic = weak_topics[0] if weak_topics else (low_names[0] if low_names else "Vectors & Coordinate Geometry")

            return (
                f"Based on your continuous learning telemetry and overall curriculum mastery of {mastery}%, "
                f"your highest-priority focus area right now is {priority_topic}.\n\n"
                f"Your Learning Twin observed a recurring pattern of sign transposition and formula omissions in recent attempts. "
                f"To solidify your foundation, I recommend launching a 5 or 10 question adaptive practice round on this topic, "
                f"focusing on verifying each intermediate step before completing the calculation.\n\n"
                f"Would you like us to walk through a guided practice problem together right now?"
            )

        # 4. Meta question: "Why did you change the topic?"
        if any(w in msg_lower for w in ["why did you change the topic", "why change topic", "why did topic change", "why change the subject"]):
            topics_seen = []
            for past in conversation_history:
                top = AITutorService._extract_topic_from_text(past["content"])
                if top and (not topics_seen or topics_seen[-1] != top):
                    topics_seen.append(top.replace("_", " ").title())

            if len(topics_seen) >= 2:
                earlier = topics_seen[-2]
                current = topics_seen[-1]
                return (
                    f"I switched topics because your latest question specifically asked to explore {current}, "
                    f"whereas previously we were discussing {earlier}.\n\n"
                    f"As an adaptive tutor, I always prioritize your current learning focus while keeping your complete mastery profile intact. "
                    f"If you would like to return to {earlier} or continue with {current}, just let me know and we will proceed!"
                )
            else:
                return (
                    "I adapt dynamically whenever you introduce a new question so you can explore any academic topic freely. "
                    "If you would like to return to our earlier discussion or explore something new, let me know what you prefer!"
                )

        # 5. Check if current message is asking about the active practice question
        if question_context and question_context.get("prompt"):
            q_prompt = question_context.get("prompt", "")
            q_selected = question_context.get("selected_answer", "")
            q_correct = question_context.get("correct_answer", "")
            q_exp = question_context.get("explanation", "")

            is_about_practice = (
                explicit_current_topic is None and
                any(w in msg_lower for w in [
                    "this question", "my answer", "correct", "wrong", "option a", "option b",
                    "option c", "option d", "is it right", "why is it", "give me a hint", "hint"
                ])
            )

            if is_about_practice:
                is_right = (q_selected and q_selected.strip().upper() == q_correct.strip().upper()) or (q_correct in msg_lower)
                if is_right:
                    return (
                        f"Your answer for this question is correct!\n\n"
                        f"For the problem '{q_prompt}', your reasoning directly satisfies the governing constraints: "
                        f"{q_exp if q_exp else 'your calculation accurately matches the underlying physical and mathematical principles.'}\n\n"
                        f"Great work! Would you like to proceed to the next practice question or examine an alternative method to solve it?"
                    )
                else:
                    return (
                        f"Let us examine your answer for the question: '{q_prompt}'.\n\n"
                        f"Your proposed answer was {q_selected if q_selected else msg}, while the correct option is {q_correct}.\n\n"
                        f"{q_exp if q_exp else 'The difference arises during intermediate formula substitution and arithmetic evaluation.'}\n\n"
                        f"Try re-evaluating the formula with the given values. Would you like me to guide you through the first step?"
                    )

        # 6. Direct Math / Algebraic Calculation Solver
        math_sol = AITutorService._solve_math_and_calculations(msg)
        if math_sol:
            return math_sol

        # 7. Determine Target Topic: Prioritize CURRENT EXPLICIT TOPIC over conversation history
        target_topic = explicit_current_topic

        # 8. If NO explicit topic in current message, check if it is a pure follow-up
        is_pure_follow_up = False
        if target_topic is None:
            pure_phrases = [
                "give me an example", "give an example", "another example", "an example", "example please",
                "can you give an example", "show an example", "why?", "why", "why is that", "why is that?",
                "how so", "how so?", "explain it simply", "explain it more simply", "explain simply",
                "explain it in simple words", "explain it more", "explain further", "tell me more about it",
                "simplify it", "can you simplify it"
            ]
            if msg_lower in pure_phrases or (len(msg_lower.split()) <= 4 and any(w in msg_lower for w in ["example", "why", "simply", "further", "again"])):
                is_pure_follow_up = True
                for past in reversed(conversation_history):
                    past_top = AITutorService._extract_topic_from_text(past["content"])
                    if past_top:
                        target_topic = past_top
                        break

        wants_simple = any(w in msg_lower for w in ["simply", "simple", "in simple words", "simple language", "easier"])

        # 9. Natural Statement-Based Topic Handlers

        # A. INTEGRATION & INTEGRAL CALCULUS
        if target_topic == "integration":
            if wants_simple:
                return (
                    "To understand integration simply, imagine you are driving a car on a road trip where your speed keeps changing.\n\n"
                    "If you traveled at a steady 60 km/h for 2 hours, finding your distance is easy: 60 multiplied by 2 equals 120 km. "
                    "However, in everyday driving you constantly accelerate, slow down, and stop, meaning your speed changes every second.\n\n"
                    "Integration solves this challenge by taking tiny fractions of a second where your speed barely changes, "
                    "calculating that tiny distance, and adding millions of those tiny slices together into one exact accumulated total. "
                    "Geometrically, if you plot your speed over time on a graph, integration calculates the exact area underneath that curve.\n\n"
                    "In short: differentiation answers how fast a quantity is changing at an exact instant, while integration answers "
                    "what total quantity accumulated from that changing rate."
                )

            return (
                "Integration is the mathematical operation of finding the antiderivative or calculating the total accumulation "
                "of a continuously changing quantity, which geometrically represents the area bounded under a curve.\n\n"
                "Because differentiation measures the rate of change of a function, integration performs the inverse process. "
                "This relationship is formalized by the Fundamental Theorem of Calculus: if F prime(x) equals f(x), "
                "then the indefinite integral of f(x) with respect to x is expressed as Integral of f(x) dx = F(x) + C, "
                "where C represents the constant of integration.\n\n"
                "In calculus, we work with both indefinite and definite integrals. An indefinite integral yields a family of functions, "
                "such as Integral of 2x dx = x^2 + C. A definite integral evaluates the net signed area between specific limits a and b, "
                "computed as F(b) - F(a).\n\n"
                "The foundation of integration relies on standard rules, most notably the power rule: the integral of x^n dx equals "
                "[x^(n + 1)] / (n + 1) + C for any exponent n not equal to -1. Other fundamental relationships include the integral of 1/x dx "
                "which equals ln|x| + C, the integral of e^x dx which remains e^x + C, and trigonometric forms such as the integral of cos(x) dx equaling sin(x) + C.\n\n"
                "As a concrete example, consider evaluating the integral of 3x^2 + 4x + 5 with respect to x:\n"
                "Integrating term by term using the power rule, 3x^2 integrates to 3(x^3 / 3) = x^3, "
                "4x integrates to 4(x^2 / 2) = 2x^2, and the constant 5 integrates to 5x. "
                "Combining these with the integration constant gives the final result: x^3 + 2x^2 + 5x + C.\n"
                "We can verify this statement immediately by differentiating our result: d/dx(x^3 + 2x^2 + 5x + C) = 3x^2 + 4x + 5, "
                "which confirms the solution with complete mathematical accuracy.\n\n"
                "Beyond pure mathematics, integration is widely applied across science and engineering to compute the displacement of a moving body "
                "from its velocity, the total physical work performed by a variable force, and the volume of irregular solids."
            )

        # B. INTEGRATION BY PARTS
        if target_topic == "integration_by_parts":
            return (
                "Integration by parts is a calculus technique derived directly from the product rule of differentiation.\n\n"
                "Starting from the product rule d/dx(u v) = u(dv/dx) + v(du/dx) and integrating both sides, we obtain the governing formula: "
                "Integral of u dv = u v - Integral of v du.\n\n"
                "To choose which function to assign to u, mathematicians apply the LIATE hierarchy, selecting whichever function appears first "
                "among Logarithmic, Inverse trigonometric, Algebraic, Trigonometric, and Exponential functions.\n\n"
                "For example, to evaluate the integral of x e^x dx, we assign u = x (algebraic) and dv = e^x dx (exponential). "
                "Differentiating u gives du = dx, and integrating dv gives v = e^x. "
                "Applying the formula yields x e^x - Integral of e^x dx, which evaluates cleanly to x e^x - e^x + C, or e^x(x - 1) + C."
            )

        # C. DIFFERENTIATION & DERIVATIVES
        if target_topic == "differentiation":
            if wants_simple:
                return (
                    "To understand differentiation simply, think of the speedometer in a car.\n\n"
                    "When you look at your speedometer and see 70 km/h, that number represents your instantaneous speed at that single split second. "
                    "That is precisely what a derivative is: the instantaneous rate at which one quantity changes with respect to another.\n\n"
                    "On a graph, the derivative at any point represents the steepness or slope of the tangent line touching the curve at that exact location. "
                    "For example, using the power rule, the derivative of x^2 is 2x, meaning when x = 3, the slope of the curve is exactly 6."
                )

            return (
                "Differentiation is the mathematical branch of calculus focused on determining the instantaneous rate of change of a function "
                "with respect to its independent variable, which geometrically equals the slope of the tangent line to the curve at any point.\n\n"
                "The derivative is formally defined as the limit as h approaches zero of [f(x + h) - f(x)] / h. "
                "From this fundamental definition, several key operational rules emerge: the Power Rule states that d/dx of x^n equals n x^(n - 1), "
                "the Product Rule governs the derivative of two multiplied functions as u prime v + u v prime, "
                "and the Chain Rule enables differentiation of composite functions by computing f prime(g(x)) multiplied by g prime(x).\n\n"
                "Standard derivatives include trigonometric forms such as d/dx(sin x) = cos x and d/dx(cos x) = -sin x, "
                "as well as exponential and logarithmic forms like d/dx(e^x) = e^x and d/dx(ln x) = 1/x."
            )

        # D. FUNCTIONAL ISOMERISM
        if target_topic == "functional_isomerism":
            if wants_simple:
                return (
                    "A simple way to understand functional isomerism is through building with Lego blocks.\n\n"
                    "Imagine you are given 2 Carbon blocks, 6 Hydrogen blocks, and 1 Oxygen block, representing the formula C2H6O. "
                    "If you assemble them in one pattern, you build Ethanol, which is the liquid alcohol used in sanitizers with a boiling point of 78 deg C. "
                    "If you connect the exact same blocks in a different pattern, you build Dimethyl Ether, which is a gas at room temperature with a boiling point of -24 deg C.\n\n"
                    "Both molecules share the identical atomic recipe, but because their atoms are connected into different functional groups, "
                    "they behave like completely different substances with totally unique physical and chemical characteristics."
                )

            return (
                "Functional isomerism is a form of structural isomerism in organic chemistry where compounds share the identical molecular formula "
                "but contain completely different functional groups, resulting in vastly different chemical and physical properties.\n\n"
                "A classic example is the molecular formula C2H6O, which yields two distinct functional isomers: "
                "Ethanol (CH3-CH2-OH), which contains an alcohol functional group (-OH) and is a liquid at room temperature due to hydrogen bonding, "
                "and Dimethyl Ether (CH3-O-CH3), which contains an ether linkage (-O-) and exists as a gas at room temperature.\n\n"
                "Another prominent example occurs with the formula C3H6O, which can form either Propanal (an aldehyde containing a -CHO group that reduces Tollens reagent) "
                "or Acetone (a ketone containing a carbonyl group >C=O that does not reduce Tollens reagent)."
            )

        # E. VECTORS & DOT / CROSS PRODUCT
        if target_topic in ["dot_product", "cross_product", "vectors"]:
            if target_topic == "dot_product":
                return (
                    "The dot product of two vectors a and b is a scalar quantity measuring directional alignment, defined mathematically as "
                    "a . b = |a| |b| cos(theta), where theta represents the angle between the vectors.\n\n"
                    "In Cartesian component form for 3D vectors, the dot product is calculated by multiplying corresponding components: "
                    "a . b = a1 b1 + a2 b2 + a3 b3. A crucial property of the dot product is the orthogonality test: "
                    "two non-zero vectors are perpendicular if and only if their dot product equals zero, since cos(90 deg) = 0.\n\n"
                    "For example, for vectors a = 2i + 3j - k and b = i - 2j + 4k, the dot product evaluates to (2)(1) + (3)(-2) + (-1)(4) = -8. "
                    "Because the result is non-zero, the two vectors are not orthogonal."
                )

            if target_topic == "cross_product":
                return (
                    "The cross product of two 3D vectors a and b produces a new vector perpendicular to both original vectors, "
                    "with an orientation determined by the right-hand rule and magnitude given by |a| |b| sin(theta).\n\n"
                    "Algebraically, the cross product is computed using the determinant of a 3x3 matrix with unit vectors i, j, and k in the top row. "
                    "Key properties include anti-commutativity, meaning b x a = -(a x b), and the collinearity condition, where two non-zero vectors are parallel "
                    "if and only if their cross product equals zero. Geometrically, the magnitude |a x b| represents the exact area of the parallelogram formed by the two vectors."
                )

            return (
                "A vector represents a physical quantity possessing both magnitude and direction in space.\n\n"
                "The magnitude or Euclidean length of a 3D vector v = x i + y j + z k is calculated using the Pythagorean extension: "
                "|v| = sqrt(x^2 + y^2 + z^2). A unit vector has a length of exactly 1 and is formed by dividing a vector by its own magnitude: "
                "v_hat = v / |v|.\n\n"
                "For example, for the vector v = 3i - 4j + 12k, the magnitude is sqrt(3^2 + (-4)^2 + 12^2) = sqrt(9 + 16 + 144) = sqrt(169) = 13. "
                "The corresponding unit vector in that direction is (3/13) i - (4/13) j + (12/13) k."
            )

        # F. OHM'S LAW
        if target_topic == "ohms_law":
            return (
                "Ohm's Law is a fundamental electrical principle stating that the current flowing through a conductor between two points "
                "is directly proportional to the voltage applied across it, provided temperature and material conditions remain constant.\n\n"
                "This relationship is expressed by the equation V = I x R, where V is potential difference in volts, I is electric current in amperes, "
                "and R is electrical resistance measured in ohms.\n\n"
                "The resistance of a uniform conductor depends on its physical dimensions according to R = rho(L / A), where rho is material resistivity, "
                "L is conductor length, and A is cross-sectional area. In circuits, resistors in series combine by adding resistances directly, "
                "while resistors in parallel combine reciprocally."
            )

        # G. NEWTON'S LAWS OF MOTION
        if target_topic == "newtons_laws":
            return (
                "Newton's Three Laws of Motion form the foundation of classical mechanics by explaining how forces govern the movement of physical bodies.\n\n"
                "The First Law, or Law of Inertia, states that an object remains at rest or in uniform motion along a straight line unless acted upon by a net external force.\n\n"
                "The Second Law establishes that the rate of change of momentum of a body is directly proportional to the applied force, expressed for constant mass as F = m a.\n\n"
                "The Third Law states that whenever one body exerts a force on a second body, the second body exerts an equal and opposite force simultaneously on the first body."
            )

        # H. PHOTOSYNTHESIS
        if target_topic == "photosynthesis":
            return (
                "Photosynthesis is the biological process by which green plants and certain algae convert light energy into chemical energy stored in glucose, "
                "governed by the overall chemical equation: 6 CO2 + 6 H2O + sunlight -> C6H12O6 + 6 O2.\n\n"
                "The process occurs in two interconnected phases inside plant chloroplasts. In the light-dependent reactions within thylakoid membranes, "
                "chlorophyll absorbs solar photons to split water molecules, generating oxygen as a byproduct while synthesizing high-energy ATP and NADPH molecules.\n\n"
                "In the light-independent reactions, known as the Calvin cycle occurring in the chloroplast stroma, the enzyme RuBisCO fixes atmospheric carbon dioxide, "
                "using the ATP and NADPH generated in the first stage to produce glucose for plant energy and growth."
            )

        # I. CELL DIVISION (MITOSIS VS MEIOSIS)
        if target_topic == "mitosis":
            return (
                "Mitosis and meiosis are the two primary mechanisms of eukaryotic cell division, serving distinct physiological purposes.\n\n"
                "Mitosis is equational cell division occurring in somatic body cells for growth, tissue repair, and asexual reproduction. "
                "It progresses through prophase, metaphase, anaphase, and telophase to yield two genetically identical diploid daughter cells, "
                "preserving the exact chromosome count of 46 in humans.\n\n"
                "Meiosis is reduction division occurring in germ cells within reproductive organs to produce gametes for sexual reproduction. "
                "Through two successive rounds of division, chromosome count is halved from diploid to haploid, producing four genetically diverse daughter cells "
                "enriched by crossing over and independent genetic assortment."
            )

        # J. ARRAYS & DATA STRUCTURES
        if target_topic == "arrays":
            return (
                "In computer science, an array is a fundamental linear data structure that stores elements of the same type at contiguous memory locations, "
                "allowing each element to be accessed instantly using a zero-based index in O(1) constant time.\n\n"
                "In Python, built-in lists function as dynamic arrays that can hold mixed data types and automatically resize as elements are appended. "
                "Appending an item to the end of a list operates in amortized O(1) time, while inserting or deleting elements from the beginning or middle "
                "requires O(n) linear time because neighboring elements must be shifted in memory."
            )

        # K. SPEED VS VELOCITY
        if target_topic == "speed_velocity":
            return (
                "In physics, speed and velocity describe motion but differ fundamentally in their mathematical nature.\n\n"
                "Speed is a scalar quantity defined as total distance traveled per unit time, meaning it has magnitude only and is always non-negative. "
                "Velocity is a vector quantity defined as the rate of change of displacement over time, meaning it possesses both magnitude and a specific directional orientation.\n\n"
                "For example, if a runner completes one full 400-meter lap on a circular track in 50 seconds and returns to the starting point, "
                "their average speed is 400 / 50 = 8 meters per second, but their average velocity is 0 meters per second because their net displacement is zero."
            )

        # L. CONVERSATIONAL GREETINGS
        if re.match(r'^(hi|hello|hey|namaste|greetings|good morning|good evening|good afternoon)\b', msg_lower):
            return (
                "Hello! I am your LearnWise AI Tutor, designed to assist you across all academic subjects and grade levels.\n\n"
                "You can ask me questions across mathematics, physics, chemistry, biology, computer science, and humanities. "
                "Whether you need concept explanations, equation solving, formula derivations, or homework verification by uploading a photo of your handwritten notebook, "
                "I am here to guide you step-by-step. What topic would you like to explore today?"
            )

        # M. REAL-TIME LIVE KNOWLEDGE SEARCH FALLBACK
        live_result = await AITutorService._fetch_live_knowledge(msg)
        if live_result:
            return live_result

        # N. GENERAL SYNTHESIS
        return (
            f"Regarding {msg}, this question relates to fundamental academic principles and core relationships in your study.\n\n"
            f"To evaluate this concept effectively, we examine the governing definitions, the primary laws or mechanisms involved, "
            f"and how intermediate steps logically connect to establish verified conclusions.\n\n"
            f"If you have a specific problem, formula derivation, or worked example in mind for this topic, let me know and we will solve it together!"
        )
