import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.question import Question, DifficultyLevel
from app.models.syllabus import CurriculumNode
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.assessment import AnswerRecord
from app.models.learning_twin import StudentLearningTwin
from app.models.risk import RiskPrediction, RiskLevel
from app.services.mastery_engine import MasteryEngine
from app.services.prerequisite_graph import PrerequisiteGraphService
from app.services.risk_engine import RiskEngine

logger = logging.getLogger("learnwise.smart_practice")

class SmartPracticeEngine:
    MISTAKE_TYPES = [
        "CONCEPT_MISUNDERSTANDING",
        "FORMULA_MISTAKE",
        "CALCULATION_MISTAKE",
        "SIGN_MISTAKE",
        "UNIT_CONVERSION_MISTAKE",
        "QUESTION_INTERPRETATION_MISTAKE",
        "CARELESS_MISTAKE",
        "PREREQUISITE_KNOWLEDGE_GAP"
    ]

    @staticmethod
    def get_or_create_twin(student_id: int, db: Session) -> StudentLearningTwin:
        twin = db.query(StudentLearningTwin).filter(StudentLearningTwin.student_id == student_id).first()
        if not twin:
            twin = StudentLearningTwin(
                student_id=student_id,
                misconception_fingerprint=[],
                recovery_mode_active=False,
                recovery_mode_step=0,
                struggle_signal_detected=False,
                struggle_signal_reason=None,
                learning_velocity=1.0,
                timeline_events=[],
                decayed_topics=[],
                consecutive_topic_successes=0,
                consecutive_topic_failures=0
            )
            db.add(twin)
            db.commit()
            db.refresh(twin)
        return twin

    @staticmethod
    def classify_mistake(
        question: Question,
        selected_answer: str,
        time_taken_seconds: int,
        student_id: int,
        db: Session
    ) -> Tuple[str, str, str]:
        """
        Classifies the student's mistake into one of the 8 canonical archetypes,
        returns (mistake_type, concept_involved, how_to_avoid).
        """
        prompt_lower = (question.prompt or "").lower()
        selected_upper = selected_answer.strip().upper()
        correct_upper = question.correct_answer.strip().upper()

        # Extract selected option text if available
        selected_text = ""
        correct_text = ""
        for opt in (question.options or []):
            if isinstance(opt, dict):
                if str(opt.get("id", "")).upper() == selected_upper:
                    selected_text = str(opt.get("text", "")).lower()
                if str(opt.get("id", "")).upper() == correct_upper:
                    correct_text = str(opt.get("text", "")).lower()

        # 1. Careless mistake check: answered way too fast (< 4 seconds)
        if time_taken_seconds < 4:
            return (
                "CARELESS_MISTAKE",
                "Pacing and Thorough Reading",
                "Take at least 15–20 seconds to read the question and verify all options before selecting an answer."
            )

        # 2. Sign mistake detection
        if (
            "-" in selected_text and "+" in correct_text or
            "+" in selected_text and "-" in correct_text or
            "negative" in selected_text or "positive" in selected_text or
            "sign" in (question.explanation or "").lower()
        ):
            return (
                "SIGN_MISTAKE",
                "Algebraic / Directional Signs",
                "Track the negative signs across each substitution. Enclose negative factors in parentheses: e.g., (-x)."
            )

        # 3. Unit conversion mistake detection
        unit_keywords = ["cm", "m/s", "km/h", "joule", "kelvin", "celsius", "mol", "radians", "degrees", "unit"]
        if any(u in prompt_lower or u in selected_text or u in correct_text for u in unit_keywords):
            if any(term in prompt_lower for term in ["convert", "standard unit", "si unit", "per hour", "per second"]):
                return (
                    "UNIT_CONVERSION_MISTAKE",
                    "Dimensional Analysis and SI Units",
                    "Always standardize all quantities to SI units (kg, m, s, K) before substituting into the formula."
                )

        # 4. Prerequisite Knowledge Gap check
        prereq_diag = PrerequisiteGraphService.diagnose_root_cause(student_id, question.topic_id, db)
        if prereq_diag and prereq_diag.get("root_cause_topic"):
            root = prereq_diag["root_cause_topic"]
            return (
                "PREREQUISITE_KNOWLEDGE_GAP",
                f"Prerequisite: {root.get('title', 'Foundational concept')}",
                f"Review foundational concept '{root.get('title')}' first. Mastery here depends directly on that foundation."
            )

        # 5. Formula mistake detection
        formula_keywords = ["formula", "theorem", "law", "derivative", "integral", "identity", "equation"]
        if any(k in prompt_lower or k in (question.explanation or "").lower() for k in formula_keywords):
            return (
                "FORMULA_MISTAKE",
                "Governing Formula Application",
                "Write down the general formula explicitly before inserting numerical values to prevent incorrect term placement."
            )

        # 6. Question interpretation mistake
        if "not" in prompt_lower or "incorrect" in prompt_lower or "except" in prompt_lower:
            return (
                "QUESTION_INTERPRETATION_MISTAKE",
                "Question Constraint Identification",
                "Highlight constraint keywords like 'NOT', 'EXCEPT', or 'ALWAYS' before evaluating choices."
            )

        # 7. Calculation mistake vs Concept misunderstanding
        if any(char.isdigit() for char in selected_text) and any(char.isdigit() for char in correct_text):
            return (
                "CALCULATION_MISTAKE",
                "Arithmetic / Algebraic Simplification",
                "Verify your intermediate arithmetic steps on scratch paper before performing the final reduction."
            )

        # Default: Concept misunderstanding
        return (
            "CONCEPT_MISUNDERSTANDING",
            question.title or "Core Conceptual Principle",
            "Review the core underlying definition and verify the conditions under which this principle holds true."
        )

    @staticmethod
    def generate_dual_explanations(
        question: Question,
        selected_answer: str,
        is_correct: bool,
        mistake_type: Optional[str] = None,
        how_to_avoid: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Returns (brief_explanation, full_explanation).
        Both right and wrong answers get full pedagogical step-by-step clarity.
        """
        raw_explanation = question.explanation or "Apply fundamental principles to solve step-by-step."
        
        # Determine human labels for options
        correct_text = question.correct_answer
        selected_text = selected_answer
        for opt in (question.options or []):
            if isinstance(opt, dict):
                if str(opt.get("id", "")).upper() == question.correct_answer.strip().upper():
                    correct_text = f"Option {question.correct_answer}: {opt.get('text', '')}"
                if str(opt.get("id", "")).upper() == selected_answer.strip().upper():
                    selected_text = f"Option {selected_answer}: {opt.get('text', '')}"

        def clean_s(s: str) -> str:
            if not s:
                return ""
            return s.replace("*", "").replace("#", "").strip()

        raw_clean = clean_s(raw_explanation)

        if is_correct:
            first_sentence = raw_clean.split('.')[0] if '.' in raw_clean else raw_clean
            brief = f"Correct! Option {question.correct_answer} is the valid answer. {first_sentence}."
            full = (
                f"Verification & Conceptual Walkthrough\n\n"
                f"Your Answer: {selected_text} (Correct)\n"
                f"Core Principle: {raw_clean}\n\n"
                f"Step-by-Step Breakdown:\n"
                f"1. Identified the governing relationship from the question prompt.\n"
                f"2. Substituted known quantities accurately into the core equation.\n"
                f"3. Executed simplification cleanly, resulting in Option {question.correct_answer}.\n\n"
                f"Pro Tip for Mastery: Keep noting the constraints in the question so you can replicate this rapid accuracy under timed exam conditions!"
            )
        else:
            first_sentence = raw_clean.split('.')[0] if '.' in raw_clean else raw_clean
            brief = (
                f"Incorrect. You chose Option {selected_answer}, but the correct answer is Option {question.correct_answer}. "
                f"Core reason: {first_sentence}."
            )
            full = (
                f"Detailed Step-by-Step Solution\n\n"
                f"Your Choice: {selected_text}\n"
                f"Correct Answer: {correct_text}\n"
                f"Mistake Archetype Detected: {mistake_type or 'CONCEPT_MISUNDERSTANDING'}\n\n"
                f"Complete Mathematical & Conceptual Derivation:\n"
                f"1. Governing Concept: {raw_clean}\n"
                f"2. Where the Deviation Occurred: Choosing Option {selected_answer} commonly occurs when terms are inverted, signs transposed, or prerequisite steps skipped.\n"
                f"3. Correct Calculation: Carrying out the formal derivation confirms Option {question.correct_answer} satisfies all constraints.\n\n"
                f"How to Avoid This in the Future:\n"
                f"{clean_s(how_to_avoid) or 'Review the core definition and double-check your sign conventions before confirming your submission.'}"
            )

        return clean_s(brief), clean_s(full)

    @staticmethod
    def process_answer_submission(
        student_id: int,
        question_id: int,
        selected_answer: str,
        time_taken_seconds: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Processes answer submission through the full Personal Learning Twin pipeline:
        - Evaluates correctness
        - Classifies mistake archetype
        - Builds dual explanations
        - Updates student mastery with recency decay
        - Enforces same-topic retention (<70% or consecutive failures)
        - Updates misconception fingerprint
        - Updates recovery mode & struggle signals
        """
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found")

        is_correct = (selected_answer.strip().upper() == question.correct_answer.strip().upper())
        
        # Classify mistake & advice
        mistake_type = None
        concept_involved = None
        how_to_avoid = None
        if not is_correct:
            mistake_type, concept_involved, how_to_avoid = SmartPracticeEngine.classify_mistake(
                question, selected_answer, time_taken_seconds, student_id, db
            )

        # Dual explanations
        explanation_brief, explanation_full = SmartPracticeEngine.generate_dual_explanations(
            question, selected_answer, is_correct, mistake_type, how_to_avoid
        )

        # Persist AnswerRecord with twin fields
        answer_rec = AnswerRecord(
            student_id=student_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken_seconds=time_taken_seconds,
            mistake_type=mistake_type,
            explanation_brief=explanation_brief,
            explanation_full=explanation_full,
            concept_involved=concept_involved,
            how_to_avoid=how_to_avoid
        )
        db.add(answer_rec)

        # Log LearningActivity
        topic_node = db.query(CurriculumNode).filter(CurriculumNode.id == question.topic_id).first()
        topic_title = topic_node.title if topic_node else "Topic Practice"
        activity = LearningActivity(
            student_id=student_id,
            activity_type="PRACTICE",
            title=f"Practice: {question.title or topic_title}",
            details={
                "topic_id": question.topic_id,
                "topic_title": topic_title,
                "correct": is_correct,
                "mistake_type": mistake_type,
                "points": question.points if is_correct else 0
            },
            score=100.0 if is_correct else 0.0,
            duration_seconds=time_taken_seconds
        )
        db.add(activity)
        db.commit()

        # Update Mastery via MasteryEngine
        updated_mastery = MasteryEngine.calculate_topic_mastery(student_id, question.topic_id, db)
        current_mastery_score = updated_mastery.mastery_score

        # Check Prerequisite Root Cause
        root_cause_info = None
        if not is_correct:
            root_cause_info = PrerequisiteGraphService.diagnose_root_cause(student_id, question.topic_id, db)

        # Update Personal Learning Twin State
        twin = SmartPracticeEngine.get_or_create_twin(student_id, db)
        
        # Track same-topic counters
        if twin.last_active_topic_id != question.topic_id:
            twin.last_active_topic_id = question.topic_id
            twin.consecutive_topic_successes = 1 if is_correct else 0
            twin.consecutive_topic_failures = 0 if is_correct else 1
        else:
            if is_correct:
                twin.consecutive_topic_successes += 1
                twin.consecutive_topic_failures = 0
            else:
                twin.consecutive_topic_failures += 1
                twin.consecutive_topic_successes = 0

        # Enforce same-topic practice rule:
        # If mastery < 70% OR student has had consecutive failures, MUST stay on topic!
        # Only advance if mastery >= 70% and consecutive_topic_successes >= 2.
        stay_on_topic = True
        stay_reason = ""
        next_topic_id = None

        if current_mastery_score < 70.0:
            stay_on_topic = True
            stay_reason = f"Current mastery on '{topic_title}' is {current_mastery_score}% (< 70%). Reinforcing this topic until consistent mastery is achieved."
        elif twin.consecutive_topic_successes < 2:
            stay_on_topic = True
            stay_reason = f"Mastery is {current_mastery_score}%, but requires 2 consecutive successful answers to confirm stable understanding (Current: {twin.consecutive_topic_successes}/2)."
        else:
            stay_on_topic = False
            stay_reason = f"Excellent! You've achieved {current_mastery_score}% mastery with {twin.consecutive_topic_successes} consecutive correct answers. Ready to advance."
            # Find next topic in curriculum
            next_topic = db.query(CurriculumNode).filter(
                CurriculumNode.parent_id == topic_node.parent_id,
                CurriculumNode.id > topic_node.id
            ).order_by(CurriculumNode.id.asc()).first()
            if next_topic:
                next_topic_id = next_topic.id

        # Update Misconception Fingerprint
        misconception_alert = None
        fingerprint = list(twin.misconception_fingerprint or [])
        if mistake_type:
            # Find existing entry or create new
            found = False
            for item in fingerprint:
                if item.get("mistake_type") == mistake_type:
                    item["count"] = item.get("count", 0) + 1
                    item["last_detected"] = datetime.now(timezone.utc).isoformat()
                    if topic_title not in item.get("topics", []):
                        item.setdefault("topics", []).append(topic_title)
                    found = True
                    if item["count"] >= 2:
                        misconception_alert = (
                            f"Misconception Alert: You have exhibited {item['count']} repeated '{mistake_type.replace('_', ' ').title()}' "
                            f"instances across recent practice. {how_to_avoid}"
                        )
                    break
            if not found:
                fingerprint.append({
                    "mistake_type": mistake_type,
                    "count": 1,
                    "topics": [topic_title],
                    "last_detected": datetime.now(timezone.utc).isoformat(),
                    "remedy_advice": how_to_avoid or "Review foundational rules and verify each step carefully."
                })
        twin.misconception_fingerprint = fingerprint

        # Learning Recovery Mode Triggering
        recovery_triggered = False
        if twin.consecutive_topic_failures >= 3 or (current_mastery_score < 35.0 and twin.consecutive_topic_failures >= 2):
            twin.recovery_mode_active = True
            twin.recovery_mode_step = 1
            twin.recovery_mode_topic_id = question.topic_id
            twin.struggle_signal_detected = True
            twin.struggle_signal_reason = f"Frequent consecutive incorrect attempts on {topic_title} (Mastery: {current_mastery_score}%)."
            recovery_triggered = True
        elif is_correct and twin.recovery_mode_active:
            # Step forward through recovery
            if twin.recovery_mode_step < 7:
                twin.recovery_mode_step += 1
            else:
                twin.recovery_mode_active = False
                twin.recovery_mode_step = 0
                twin.struggle_signal_detected = False
                twin.struggle_signal_reason = None

        # Record timeline event if milestone reached
        timeline = list(twin.timeline_events or [])
        total_answers = db.query(AnswerRecord).filter(AnswerRecord.student_id == student_id).count()
        if total_answers % 5 == 0:
            now_str = datetime.now(timezone.utc).strftime("Week %U, %Y")
            timeline.append({
                "week_or_date": now_str,
                "summary": f"Completed {total_answers} practice items. {topic_title} mastery at {current_mastery_score}%.",
                "status": "MASTERED" if current_mastery_score >= 80 else ("IMPROVING" if current_mastery_score >= 60 else "STRUGGLING"),
                "mastery_avg": current_mastery_score,
                "questions_attempted": total_answers,
                "mistakes_made": db.query(AnswerRecord).filter(AnswerRecord.student_id == student_id, AnswerRecord.is_correct == False).count(),
                "key_achievement": f"{'Mastered' if current_mastery_score >= 70 else 'Practiced'} {topic_title}"
            })
            twin.timeline_events = timeline[-10:] # Keep latest 10 milestones

        db.commit()
        db.refresh(twin)

        # Trigger background risk update
        try:
            RiskEngine.calculate_student_risk(student_id, db)
        except Exception as e:
            logger.warning(f"Error recalculating risk: {e}")

        return {
            "question_id": question_id,
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation or "",
            "explanation_brief": explanation_brief,
            "explanation_full": explanation_full,
            "mistake_type": mistake_type,
            "concept_involved": concept_involved,
            "how_to_avoid": how_to_avoid,
            "prerequisite_hint": question.prerequisite_hint,
            "updated_mastery_score": current_mastery_score,
            "updated_mastery_status": updated_mastery.status.value,
            "root_cause_warning": root_cause_info.get("warning") if root_cause_info else None,
            "recommended_remedy": root_cause_info.get("remedy") if root_cause_info else None,
            "stay_on_topic": stay_on_topic,
            "stay_on_topic_reason": stay_reason,
            "consecutive_successes": twin.consecutive_topic_successes,
            "next_recommended_topic_id": next_topic_id,
            "recovery_mode_triggered": recovery_triggered,
            "misconception_alert": misconception_alert
        }

    @staticmethod
    def get_risk_adjusted_questions(
        student_id: int,
        topic_id: Optional[int],
        subject_id: Optional[int],
        num_questions: int,
        db: Session
    ) -> List[Question]:
        """
        Dynamically steers question selection and difficulty based on Student Risk:
        - HIGH Risk -> EASY questions or foundational questions
        - MEDIUM Risk -> MEDIUM questions with scaffolding
        - LOW Risk -> HARD / Application questions
        Prevents serving recently solved questions.
        """
        # Determine student risk
        risk_record = db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).first()
        risk_level = risk_record.risk_level if risk_record else RiskLevel.MEDIUM

        # Desired difficulty order based on risk
        if risk_level == RiskLevel.HIGH:
            difficulty_priority = [DifficultyLevel.EASY, DifficultyLevel.MEDIUM, DifficultyLevel.HARD]
        elif risk_level == RiskLevel.LOW:
            difficulty_priority = [DifficultyLevel.HARD, DifficultyLevel.MEDIUM, DifficultyLevel.EASY]
        else:
            difficulty_priority = [DifficultyLevel.MEDIUM, DifficultyLevel.EASY, DifficultyLevel.HARD]

        # Previously answered questions by student
        answered_ids = [
            r[0] for r in db.query(AnswerRecord.question_id).filter(
                AnswerRecord.student_id == student_id,
                AnswerRecord.is_correct == True
            ).all()
        ]

        query = db.query(Question)

        if topic_id:
            query = query.filter(Question.topic_id == topic_id)
        elif subject_id:
            # Find all topics under subject
            topic_ids = [
                node.id for node in db.query(CurriculumNode).filter(
                    (CurriculumNode.parent_id == subject_id) | (CurriculumNode.id == subject_id)
                ).all()
            ]
            query = query.filter(Question.topic_id.in_(topic_ids))

        all_candidates = query.all()
        if not all_candidates:
            # Fallback: any questions
            all_candidates = db.query(Question).limit(20).all()

        # Sort candidates: prefer priority difficulty and unattempted
        def sort_key(q: Question):
            diff_score = difficulty_priority.index(q.difficulty) if q.difficulty in difficulty_priority else 99
            already_done = 1 if q.id in answered_ids else 0
            return (already_done, diff_score, q.id)

        sorted_candidates = sorted(all_candidates, key=sort_key)
        return sorted_candidates[:num_questions]

    @staticmethod
    def detect_knowledge_decay(student_id: int, db: Session) -> List[Dict[str, Any]]:
        """
        Detects knowledge decay:
        When a previously strong topic (mastery >= 70%) has not been practiced
        or estimated retention has decayed below 60%.
        """
        masteries = db.query(StudentTopicMastery).filter(
            StudentTopicMastery.student_id == student_id,
            StudentTopicMastery.total_attempts > 0
        ).all()

        decayed = []
        now = datetime.now(timezone.utc)

        for m in masteries:
            last_attempt = m.last_attempt_at or m.created_at or now
            if last_attempt.tzinfo is None:
                last_attempt = last_attempt.replace(tzinfo=timezone.utc)

            days_elapsed = max(0, (now - last_attempt).days)
            
            # Retention half-life formula: R = M * e^(-0.05 * t)
            decay_rate = 0.05
            estimated_retention = m.mastery_score * (2.71828 ** (-decay_rate * days_elapsed))
            estimated_retention = max(20.0, round(estimated_retention, 1))

            # If it was once >= 65% but has decayed or hasn't been touched in >= 7 days
            if (m.mastery_score >= 65.0 and estimated_retention < 60.0) or (m.mastery_score >= 70.0 and days_elapsed >= 7):
                topic = db.query(CurriculumNode).filter(CurriculumNode.id == m.topic_id).first()
                parent = db.query(CurriculumNode).filter(CurriculumNode.id == topic.parent_id).first() if topic else None
                decayed.append({
                    "topic_id": m.topic_id,
                    "topic_name": topic.title if topic else "Topic",
                    "subject": parent.title if parent else "Science/Math",
                    "highest_mastery": m.mastery_score,
                    "current_estimated_mastery": estimated_retention,
                    "days_since_last_practice": days_elapsed,
                    "memory_decay_pct": round(max(0.0, m.mastery_score - estimated_retention), 1),
                    "needs_review": True
                })

        return decayed

    @staticmethod
    def get_full_twin_profile(student_id: int, db: Session) -> Dict[str, Any]:
        """
        Assembles the complete Personal Learning Twin profile for student or teacher:
        - Real overall mastery and risk level
        - Misconception fingerprint
        - Prerequisite gaps
        - Recovery Mode status
        - Struggle Signal status
        - Decayed topics
        - Timeline milestones
        - Next Best Action
        - What-If simulations
        """
        twin = SmartPracticeEngine.get_or_create_twin(student_id, db)
        
        # Calculate real overall mastery
        masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id == student_id).all()
        if masteries:
            overall_mastery = round(sum(m.mastery_score for m in masteries) / len(masteries), 1)
        else:
            overall_mastery = 0.0

        # Calculate real answers & accuracy
        all_answers = db.query(AnswerRecord).filter(AnswerRecord.student_id == student_id).all()
        total_answers = len(all_answers)
        correct_answers = sum(1 for a in all_answers if a.is_correct)
        accuracy_rate = round((correct_answers / total_answers * 100.0), 1) if total_answers > 0 else 0.0

        # Student risk
        risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).first()
        risk_level = risk.risk_level.value if risk else "MEDIUM"
        risk_score = risk.risk_score if risk else 50.0

        # Current focus topic
        current_focus = None
        if twin.last_active_topic_id:
            curr_node = db.query(CurriculumNode).filter(CurriculumNode.id == twin.last_active_topic_id).first()
            if curr_node:
                curr_mastery = next((m.mastery_score for m in masteries if m.topic_id == curr_node.id), 0.0)
                current_focus = {
                    "topic_id": curr_node.id,
                    "title": curr_node.title,
                    "code": curr_node.code,
                    "mastery": curr_mastery,
                    "consecutive_successes": twin.consecutive_topic_successes,
                    "consecutive_failures": twin.consecutive_topic_failures
                }

        # Decayed topics
        decayed = SmartPracticeEngine.detect_knowledge_decay(student_id, db)

        # Misconception Fingerprint
        fingerprint = []
        raw_fingerprint = twin.misconception_fingerprint or []
        total_mistakes = sum(item.get("count", 0) for item in raw_fingerprint)
        for item in raw_fingerprint:
            cnt = item.get("count", 0)
            pct = round((cnt / total_mistakes * 100.0), 1) if total_mistakes > 0 else 0.0
            fingerprint.append({
                "mistake_type": item.get("mistake_type", "CONCEPT_MISUNDERSTANDING"),
                "count": cnt,
                "frequency_pct": pct,
                "topics": item.get("topics", []),
                "last_detected": item.get("last_detected"),
                "remedy_advice": item.get("remedy_advice", "Review definitions and step-by-step logic.")
            })

        # Prerequisite gaps
        prereq_gaps = []
        for m in masteries:
            if m.mastery_score < 50.0:
                diag = PrerequisiteGraphService.diagnose_root_cause(student_id, m.topic_id, db)
                if diag and diag.get("root_cause_topic"):
                    topic_node = db.query(CurriculumNode).filter(CurriculumNode.id == m.topic_id).first()
                    parent_node = db.query(CurriculumNode).filter(CurriculumNode.id == topic_node.parent_id).first() if topic_node else None
                    prereq_gaps.append({
                        "topic_id": m.topic_id,
                        "topic_name": topic_node.title if topic_node else "Topic",
                        "subject": parent_node.title if parent_node else "Curriculum",
                        "root_prerequisite_id": diag["root_cause_topic"]["topic_id"],
                        "root_prerequisite_name": diag["root_cause_topic"]["title"],
                        "gap_severity": "CRITICAL" if m.mastery_score < 30.0 else "MODERATE",
                        "suggested_action": diag.get("remedy", "Review prerequisite foundations first.")
                    })

        # Recovery mode status
        rec_topic = db.query(CurriculumNode).filter(CurriculumNode.id == twin.recovery_mode_topic_id).first() if twin.recovery_mode_topic_id else None
        step_names = {
            0: "Inactive",
            1: "Diagnose Difficulty",
            2: "Intuitive Explanation",
            3: "Simple Worked Example",
            4: "Guided Micro-Question",
            5: "Easy Confidence Practice",
            6: "Medium Practice",
            7: "Final Reassessment"
        }
        recovery_status = {
            "active": twin.recovery_mode_active,
            "step": twin.recovery_mode_step,
            "step_name": step_names.get(twin.recovery_mode_step, "Active Recovery"),
            "topic_id": twin.recovery_mode_topic_id,
            "topic_name": rec_topic.title if rec_topic else None,
            "subject": "Mathematics / Science",
            "guidance": (
                "Work through this step carefully. Once you complete the guided exercise correctly, you will progress to the next step."
                if twin.recovery_mode_active else "All learning parameters operating normally."
            )
        }

        # Struggle signal status
        struggle_status = {
            "detected": twin.struggle_signal_detected,
            "reason": twin.struggle_signal_reason,
            "intervention_recommended": (
                f"Schedule 1-on-1 scaffolding on {rec_topic.title if rec_topic else 'current topic'} or assign targeted prerequisite exercises."
                if twin.struggle_signal_detected else None
            )
        }

        # Timeline milestones
        timeline = twin.timeline_events or []
        if not timeline and total_answers > 0:
            timeline = [{
                "week_or_date": datetime.now(timezone.utc).strftime("Week %U, %Y"),
                "summary": f"Completed initial diagnostic practice of {total_answers} questions.",
                "status": "IMPROVING" if overall_mastery >= 50 else "STRUGGLING",
                "mastery_avg": overall_mastery,
                "questions_attempted": total_answers,
                "mistakes_made": total_answers - correct_answers,
                "key_achievement": "Started Personal Learning Twin journey"
            }]

        # Next Best Action
        next_action = SmartPracticeEngine._determine_next_best_action(
            twin, current_focus, prereq_gaps, decayed, overall_mastery, db
        )

        # What-If Simulations
        what_if = SmartPracticeEngine._generate_what_if_simulations(overall_mastery, risk_level, current_focus, fingerprint)

        from app.models.user import User
        user = db.query(User).filter(User.id == student_id).first()
        student_name = user.full_name if user else f"Student #{student_id}"

        return {
            "student_id": student_id,
            "student_name": student_name,
            "overall_mastery": overall_mastery,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "learning_velocity": twin.learning_velocity or 1.0,
            "active_streak_days": 1 if total_answers > 0 else 0,
            "total_questions_answered": total_answers,
            "accuracy_rate": accuracy_rate,
            "current_focus_topic": current_focus,
            "misconception_fingerprint": fingerprint,
            "prerequisite_gaps": prereq_gaps,
            "recovery_mode": recovery_status,
            "struggle_signal": struggle_status,
            "decayed_topics": decayed,
            "timeline": timeline,
            "next_best_action": next_action,
            "what_if_simulations": what_if
        }

    @staticmethod
    def _determine_next_best_action(
        twin: StudentLearningTwin,
        current_focus: Optional[Dict[str, Any]],
        prereq_gaps: List[Dict[str, Any]],
        decayed: List[Dict[str, Any]],
        overall_mastery: float,
        db: Session
    ) -> Dict[str, Any]:
        """
        Computes the single highest-leverage next pedagogical action.
        """
        # Priority 1: Recovery Mode active
        if twin.recovery_mode_active and twin.recovery_mode_topic_id:
            topic = db.query(CurriculumNode).filter(CurriculumNode.id == twin.recovery_mode_topic_id).first()
            name = topic.title if topic else "Current Topic"
            return {
                "action_type": "RECOVERY_STEP",
                "title": f"Step {twin.recovery_mode_step}: Recovery on {name}",
                "description": f"You are currently in Recovery Mode on {name}. Complete this step to rebuild conceptual stability.",
                "topic_id": twin.recovery_mode_topic_id,
                "topic_name": name,
                "difficulty": "EASY",
                "cta_label": "Resume Recovery Step",
                "cta_url": f"/student/practice?topic_id={twin.recovery_mode_topic_id}&difficulty=EASY"
            }

        # Priority 2: Critical Prerequisite Gap
        if prereq_gaps:
            critical_gap = prereq_gaps[0]
            return {
                "action_type": "REVIEW_PREREQUISITE",
                "title": f"Reinforce Prerequisite: {critical_gap['root_prerequisite_name']}",
                "description": f"Your struggle in '{critical_gap['topic_name']}' is linked to '{critical_gap['root_prerequisite_name']}'. Reviewing this will unlock faster progress.",
                "topic_id": critical_gap["root_prerequisite_id"],
                "topic_name": critical_gap["root_prerequisite_name"],
                "difficulty": "EASY",
                "cta_label": "Practice Prerequisite",
                "cta_url": f"/student/practice?topic_id={critical_gap['root_prerequisite_id']}&difficulty=EASY"
            }

        # Priority 3: Retain on Current Topic if < 70%
        if current_focus and current_focus["mastery"] < 70.0:
            return {
                "action_type": "PRACTICE_SAME_TOPIC",
                "title": f"Reinforce: {current_focus['title']}",
                "description": f"Current mastery is {current_focus['mastery']}%. Complete targeted practice to reach the 70% threshold.",
                "topic_id": current_focus["topic_id"],
                "topic_name": current_focus["title"],
                "difficulty": "MEDIUM",
                "cta_label": "Continue Topic Practice",
                "cta_url": f"/student/practice?topic_id={current_focus['topic_id']}&difficulty=MEDIUM"
            }

        # Priority 4: Knowledge Decay Review
        if decayed:
            d = decayed[0]
            return {
                "action_type": "REASSESSMENT",
                "title": f"Review Decayed Topic: {d['topic_name']}",
                "description": f"Memory retention has decayed from {d['highest_mastery']}% to {d['current_estimated_mastery']}%. A 5-minute refresher will restore peak retention.",
                "topic_id": d["topic_id"],
                "topic_name": d["topic_name"],
                "difficulty": "MEDIUM",
                "cta_label": "Refresh Memory",
                "cta_url": f"/student/practice?topic_id={d['topic_id']}&difficulty=MEDIUM"
            }

        # Priority 5: Advance to Next Topic
        # Find next available topic
        next_topic = db.query(CurriculumNode).filter(
            CurriculumNode.type == "TOPIC"
        ).first()
        topic_id = next_topic.id if next_topic else None
        topic_name = next_topic.title if next_topic else "Next Topic"

        return {
            "action_type": "ADVANCE_TOPIC",
            "title": f"Start Next Topic: {topic_name}",
            "description": "Your foundations are solid! Advance to the next section in your curriculum.",
            "topic_id": topic_id,
            "topic_name": topic_name,
            "difficulty": "MEDIUM",
            "cta_label": "Start Practice",
            "cta_url": f"/student/practice?topic_id={topic_id}" if topic_id else "/student/practice"
        }

    @staticmethod
    def _generate_what_if_simulations(
        overall_mastery: float,
        risk_level: str,
        current_focus: Optional[Dict[str, Any]],
        fingerprint: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generates predictive simulation projections for student motivation.
        """
        focus_title = current_focus.get("title", "Current Topic") if current_focus else "Weak Topic"
        
        sims = [
            {
                "scenario": f"Complete 20 mins targeted practice on {focus_title}",
                "projected_mastery_gain": +15.0,
                "projected_new_mastery": min(100.0, round(overall_mastery + 15.0, 1)),
                "projected_risk_reduction": "LOW" if risk_level != "LOW" else "MINIMAL",
                "recommended_time_minutes": 20
            },
            {
                "scenario": "Eliminate top recurring mistake in Misconception Fingerprint",
                "projected_mastery_gain": +22.5,
                "projected_new_mastery": min(100.0, round(overall_mastery + 22.5, 1)),
                "projected_risk_reduction": "LOW",
                "recommended_time_minutes": 35
            },
            {
                "scenario": "Daily 10-minute streak for 5 consecutive days",
                "projected_mastery_gain": +30.0,
                "projected_new_mastery": min(100.0, round(overall_mastery + 30.0, 1)),
                "projected_risk_reduction": "LOW",
                "recommended_time_minutes": 50
            }
        ]
        return sims
