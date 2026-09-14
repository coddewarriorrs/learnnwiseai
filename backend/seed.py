import sys
from datetime import datetime, timezone, timedelta
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.models.syllabus import CurriculumNode, NodeType, NodeStatus
from app.models.question import Question, DifficultyLevel
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AnswerRecord, AttemptStatus
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.risk import RiskPrediction, RiskLevel
from app.models.intervention import Intervention, InterventionType, InterventionStatus, TeacherStudentNote
from app.models.assignment import Assignment, AssignmentSubmission, SubmissionStatus
from app.core.security import get_password_hash
from app.services.risk_engine import RiskEngine

def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print('Seeding database with realistic LearnWise AI data...')

    # 1. Users
    pw_hash = get_password_hash('LearnWise@2026')

    admin = db.query(User).filter(User.email == 'admin@learnwise.ai').first()
    if not admin:
        admin = User(
            email='admin@learnwise.ai',
            hashed_password=pw_hash,
            full_name='Platform Administrator',
            role=UserRole.ADMIN,
            parent_access_token='parent-token-admin'
        )
        db.add(admin)

    teacher = db.query(User).filter(User.email == 'teacher@learnwise.ai').first()
    if not teacher:
        teacher = User(
            email='teacher@learnwise.ai',
            hashed_password=pw_hash,
            full_name='Dr. Eleanor Vance',
            role=UserRole.TEACHER,
            parent_access_token='parent-token-teacher'
        )
        db.add(teacher)

    arjun = db.query(User).filter(User.email == 'arjun@learnwise.ai').first()
    if not arjun:
        arjun = User(
            email='arjun@learnwise.ai',
            hashed_password=pw_hash,
            full_name='Arjun Mehta',
            role=UserRole.STUDENT,
            grade_level='Grade 11',
            parent_access_token='parent-token-arjun-11'
        )
        db.add(arjun)

    priya = db.query(User).filter(User.email == 'priya@learnwise.ai').first()
    if not priya:
        priya = User(
            email='priya@learnwise.ai',
            hashed_password=pw_hash,
            full_name='Priya Sharma',
            role=UserRole.STUDENT,
            grade_level='Grade 11',
            parent_access_token='parent-token-priya-11'
        )
        db.add(priya)

    rohit = db.query(User).filter(User.email == 'rohit@learnwise.ai').first()
    if not rohit:
        rohit = User(
            email='rohit@learnwise.ai',
            hashed_password=pw_hash,
            full_name='Rohit Verma',
            role=UserRole.STUDENT,
            grade_level='Grade 11',
            parent_access_token='parent-token-rohit-11'
        )
        db.add(rohit)

    db.commit()
    db.refresh(teacher)
    db.refresh(arjun)
    db.refresh(priya)
    db.refresh(rohit)

    # 2. Classes
    from app.curriculum_data import CLASSES_DATA, NODES_DATA, QUESTIONS_DATA

    for cd in CLASSES_DATA:
        existing_cls = db.query(Class).filter(Class.class_code == cd['class_code']).first()
        if not existing_cls:
            new_cls = Class(
                name=cd['name'],
                grade=cd['grade'],
                subject=cd['subject'],
                board='CBSE',
                academic_year='2026-2027',
                teacher_id=teacher.id,
                class_code=cd['class_code'],
                invite_token=cd['invite_token'],
                invite_active=True
            )
            db.add(new_cls)
    db.commit()

    cls1 = db.query(Class).filter(Class.class_code == 'MATH11').first()
    cls2 = db.query(Class).filter(Class.class_code == 'PHYS11').first()

    # Enroll Arjun, Priya, and Rohit into all Grade 11 cohorts
    all_grade11_classes = db.query(Class).filter(Class.grade == '11').all()
    for c in all_grade11_classes:
        for s in [arjun, priya, rohit]:
            if not db.query(ClassMember).filter(ClassMember.class_id == c.id, ClassMember.student_id == s.id).first():
                db.add(ClassMember(class_id=c.id, student_id=s.id))
    db.commit()

    # 3. Curriculum & Syllabus Hierarchy (Mathematics, Physics, Chemistry, Biology)
    code_to_id = {}
    for n in NODES_DATA:
        existing = db.query(CurriculumNode).filter(CurriculumNode.code == n['code']).first()
        parent_id = code_to_id.get(n['parent'])
        node_type = NodeType[n['type']] if isinstance(n['type'], str) else n['type']
        if not existing:
            node = CurriculumNode(
                type=node_type,
                title=n['title'],
                code=n['code'],
                parent_id=parent_id,
                prerequisites=n['prereqs'],
                status=NodeStatus.PUBLISHED
            )
            db.add(node)
            db.commit()
            db.refresh(node)
            code_to_id[n['code']] = node.id
        else:
            if parent_id and not existing.parent_id:
                existing.parent_id = parent_id
            existing.prerequisites = n['prereqs']
            db.commit()
            code_to_id[n['code']] = existing.id

    # 4. Question Bank (Diverse multi-subject pool)
    created_questions = []
    for qd in QUESTIONS_DATA:
        existing = db.query(Question).filter(Question.title == qd['title']).first()
        topic_id = code_to_id.get(qd['topic_code'])
        if not topic_id:
            top_node = db.query(CurriculumNode).filter(CurriculumNode.code == qd['topic_code']).first()
            topic_id = top_node.id if top_node else None

        diff = DifficultyLevel[qd['difficulty']] if isinstance(qd['difficulty'], str) else qd['difficulty']
        if not existing and topic_id:
            q = Question(
                topic_id=topic_id,
                title=qd['title'],
                prompt=qd['prompt'],
                options=qd['options'],
                correct_answer=qd['correct_answer'],
                explanation=qd['explanation'],
                prerequisite_hint=qd['prerequisite_hint'],
                difficulty=diff,
                points=qd['points']
            )
            db.add(q)
            db.commit()
            db.refresh(q)
            created_questions.append(q)
        elif existing:
            created_questions.append(existing)
    db.commit()

    # 5. Initialize Fresh Student Learning Twins (clean slate, zero fake attempts)
    from app.services.reset_service import LearningProfileResetService
    LearningProfileResetService.reset_all_student_profiles(db)

    print('Database seeded successfully!')
    print('Seed Accounts:')
    print('  Admin:   admin@learnwise.ai   / LearnWise@2026')
    print('  Teacher: teacher@learnwise.ai / LearnWise@2026')
    print('  Student: arjun@learnwise.ai   / LearnWise@2026 (HIGH RISK - Calculus gap)')
    print('  Student: priya@learnwise.ai   / LearnWise@2026 (MEDIUM RISK)')
    print('  Student: rohit@learnwise.ai   / LearnWise@2026 (LOW RISK - Strong)')
    print('  Class Code: MATH11 | Invite URL: /join/math11-invite-token-abc')
    db.close()

if __name__ == '__main__':
    run_seed()
