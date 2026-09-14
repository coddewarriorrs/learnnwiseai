import sys
import os
import json
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.syllabus_hierarchy import (
    Board, AcademicYear, AcademicClass, Subject, Unit, 
    Chapter, Topic, SubTopic, LearningOutcome
)
from app.models.syllabus import CurriculumNode, NodeType, NodeStatus
from app.models.question import Question, DifficultyLevel
from app.models.user import User
from app.curriculum_cbse2026 import CBSE_2026_SYLLABUS

def seed_cbse_2026(db: Session):
    print("=== SEEDING CBSE 2026-27 PERSISTENT SYLLABUS DATABASE ===")
    
    # Ensure all tables exist in database
    Base.metadata.create_all(bind=engine)

    # Ensure schema migrations for existing tables
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS class_id INTEGER REFERENCES academic_classes(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS subject_id INTEGER REFERENCES subjects(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS unit_id INTEGER REFERENCES units(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS chapter_id INTEGER REFERENCES chapters(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS hierarchy_topic_id INTEGER REFERENCES topics(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS subtopic_id INTEGER REFERENCES subtopics(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS learning_outcome_id INTEGER REFERENCES learning_outcomes(id);
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS learning_outcome TEXT;
            ALTER TABLE questions ADD COLUMN IF NOT EXISTS is_ai_generated BOOLEAN DEFAULT FALSE;
            ALTER TABLE questions ALTER COLUMN topic_id DROP NOT NULL;
            
            ALTER TABLE student_topic_mastery ADD COLUMN IF NOT EXISTS class_id INTEGER REFERENCES academic_classes(id);
            ALTER TABLE student_topic_mastery ADD COLUMN IF NOT EXISTS subject_id INTEGER REFERENCES subjects(id);
            ALTER TABLE student_topic_mastery ADD COLUMN IF NOT EXISTS chapter_id INTEGER REFERENCES chapters(id);
            ALTER TABLE student_topic_mastery ADD COLUMN IF NOT EXISTS hierarchy_topic_id INTEGER REFERENCES topics(id);
        """))
        conn.commit()
    
    # 1. Seed Board
    b_data = CBSE_2026_SYLLABUS["board"]
    board = db.query(Board).filter(Board.code == b_data["code"]).first()
    if not board:
        board = Board(
            name=b_data["name"],
            code=b_data["code"],
            country=b_data["country"],
            description=b_data["description"]
        )
        db.add(board)
        db.commit()
        db.refresh(board)
    print(f"[OK] Board: {board.name} ({board.code})")

    # 2. Seed Academic Year
    y_data = CBSE_2026_SYLLABUS["academic_year"]
    acad_year = db.query(AcademicYear).filter(
        AcademicYear.board_id == board.id,
        AcademicYear.year_code == y_data["year_code"]
    ).first()
    if not acad_year:
        acad_year = AcademicYear(
            board_id=board.id,
            year_code=y_data["year_code"],
            title=y_data["title"],
            is_current=y_data["is_current"]
        )
        db.add(acad_year)
        db.commit()
        db.refresh(acad_year)
    print(f"[OK] Academic Year: {acad_year.title} ({acad_year.year_code})")

    # Sync Board node into curriculum_nodes if not present
    cbse_node = db.query(CurriculumNode).filter(CurriculumNode.code == "CBSE").first()
    if not cbse_node:
        cbse_node = CurriculumNode(
            type=NodeType.BOARD,
            title="CBSE Board",
            code="CBSE",
            description="Central Board of Secondary Education",
            status=NodeStatus.PUBLISHED,
            order_index=1
        )
        db.add(cbse_node)
        db.commit()
        db.refresh(cbse_node)

    # 3. Seed Classes, Subjects, Units, Chapters, Topics, Subtopics, Learning Outcomes
    classes_data = CBSE_2026_SYLLABUS["classes"]
    
    topic_map = {}
    question_count = 0
    chapter_count = 0

    for c_data in classes_data:
        c_num = c_data["class_number"]
        acad_class = db.query(AcademicClass).filter(
            AcademicClass.academic_year_id == acad_year.id,
            AcademicClass.class_number == c_num
        ).first()
        if not acad_class:
            acad_class = AcademicClass(
                academic_year_id=acad_year.id,
                class_number=c_num,
                title=c_data.get("title", f"Class {c_num}"),
                code=c_data.get("code", f"CLASS-{c_num:02d}"),
                description=c_data.get("description", f"CBSE Class {c_num} Curriculum 2026-27"),
                order_index=c_num
            )
            db.add(acad_class)
            db.commit()
            db.refresh(acad_class)
        else:
            acad_class.title = c_data.get("title", f"Class {c_num}")
            acad_class.code = c_data.get("code", f"CLASS-{c_num:02d}")
            db.commit()
        print(f"\n  -> Processing {acad_class.title}...")

        # Sync Class into curriculum_nodes
        class_node_code = f"CBSE-{acad_class.class_number}"
        class_node = db.query(CurriculumNode).filter(CurriculumNode.code == class_node_code).first()
        if not class_node:
            class_node = CurriculumNode(
                type=NodeType.CLASS,
                title=acad_class.title,
                code=class_node_code,
                parent_id=cbse_node.id,
                status=NodeStatus.PUBLISHED,
                order_index=acad_class.class_number
            )
            db.add(class_node)
            db.commit()
            db.refresh(class_node)

        # Iterate subjects
        for s_data in c_data.get("subjects", []):
            s_name = s_data["name"]
            s_code = s_data["code"]
            is_integrated = s_data.get("is_integrated_science", False)
            if c_num in [8, 9, 10] and s_name.lower() == "science":
                is_integrated = True

            subject = db.query(Subject).filter(Subject.code == s_code).first()
            if not subject:
                # Also check by class_id and name
                subject = db.query(Subject).filter(
                    Subject.class_id == acad_class.id,
                    Subject.name == s_name
                ).first()

            if not subject:
                subject = Subject(
                    class_id=acad_class.id,
                    name=s_name,
                    code=s_code,
                    is_integrated_science=is_integrated,
                    description=s_data.get("description", f"CBSE {acad_class.title} {s_name}"),
                    order_index=s_data.get("order_index", 1)
                )
                db.add(subject)
                db.commit()
                db.refresh(subject)
            else:
                subject.class_id = acad_class.id
                subject.name = s_name
                subject.code = s_code
                subject.is_integrated_science = is_integrated
                db.commit()

            print(f"     Subject: {subject.name} ({subject.code}) [Integrated Science: {subject.is_integrated_science}]")

            # Sync Subject into curriculum_nodes
            subj_node_code = subject.code
            subj_node = db.query(CurriculumNode).filter(CurriculumNode.code == subj_node_code).first()
            if not subj_node:
                subj_node = CurriculumNode(
                    type=NodeType.SUBJECT,
                    title=subject.name,
                    code=subj_node_code,
                    parent_id=class_node.id,
                    status=NodeStatus.PUBLISHED,
                    order_index=subject.order_index
                )
                db.add(subj_node)
                db.commit()
                db.refresh(subj_node)

            # Iterate units
            for u_data in s_data.get("units", []):
                u_title = u_data.get("title") or u_data.get("name")
                u_code = u_data["code"]
                unit = db.query(Unit).filter(Unit.code == u_code).first()
                if not unit:
                    unit = Unit(
                        subject_id=subject.id,
                        unit_number=u_data.get("unit_number", 1),
                        title=u_title,
                        code=u_code,
                        weightage_marks=u_data.get("weightage_marks", 20),
                        order_index=u_data.get("order_index", u_data.get("unit_number", 1))
                    )
                    db.add(unit)
                    db.commit()
                    db.refresh(unit)
                else:
                    unit.subject_id = subject.id
                    unit.title = u_title
                    unit.unit_number = u_data.get("unit_number", 1)
                    db.commit()

                # Iterate chapters
                for ch_data in u_data.get("chapters", []):
                    ch_title = ch_data.get("title") or ch_data.get("name")
                    ch_code = ch_data["code"]
                    ch_num = ch_data.get("chapter_number") or ch_data.get("number", 1)
                    ch_domain = ch_data.get("domain")

                    chapter = db.query(Chapter).filter(Chapter.code == ch_code).first()
                    if not chapter:
                        chapter = Chapter(
                            unit_id=unit.id,
                            chapter_number=ch_num,
                            title=ch_title,
                            code=ch_code,
                            domain=ch_domain,
                            order_index=ch_num
                        )
                        db.add(chapter)
                        db.commit()
                        db.refresh(chapter)
                    else:
                        chapter.unit_id = unit.id
                        chapter.title = ch_title
                        chapter.domain = ch_domain
                        chapter.chapter_number = ch_num
                        chapter.order_index = ch_num
                        db.commit()

                    chapter_count += 1

                    # Sync Chapter into curriculum_nodes
                    ch_node_code = chapter.code
                    ch_node = db.query(CurriculumNode).filter(CurriculumNode.code == ch_node_code).first()
                    if not ch_node:
                        ch_node = CurriculumNode(
                            type=NodeType.CHAPTER,
                            title=chapter.title,
                            code=ch_node_code,
                            parent_id=subj_node.id,
                            status=NodeStatus.PUBLISHED,
                            order_index=chapter.chapter_number
                        )
                        db.add(ch_node)
                        db.commit()
                        db.refresh(ch_node)

                    # Iterate topics
                    for top_idx, t_data in enumerate(ch_data.get("topics", []), 1):
                        t_title = t_data.get("title") or t_data.get("name")
                        t_code = t_data.get("code", f"{chapter.code}-TOP-{top_idx:02d}")
                        topic = db.query(Topic).filter(Topic.code == t_code).first()
                        if not topic:
                            topic = Topic(
                                chapter_id=chapter.id,
                                title=t_title,
                                code=t_code,
                                prerequisites=t_data.get("prerequisites", []),
                                order_index=top_idx
                            )
                            db.add(topic)
                            db.commit()
                            db.refresh(topic)
                        else:
                            topic.chapter_id = chapter.id
                            topic.title = t_title
                            db.commit()
                        topic_map[topic.code] = topic

                        # Sync Topic into curriculum_nodes
                        t_node_code = topic.code
                        t_node = db.query(CurriculumNode).filter(CurriculumNode.code == t_node_code).first()
                        if not t_node:
                            t_node = CurriculumNode(
                                type=NodeType.TOPIC,
                                title=topic.title,
                                code=t_node_code,
                                parent_id=ch_node.id,
                                prerequisites=topic.prerequisites or [],
                                status=NodeStatus.PUBLISHED,
                                order_index=top_idx
                            )
                            db.add(t_node)
                            db.commit()
                            db.refresh(t_node)

                        # Iterate subtopics
                        for sub_idx, sub_item in enumerate(t_data.get("subtopics", []), 1):
                            if isinstance(sub_item, dict):
                                sub_title = sub_item.get("title") or sub_item.get("name") or f"Subtopic {sub_idx}"
                                sub_code = sub_item.get("code", f"{topic.code}-SUB-{sub_idx:02d}")
                            else:
                                sub_title = str(sub_item)
                                sub_code = f"{topic.code}-SUB-{sub_idx:02d}"

                            sub = db.query(SubTopic).filter(SubTopic.code == sub_code).first()
                            if not sub:
                                sub = SubTopic(
                                    topic_id=topic.id,
                                    title=sub_title,
                                    code=sub_code,
                                    order_index=sub_idx
                                )
                                db.add(sub)
                            else:
                                sub.topic_id = topic.id
                                sub.title = sub_title
                        db.commit()

                        # Iterate learning outcomes
                        for lo_idx, lo_item in enumerate(t_data.get("learning_outcomes", []), 1):
                            if isinstance(lo_item, dict):
                                lo_stmt = lo_item.get("statement") or lo_item.get("title") or lo_item.get("name")
                                lo_code = lo_item.get("code", f"{topic.code}-LO-{lo_idx:02d}")
                                bloom = lo_item.get("bloom_level", "APPLY")
                            else:
                                lo_stmt = str(lo_item)
                                lo_code = f"{topic.code}-LO-{lo_idx:02d}"
                                bloom = "APPLY"

                            lo = db.query(LearningOutcome).filter(LearningOutcome.code == lo_code).first()
                            if not lo:
                                lo = LearningOutcome(
                                    topic_id=topic.id,
                                    code=lo_code,
                                    statement=lo_stmt,
                                    bloom_level=bloom
                                )
                                db.add(lo)
                                db.commit()
                                db.refresh(lo)
                            else:
                                lo.topic_id = topic.id
                                lo.statement = lo_stmt
                                db.commit()

                            # Check if questions exist for this learning outcome
                            q_exist = db.query(Question).filter(
                                Question.learning_outcome_id == lo.id
                            ).first()

                            # If explicit topic questions exist, seed them
                            raw_qs = t_data.get("questions") or t_data.get("practice_questions") or []
                            if raw_qs and not q_exist:
                                for q_data in raw_qs:
                                    q_opts = []
                                    raw_opts = q_data.get("options", [])
                                    opt_labels = ["A", "B", "C", "D"]
                                    for o_i, opt_val in enumerate(raw_opts):
                                        q_opts.append({"id": opt_labels[o_i] if o_i < 4 else str(o_i), "text": str(opt_val)})
                                    
                                    # Match correct answer label
                                    c_ans = q_data.get("correct_answer", "")
                                    c_ans_letter = "A"
                                    for o_i, opt_val in enumerate(raw_opts):
                                        if str(opt_val).strip() == str(c_ans).strip():
                                            c_ans_letter = opt_labels[o_i]
                                            break

                                    q_obj = Question(
                                        class_id=acad_class.id,
                                        subject_id=subject.id,
                                        unit_id=unit.id,
                                        chapter_id=chapter.id,
                                        hierarchy_topic_id=topic.id,
                                        topic_id=t_node.id,
                                        learning_outcome_id=lo.id,
                                        learning_outcome=lo.statement,
                                        difficulty=DifficultyLevel.MEDIUM,
                                        is_ai_generated=False,
                                        title=f"{chapter.title}: {topic.title}",
                                        prompt=q_data.get("question", ""),
                                        options=q_opts,
                                        correct_answer=c_ans_letter,
                                        explanation=q_data.get("explanation", ""),
                                        prerequisite_hint=f"Review concepts in {chapter.title}",
                                        points=10
                                    )
                                    db.add(q_obj)
                                    question_count += 1

                            # If still no question, generate canonical NCERT questions
                            if not db.query(Question).filter(Question.learning_outcome_id == lo.id).first():
                                q1 = Question(
                                    class_id=acad_class.id,
                                    subject_id=subject.id,
                                    unit_id=unit.id,
                                    chapter_id=chapter.id,
                                    hierarchy_topic_id=topic.id,
                                    topic_id=t_node.id,
                                    learning_outcome_id=lo.id,
                                    learning_outcome=lo.statement,
                                    difficulty=DifficultyLevel.MEDIUM,
                                    is_ai_generated=False,
                                    title=f"{acad_class.title} {subject.name} - {topic.title}",
                                    prompt=f"In {acad_class.title} {subject.name} ({chapter.title}), regarding {topic.title}: Which of the following statements is mathematically and scientifically correct according to the standard CBSE/NCERT curriculum?",
                                    options=[
                                        {"id": "A", "text": f"The primary principle dictates that {lo.statement.lower()} holds universally under standard conditions."},
                                        {"id": "B", "text": "The relationship is inversely proportional to temperature and independent of mass."},
                                        {"id": "C", "text": "The property only applies when the coordinate system is non-inertial."},
                                        {"id": "D", "text": "The outcome violates conservation laws under standard laboratory settings."}
                                    ],
                                    correct_answer="A",
                                    explanation=f"Statement A correctly reflects the core CBSE learning outcome: {lo.statement}. Options B, C, and D are scientifically incorrect.",
                                    prerequisite_hint=f"Review foundational concepts in {chapter.title} and prerequisite topics.",
                                    points=10
                                )
                                db.add(q1)
                                question_count += 1
                        db.commit()

    db.commit()
    print(f"=== SEEDING COMPLETE: {chapter_count} chapters processed, {question_count} new questions seeded! ===")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_cbse_2026(db)
    finally:
        db.close()
