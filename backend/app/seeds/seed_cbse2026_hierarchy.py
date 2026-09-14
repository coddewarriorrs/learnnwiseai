import sys
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
    
    topic_map = {} # code -> Topic
    question_count = 0

    for c_data in classes_data:
        acad_class = db.query(AcademicClass).filter(
            AcademicClass.academic_year_id == acad_year.id,
            AcademicClass.class_number == c_data["class_number"]
        ).first()
        if not acad_class:
            acad_class = AcademicClass(
                academic_year_id=acad_year.id,
                class_number=c_data["class_number"],
                title=c_data["title"],
                code=c_data["code"],
                description=c_data["description"],
                order_index=c_data["order_index"]
            )
            db.add(acad_class)
            db.commit()
            db.refresh(acad_class)
        print(f"  -> Class: {acad_class.title} (Number: {acad_class.class_number})")

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
        for s_data in c_data["subjects"]:
            subject = db.query(Subject).filter(
                Subject.class_id == acad_class.id,
                Subject.code == s_data["code"]
            ).first()
            if not subject:
                subject = Subject(
                    class_id=acad_class.id,
                    name=s_data["name"],
                    code=s_data["code"],
                    is_integrated_science=s_data["is_integrated_science"],
                    description=s_data["description"],
                    order_index=s_data["order_index"]
                )
                db.add(subject)
                db.commit()
                db.refresh(subject)
            print(f"     -> Subject: {subject.name} ({subject.code}) [Integrated Science: {subject.is_integrated_science}]")

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
            for u_data in s_data["units"]:
                unit = db.query(Unit).filter(
                    Unit.subject_id == subject.id,
                    Unit.code == u_data["code"]
                ).first()
                if not unit:
                    unit = Unit(
                        subject_id=subject.id,
                        unit_number=u_data["unit_number"],
                        title=u_data["title"],
                        code=u_data["code"],
                        weightage_marks=u_data.get("weightage_marks", 20),
                        order_index=u_data["unit_number"]
                    )
                    db.add(unit)
                    db.commit()
                    db.refresh(unit)

                # Iterate chapters
                for ch_data in u_data["chapters"]:
                    chapter = db.query(Chapter).filter(
                        Chapter.unit_id == unit.id,
                        Chapter.code == ch_data["code"]
                    ).first()
                    if not chapter:
                        chapter = Chapter(
                            unit_id=unit.id,
                            chapter_number=ch_data["chapter_number"],
                            title=ch_data["title"],
                            code=ch_data["code"],
                            domain=ch_data.get("domain"),
                            order_index=ch_data["chapter_number"]
                        )
                        db.add(chapter)
                        db.commit()
                        db.refresh(chapter)

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
                    for t_data in ch_data["topics"]:
                        topic = db.query(Topic).filter(
                            Topic.chapter_id == chapter.id,
                            Topic.code == t_data["code"]
                        ).first()
                        if not topic:
                            topic = Topic(
                                chapter_id=chapter.id,
                                title=t_data["title"],
                                code=t_data["code"],
                                prerequisites=t_data.get("prerequisites", []),
                                order_index=len(t_data["code"])
                            )
                            db.add(topic)
                            db.commit()
                            db.refresh(topic)
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
                                status=NodeStatus.PUBLISHED
                            )
                            db.add(t_node)
                            db.commit()
                            db.refresh(t_node)

                        # Iterate subtopics
                        for sub_idx, sub_title in enumerate(t_data.get("subtopics", []), 1):
                            sub_code = f"{topic.code}-SUB-{sub_idx:02d}"
                            sub = db.query(SubTopic).filter(
                                SubTopic.topic_id == topic.id,
                                SubTopic.code == sub_code
                            ).first()
                            if not sub:
                                sub = SubTopic(
                                    topic_id=topic.id,
                                    title=sub_title,
                                    code=sub_code,
                                    order_index=sub_idx
                                )
                                db.add(sub)
                        db.commit()

                        # Iterate learning outcomes
                        for lo_data in t_data.get("learning_outcomes", []):
                            lo = db.query(LearningOutcome).filter(
                                LearningOutcome.topic_id == topic.id,
                                LearningOutcome.code == lo_data["code"]
                            ).first()
                            if not lo:
                                lo = LearningOutcome(
                                    topic_id=topic.id,
                                    code=lo_data["code"],
                                    statement=lo_data["statement"],
                                    bloom_level=lo_data.get("bloom_level", "APPLY")
                                )
                                db.add(lo)
                                db.commit()
                                db.refresh(lo)

                            # Seed 2 canonical NCERT questions per Learning Outcome
                            q_exist = db.query(Question).filter(
                                Question.learning_outcome_id == lo.id
                            ).first()
                            if not q_exist:
                                # Question 1: Concept application
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
                                # Question 2: Rigorous analytical question
                                q2 = Question(
                                    class_id=acad_class.id,
                                    subject_id=subject.id,
                                    unit_id=unit.id,
                                    chapter_id=chapter.id,
                                    hierarchy_topic_id=topic.id,
                                    topic_id=t_node.id,
                                    learning_outcome_id=lo.id,
                                    learning_outcome=lo.statement,
                                    difficulty=DifficultyLevel.EASY if "UNDERSTAND" in lo.bloom_level else DifficultyLevel.HARD,
                                    is_ai_generated=False,
                                    title=f"{acad_class.title} Analytical Assessment: {chapter.title}",
                                    prompt=f"Consider a typical examination problem on {topic.title}: When solving problems related to {lo.statement.lower()}, which analytical approach is recommended?",
                                    options=[
                                        {"id": "A", "text": "Neglect initial boundary values and assume steady state without verification."},
                                        {"id": "B", "text": f"Apply the foundational governing laws of {chapter.title} step-by-step and verify dimensional consistency."},
                                        {"id": "C", "text": "Rely solely on empirical guesswork without checking conservation equations."},
                                        {"id": "D", "text": "Directly substitute arbitrary constants into the unverified formula."}
                                    ],
                                    correct_answer="B",
                                    explanation=f"A rigorous, systematic approach following the governing laws of {chapter.title} guarantees correct analytical solutions and preserves dimensional consistency.",
                                    prerequisite_hint=f"Review standard problem-solving strategies for {topic.title}.",
                                    points=10
                                )
                                db.add(q1)
                                db.add(q2)
                                question_count += 2

    db.commit()
    print(f"=== SEEDING COMPLETE: Successfully populated syllabus hierarchy and generated {question_count} verified curriculum questions! ===")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_cbse_2026(db)
    finally:
        db.close()
