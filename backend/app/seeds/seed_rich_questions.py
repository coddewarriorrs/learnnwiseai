"""
LearnWise AI - Seed Rich CBSE/NCERT Questions
Ensures every single chapter in Classes 8-12 has authentic, unique, syllabus-aligned questions.
Enforces 100% prompt uniqueness so questions never repeat.
"""

from app.database import SessionLocal
from app.models.question import Question, DifficultyLevel
from app.models.syllabus_hierarchy import AcademicClass, Subject, Unit, Chapter, Topic
from app.services.question_generator_service import QuestionGeneratorService

def seed_rich_questions():
    db = SessionLocal()
    try:
        print("=== Checking existing questions in database ===")
        total_q = db.query(Question).count()
        print(f"Current total distinct questions: {total_q}")

        classes = db.query(AcademicClass).order_by(AcademicClass.class_number).all()
        TARGET_PER_CHAPTER = 6
        total_new_seeded = 0

        existing_prompts = set(p[0] for p in db.query(Question.prompt).all())

        for ac in classes:
            print(f"\nSeeding questions for {ac.title}...")
            subjects = db.query(Subject).filter(Subject.class_id == ac.id).all()
            for subj in subjects:
                chapters = (
                    db.query(Chapter)
                    .join(Unit, Unit.id == Chapter.unit_id)
                    .filter(Unit.subject_id == subj.id)
                    .order_by(Chapter.order_index)
                    .all()
                )
                for ch in chapters:
                    ch_q_count = db.query(Question).filter(Question.chapter_id == ch.id).count()
                    needed = TARGET_PER_CHAPTER - ch_q_count
                    if needed <= 0:
                        continue

                    t = db.query(Topic).filter(Topic.chapter_id == ch.id).first()
                    topic_id = t.id if t else None

                    attempts = 0
                    while ch_q_count < TARGET_PER_CHAPTER and attempts < 25:
                        attempts += 1
                        diff = [DifficultyLevel.EASY, DifficultyLevel.MEDIUM, DifficultyLevel.HARD][ch_q_count % 3]
                        # Generate single candidate
                        q_dict = QuestionGeneratorService._generate_single_question(
                            class_title=ac.title,
                            subject_name=subj.name,
                            chapter_title=ch.title,
                            difficulty=diff
                        )

                        if q_dict["prompt"] in existing_prompts:
                            continue

                        existing_prompts.add(q_dict["prompt"])
                        q_obj = Question(
                            class_id=ac.id,
                            subject_id=subj.id,
                            unit_id=ch.unit_id,
                            chapter_id=ch.id,
                            hierarchy_topic_id=topic_id,
                            title=f"{ch.title}: {q_dict['title']}",
                            prompt=q_dict["prompt"],
                            options=q_dict["options"],
                            correct_answer=q_dict["correct_answer"],
                            explanation=q_dict["explanation"],
                            prerequisite_hint=q_dict.get("prerequisite_hint", f"Review concepts in {ch.title}."),
                            difficulty=diff,
                            points=10,
                            is_ai_generated=True
                        )
                        db.add(q_obj)
                        db.commit()
                        ch_q_count += 1
                        total_new_seeded += 1

        db.commit()
        final_total = db.query(Question).count()
        print(f"\n=== SEEDING COMPLETED ===")
        print(f"Total new unique questions added: {total_new_seeded}")
        print(f"Final total active questions in database: {final_total}")

    finally:
        db.close()

if __name__ == "__main__":
    seed_rich_questions()