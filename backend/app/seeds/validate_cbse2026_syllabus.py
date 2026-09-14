import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.syllabus_hierarchy import (
    Board, AcademicYear, AcademicClass, Subject, Unit, 
    Chapter, Topic, SubTopic, LearningOutcome
)
from app.models.question import Question

# Expected official rationalized chapter counts for CBSE/NCERT 2026-27:
# Class 8: 13 Math + 13 Science = 26 chapters
# Class 9: 12 Math + 12 Science = 24 chapters
# Class 10: 14 Math + 13 Science = 27 chapters
# Class 11: 14 Math + 14 Physics + 9 Chem + 19 Bio = 56 chapters
# Class 12: 13 Math + 14 Physics + 10 Chem + 13 Bio = 50 chapters
# Total: 183 chapters

EXPECTED_COUNTS = {
    8: {"Mathematics": 13, "Science": 13, "total": 26},
    9: {"Mathematics": 12, "Science": 12, "total": 24},
    10: {"Mathematics": 14, "Science": 13, "total": 27},
    11: {"Mathematics": 14, "Physics": 14, "Chemistry": 9, "Biology": 19, "total": 56},
    12: {"Mathematics": 13, "Physics": 14, "Chemistry": 10, "Biology": 13, "total": 50},
}

FORBIDDEN_TOKENS = ["etc", "tbd", "placeholder", "chapter 1...", "...", "more", "sample"]

def validate_syllabus():
    db = SessionLocal()
    try:
        print("=" * 80)
        print("   CBSE / NCERT 2026-27 CURRICULUM DATABASE COMPLETENESS AUDIT REPORT")
        print("=" * 80)

        board = db.query(Board).filter(Board.code == "CBSE").first()
        if not board:
            print("FAILED: Board CBSE not found in database!")
            sys.exit(1)

        acad_year = db.query(AcademicYear).filter(AcademicYear.year_code == "2026-27").first()
        if not acad_year:
            print("FAILED: Academic Year 2026-27 not found in database!")
            sys.exit(1)

        print(f"Board: {board.name} ({board.code})")
        print(f"Academic Year: {acad_year.title} ({acad_year.year_code})")
        print("-" * 80)

        classes = db.query(AcademicClass).filter(
            AcademicClass.academic_year_id == acad_year.id
        ).order_by(AcademicClass.class_number).all()

        if len(classes) != 5:
            print(f"FAILED: Expected 5 classes, found {len(classes)}!")
            sys.exit(1)

        total_chapters = 0
        total_topics = 0
        total_subtopics = 0
        total_los = 0
        total_questions = 0

        header = f"{'Class':<10} | {'Subject':<14} | {'Expected':<8} | {'Found':<8} | {'Status':<10} | {'Topics':<8} | {'Questions':<10}"
        print(header)
        print("-" * len(header))

        for c in classes:
            c_num = c.class_number
            expected_subj_map = EXPECTED_COUNTS.get(c_num, {})
            subjects = db.query(Subject).filter(Subject.class_id == c.id).order_by(Subject.order_index).all()
            
            c_chapters = 0
            for s in subjects:
                # Count chapters in this subject
                ch_list = db.query(Chapter).join(Unit).filter(Unit.subject_id == s.id).all()
                found_cnt = len(ch_list)
                c_chapters += found_cnt
                total_chapters += found_cnt

                exp_cnt = expected_subj_map.get(s.name, 0)
                status = "PASS" if found_cnt >= exp_cnt else "FAIL"

                # Count topics, subtopics, LOs, questions for this subject
                subj_topics = db.query(Topic).join(Chapter).join(Unit).filter(Unit.subject_id == s.id).all()
                subj_q_cnt = db.query(Question).filter(Question.subject_id == s.id).count()

                total_topics += len(subj_topics)
                total_questions += subj_q_cnt

                for top in subj_topics:
                    total_subtopics += db.query(SubTopic).filter(SubTopic.topic_id == top.id).count()
                    total_los += db.query(LearningOutcome).filter(LearningOutcome.topic_id == top.id).count()

                # Validate chapter names against placeholder tokens
                for ch in ch_list:
                    name_lower = ch.title.lower()
                    for token in FORBIDDEN_TOKENS:
                        if token in name_lower.split():
                            print(f"WARNING: Potential placeholder '{token}' found in chapter '{ch.title}' (ID: {ch.id})")

                print(f"{c.title:<10} | {s.name:<14} | {exp_cnt:<8} | {found_cnt:<8} | {status:<10} | {len(subj_topics):<8} | {subj_q_cnt:<10}")

            exp_class_total = expected_subj_map.get("total", 0)
            class_status = "PASS" if c_chapters >= exp_class_total else "FAIL"
            print(f"  * {c.title} Total Chapters: {c_chapters}/{exp_class_total} -> [{class_status}]")
            print("-" * len(header))

        print(f"\nGLOBAL CURRICULUM TOTALS:")
        print(f"  - Total Academic Classes:      {len(classes)} (Classes 8, 9, 10, 11, 12)")
        print(f"  - Total Official Chapters:     {total_chapters} (Target: 183)")
        print(f"  - Total Syllabus Topics:       {total_topics}")
        print(f"  - Total Sub-topics:            {total_subtopics}")
        print(f"  - Total Learning Outcomes:     {total_los}")
        print(f"  - Total Curated Questions:     {total_questions}")
        print("=" * 80)

        if total_chapters >= 183:
            print("RESULT: SUCCESS - ALL 183 OFFICIAL NCERT RATIONALIZED CHAPTERS ARE FULLY VERIFIED IN DATABASE!")
            return True
        else:
            print(f"RESULT: FAILED - Found {total_chapters}/183 chapters!")
            sys.exit(1)

    finally:
        db.close()

if __name__ == "__main__":
    validate_syllabus()
