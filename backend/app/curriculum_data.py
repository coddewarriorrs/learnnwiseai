# LearnWise AI Complete Multi-Subject Curriculum & Question Bank
# Covers: Mathematics, Physics, Chemistry, Biology (CBSE Class 11 & 12)

NODES_DATA = [
    # Board
    {'type': 'BOARD', 'title': 'CBSE Board', 'code': 'CBSE', 'parent': None, 'prereqs': []},
    
    # Classes
    {'type': 'CLASS', 'title': 'Class 11', 'code': 'CBSE-11', 'parent': 'CBSE', 'prereqs': []},
    {'type': 'CLASS', 'title': 'Class 12', 'code': 'CBSE-12', 'parent': 'CBSE', 'prereqs': []},
    
    # ==========================================
    # 1. MATHEMATICS (Class 11 & 12)
    # ==========================================
    {'type': 'SUBJECT', 'title': 'Mathematics', 'code': 'MATH-11', 'parent': 'CBSE-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Algebraic Foundations', 'code': 'CH-ALG', 'parent': 'MATH-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Calculus & Integration', 'code': 'CH-CALC', 'parent': 'MATH-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Linear Algebra & Vectors', 'code': 'CH-LA', 'parent': 'MATH-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Probability & Statistics', 'code': 'CH-STAT', 'parent': 'MATH-11', 'prereqs': []},
    
    {'type': 'TOPIC', 'title': 'Algebraic Manipulation', 'code': 'TOP-ALG-01', 'parent': 'CH-ALG', 'prereqs': []},
    {'type': 'TOPIC', 'title': 'Differentiation Basics', 'code': 'TOP-CALC-01', 'parent': 'CH-CALC', 'prereqs': ['TOP-ALG-01']},
    {'type': 'TOPIC', 'title': 'Indefinite Integrals', 'code': 'TOP-CALC-02', 'parent': 'CH-CALC', 'prereqs': ['TOP-CALC-01', 'TOP-ALG-01']},
    {'type': 'TOPIC', 'title': 'Integration by Parts', 'code': 'TOP-CALC-03', 'parent': 'CH-CALC', 'prereqs': ['TOP-CALC-02', 'TOP-CALC-01', 'TOP-ALG-01']},
    {'type': 'TOPIC', 'title': 'Matrices & Determinants', 'code': 'TOP-LA-01', 'parent': 'CH-LA', 'prereqs': ['TOP-ALG-01']},
    {'type': 'TOPIC', 'title': 'Vectors & 3D Geometry', 'code': 'TOP-LA-02', 'parent': 'CH-LA', 'prereqs': ['TOP-ALG-01']},
    {'type': 'TOPIC', 'title': 'Probability Distributions', 'code': 'TOP-STAT-01', 'parent': 'CH-STAT', 'prereqs': ['TOP-ALG-01']},

    # ==========================================
    # 2. PHYSICS (Class 11 & 12)
    # ==========================================
    {'type': 'SUBJECT', 'title': 'Physics', 'code': 'PHYS-11', 'parent': 'CBSE-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Kinematics & Dynamics', 'code': 'CH-PHYS-KIN', 'parent': 'PHYS-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Work, Energy & Power', 'code': 'CH-PHYS-EN', 'parent': 'PHYS-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Gravitation', 'code': 'CH-PHYS-GRAV', 'parent': 'PHYS-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Electrostatics & Current', 'code': 'CH-PHYS-ELEC', 'parent': 'PHYS-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Optics & Wave Motion', 'code': 'CH-PHYS-OPT', 'parent': 'PHYS-11', 'prereqs': []},

    {'type': 'TOPIC', 'title': '1D & 2D Kinematics', 'code': 'TOP-PHYS-01', 'parent': 'CH-PHYS-KIN', 'prereqs': []},
    {'type': 'TOPIC', 'title': "Newton's Laws of Motion & Friction", 'code': 'TOP-PHYS-02', 'parent': 'CH-PHYS-KIN', 'prereqs': ['TOP-PHYS-01']},
    {'type': 'TOPIC', 'title': 'Work-Energy Theorem & Conservation', 'code': 'TOP-PHYS-03', 'parent': 'CH-PHYS-EN', 'prereqs': ['TOP-PHYS-02']},
    {'type': 'TOPIC', 'title': 'Universal Gravitation & Orbital Motion', 'code': 'TOP-PHYS-04', 'parent': 'CH-PHYS-GRAV', 'prereqs': ['TOP-PHYS-03', 'TOP-PHYS-01']},
    {'type': 'TOPIC', 'title': "Coulomb's Law & Electric Potential", 'code': 'TOP-PHYS-05', 'parent': 'CH-PHYS-ELEC', 'prereqs': ['TOP-PHYS-03']},
    {'type': 'TOPIC', 'title': "Current Electricity & Kirchhoff's Rules", 'code': 'TOP-PHYS-06', 'parent': 'CH-PHYS-ELEC', 'prereqs': ['TOP-PHYS-05']},
    {'type': 'TOPIC', 'title': 'Ray Optics & Refraction', 'code': 'TOP-PHYS-07', 'parent': 'CH-PHYS-OPT', 'prereqs': ['TOP-PHYS-01']},

    # ==========================================
    # 3. CHEMISTRY (Class 11 & 12)
    # ==========================================
    {'type': 'SUBJECT', 'title': 'Chemistry', 'code': 'CHEM-11', 'parent': 'CBSE-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Atomic Structure & Periodic Trends', 'code': 'CH-CHEM-STR', 'parent': 'CHEM-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Chemical Bonding & Molecular Geometry', 'code': 'CH-CHEM-BOND', 'parent': 'CHEM-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Chemical Energetics & Equilibrium', 'code': 'CH-CHEM-THERMO', 'parent': 'CHEM-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Organic Chemistry & Mechanisms', 'code': 'CH-CHEM-ORG', 'parent': 'CHEM-11', 'prereqs': []},

    {'type': 'TOPIC', 'title': 'Bohr Model & Quantum Numbers', 'code': 'TOP-CHEM-01', 'parent': 'CH-CHEM-STR', 'prereqs': []},
    {'type': 'TOPIC', 'title': 'Periodic Properties & Ionic Bonding', 'code': 'TOP-CHEM-02', 'parent': 'CH-CHEM-STR', 'prereqs': ['TOP-CHEM-01']},
    {'type': 'TOPIC', 'title': 'VSEPR Theory & Hybridization', 'code': 'TOP-CHEM-03', 'parent': 'CH-CHEM-BOND', 'prereqs': ['TOP-CHEM-02']},
    {'type': 'TOPIC', 'title': 'Enthalpy, Entropy & Free Energy', 'code': 'TOP-CHEM-04', 'parent': 'CH-CHEM-THERMO', 'prereqs': ['TOP-CHEM-02']},
    {'type': 'TOPIC', 'title': "Chemical Equilibrium & Le Chatelier's Principle", 'code': 'TOP-CHEM-05', 'parent': 'CH-CHEM-THERMO', 'prereqs': ['TOP-CHEM-04']},
    {'type': 'TOPIC', 'title': 'Hydrocarbons & Reaction Mechanisms', 'code': 'TOP-CHEM-06', 'parent': 'CH-CHEM-ORG', 'prereqs': ['TOP-CHEM-03']},
    {'type': 'TOPIC', 'title': 'Electrochemistry & Redox Potentials', 'code': 'TOP-CHEM-07', 'parent': 'CH-CHEM-THERMO', 'prereqs': ['TOP-CHEM-04']},

    # ==========================================
    # 4. BIOLOGY (Class 11 & 12)
    # ==========================================
    {'type': 'SUBJECT', 'title': 'Biology', 'code': 'BIO-11', 'parent': 'CBSE-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Cell Biology & Cell Cycle', 'code': 'CH-BIO-CELL', 'parent': 'BIO-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Genetics & Molecular Biology', 'code': 'CH-BIO-GEN', 'parent': 'BIO-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Human & Plant Physiology', 'code': 'CH-BIO-PHYS', 'parent': 'BIO-11', 'prereqs': []},
    {'type': 'CHAPTER', 'title': 'Ecology & Biodiversity', 'code': 'CH-BIO-ECO', 'parent': 'BIO-11', 'prereqs': []},

    {'type': 'TOPIC', 'title': 'Cell Organelles & Membrane Transport', 'code': 'TOP-BIO-01', 'parent': 'CH-BIO-CELL', 'prereqs': []},
    {'type': 'TOPIC', 'title': 'Mitosis, Meiosis & Cell Cycle Checkpoints', 'code': 'TOP-BIO-02', 'parent': 'CH-BIO-CELL', 'prereqs': ['TOP-BIO-01']},
    {'type': 'TOPIC', 'title': 'Mendelian Genetics & Monohybrid Crosses', 'code': 'TOP-BIO-03', 'parent': 'CH-BIO-GEN', 'prereqs': ['TOP-BIO-02']},
    {'type': 'TOPIC', 'title': 'DNA Replication & Protein Synthesis', 'code': 'TOP-BIO-04', 'parent': 'CH-BIO-GEN', 'prereqs': ['TOP-BIO-03', 'TOP-BIO-01']},
    {'type': 'TOPIC', 'title': 'Photosynthesis & Carbon Fixation', 'code': 'TOP-BIO-05', 'parent': 'CH-BIO-PHYS', 'prereqs': ['TOP-BIO-01']},
    {'type': 'TOPIC', 'title': 'Human Circulatory & Heart Function', 'code': 'TOP-BIO-06', 'parent': 'CH-BIO-PHYS', 'prereqs': ['TOP-BIO-01']},
    {'type': 'TOPIC', 'title': 'Ecosystem Dynamics & Food Webs', 'code': 'TOP-BIO-07', 'parent': 'CH-BIO-ECO', 'prereqs': ['TOP-BIO-05']}
]

CLASSES_DATA = [
    {
        'class_code': 'MATH11',
        'name': 'Grade 11 Advanced Mathematics',
        'grade': '11',
        'subject': 'Mathematics',
        'invite_token': 'math11-invite-token-abc'
    },
    {
        'class_code': 'PHYS11',
        'name': 'Grade 11 Classical Mechanics & Physics',
        'grade': '11',
        'subject': 'Physics',
        'invite_token': 'phys11-invite-token-xyz'
    },
    {
        'class_code': 'CHEM11',
        'name': 'Grade 11 General & Organic Chemistry',
        'grade': '11',
        'subject': 'Chemistry',
        'invite_token': 'chem11-invite-token-123'
    },
    {
        'class_code': 'BIO11',
        'name': 'Grade 11 Cellular Systems & Genetics',
        'grade': '11',
        'subject': 'Biology',
        'invite_token': 'bio11-invite-token-456'
    },
    {
        'class_code': 'MATH12',
        'name': 'Grade 12 Advanced Calculus & Vectors',
        'grade': '12',
        'subject': 'Mathematics',
        'invite_token': 'math12-invite-token-789'
    },
    {
        'class_code': 'PHYS12',
        'name': 'Grade 12 Electromagnetism & Modern Physics',
        'grade': '12',
        'subject': 'Physics',
        'invite_token': 'phys12-invite-token-321'
    }
]

QUESTIONS_DATA = [
    # =========================================================================
    # MATHEMATICS
    # =========================================================================
    # Algebraic Manipulation (TOP-ALG-01)
    {
        'topic_code': 'TOP-ALG-01',
        'title': 'Quadratic Factorization',
        'prompt': 'Find the roots of the quadratic equation: 2x^2 - 7x + 3 = 0.',
        'options': [
            {'id': 'A', 'text': 'x = 3, x = 1/2'},
            {'id': 'B', 'text': 'x = -3, x = -1/2'},
            {'id': 'C', 'text': 'x = 2, x = 3/2'},
            {'id': 'D', 'text': 'x = 1, x = 6'}
        ],
        'correct_answer': 'A',
        'explanation': 'Factoring: (2x - 1)(x - 3) = 0. Setting each factor to zero yields x = 1/2 and x = 3.',
        'prerequisite_hint': 'Review the quadratic formula x = (-b ± √(b^2 - 4ac)) / (2a) and middle-term splitting.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-ALG-01',
        'title': 'Logarithmic Expansion',
        'prompt': 'If log_10(2) = a and log_10(3) = b, express log_10(15) in terms of a and b.',
        'options': [
            {'id': 'A', 'text': '1 - a + b'},
            {'id': 'B', 'text': 'a + b - 1'},
            {'id': 'C', 'text': 'b / a'},
            {'id': 'D', 'text': '1 + a - b'}
        ],
        'correct_answer': 'A',
        'explanation': 'log_10(15) = log_10(30 / 2) = log_10(3 x 10 / 2) = log_10(3) + log_10(10) - log_10(2) = b + 1 - a = 1 - a + b.',
        'prerequisite_hint': 'Recall basic logarithm product and quotient rules: log(xy) = log x + log y and log(x/y) = log x - log y.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Differentiation Basics (TOP-CALC-01)
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Derivative of Quotient',
        'prompt': 'Find the first derivative of f(x) = (x^2 + 1) / (x - 1) with respect to x.',
        'options': [
            {'id': 'A', 'text': '(x^2 - 2x - 1) / (x - 1)^2'},
            {'id': 'B', 'text': '2x / (x - 1)^2'},
            {'id': 'C', 'text': '(x^2 + 2x - 1) / (x - 1)^2'},
            {'id': 'D', 'text': '(2x^2 - x) / (x - 1)^2'}
        ],
        'correct_answer': 'A',
        'explanation': 'By quotient rule [u/v]\' = (u\'v - uv\') / v^2: [2x(x - 1) - (x^2 + 1)(1)] / (x - 1)^2 = (2x^2 - 2x - x^2 - 1) / (x - 1)^2 = (x^2 - 2x - 1) / (x - 1)^2.',
        'prerequisite_hint': 'Make sure to apply the quotient rule order correctly: denominator times derivative of numerator minus numerator times derivative of denominator.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Chain Rule Derivative',
        'prompt': 'Find the derivative of f(x) = sin(3x^2 + 5).',
        'options': [
            {'id': 'A', 'text': '6x x cos(3x^2 + 5)'},
            {'id': 'B', 'text': 'cos(6x)'},
            {'id': 'C', 'text': '-6x x cos(3x^2 + 5)'},
            {'id': 'D', 'text': '3x x sin(3x^2 + 5)'}
        ],
        'correct_answer': 'A',
        'explanation': 'Let u = 3x^2 + 5 => du/dx = 6x. d/dx[sin(u)] = cos(u) x du/dx = 6x x cos(3x^2 + 5).',
        'prerequisite_hint': 'Review the chain rule dy/dx = (dy/du) x (du/dx).',
        'difficulty': 'EASY',
        'points': 10
    },

    # Indefinite Integrals (TOP-CALC-02)
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Substitution Method Integral',
        'prompt': 'Evaluate ∫ (2x) / (x^2 + 4) dx.',
        'options': [
            {'id': 'A', 'text': 'ln(x^2 + 4) + C'},
            {'id': 'B', 'text': '1 / (x^2 + 4)^2 + C'},
            {'id': 'C', 'text': '2 x ln(x^2 + 4) + C'},
            {'id': 'D', 'text': 'arctan(x/2) + C'}
        ],
        'correct_answer': 'A',
        'explanation': 'Substitute u = x^2 + 4, so du = 2x dx. The integral becomes ∫ (1/u) du = ln|u| + C = ln(x^2 + 4) + C.',
        'prerequisite_hint': 'Notice that the numerator 2x is the exact derivative of the denominator polynomial.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Integration by Parts (TOP-CALC-03)
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Integral of x x e^x',
        'prompt': 'Evaluate the indefinite integral: ∫ x x e^x dx',
        'options': [
            {'id': 'A', 'text': 'e^x (x - 1) + C'},
            {'id': 'B', 'text': 'e^x (x + 1) + C'},
            {'id': 'C', 'text': 'x^2 x e^x / 2 + C'},
            {'id': 'D', 'text': 'x x e^x - e^(-x) + C'}
        ],
        'correct_answer': 'A',
        'explanation': 'Using integration by parts: let u = x => du = dx, and dv = e^x dx => v = e^x. ∫ u dv = x e^x - ∫ e^x dx = e^x (x - 1) + C.',
        'prerequisite_hint': 'Recall the product integration formula ∫ u dv = u v - ∫ v du.',
        'difficulty': 'MEDIUM',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Integral of x x sin(x)',
        'prompt': 'Evaluate: ∫ x x sin(x) dx',
        'options': [
            {'id': 'A', 'text': 'x cos(x) - sin(x) + C'},
            {'id': 'B', 'text': '-x cos(x) + sin(x) + C'},
            {'id': 'C', 'text': '-x sin(x) + cos(x) + C'},
            {'id': 'D', 'text': 'x^2 / 2 x (-cos(x)) + C'}
        ],
        'correct_answer': 'B',
        'explanation': 'Let u = x => du = dx, and dv = sin(x) dx => v = -cos(x). ∫ u dv = -x cos(x) - ∫ (-cos(x)) dx = -x cos(x) + sin(x) + C.',
        'prerequisite_hint': 'Check standard trigonometric derivatives and integrals: ∫ sin(x) dx = -cos(x).',
        'difficulty': 'HARD',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Integral of ln(x)',
        'prompt': 'Evaluate: ∫ ln(x) dx',
        'options': [
            {'id': 'A', 'text': '1/x + C'},
            {'id': 'B', 'text': 'x ln(x) - x + C'},
            {'id': 'C', 'text': 'x ln(x) + x + C'},
            {'id': 'D', 'text': '(ln(x))^2 / 2 + C'}
        ],
        'correct_answer': 'B',
        'explanation': 'Let u = ln(x) => du = 1/x dx, and dv = dx => v = x. ∫ ln(x) dx = x ln(x) - ∫ x x (1/x) dx = x ln(x) - x + C.',
        'prerequisite_hint': 'Review the derivative of natural logarithm d/dx(ln x) = 1/x.',
        'difficulty': 'MEDIUM',
        'points': 10
    },

    # Vectors & 3D Geometry (TOP-LA-02)
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Vector Dot Product & Orthogonality',
        'prompt': 'For what value of k are the vectors a = 2i + 3j - k and b = i - 2j + 4k orthogonal?',
        'options': [
            {'id': 'A', 'text': 'k = -1'},
            {'id': 'B', 'text': 'k = 1'},
            {'id': 'C', 'text': 'k = -4'},
            {'id': 'D', 'text': 'k = 2'}
        ],
        'correct_answer': 'A',
        'explanation': 'Two vectors are orthogonal if their dot product is 0: a . b = (2)(1) + (3)(-2) + (-k)(4) = 2 - 6 - 4k = -4 - 4k = 0, giving k = -1.',
        'prerequisite_hint': 'Orthogonal vectors satisfy a . b = a_x b_x + a_y b_y + a_z b_z = 0.',
        'difficulty': 'MEDIUM',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Vector Magnitude Calculation',
        'prompt': 'Find the magnitude of the vector v = 3i - 4j + 12k.',
        'options': [
            {'id': 'A', 'text': '13'},
            {'id': 'B', 'text': '11'},
            {'id': 'C', 'text': '15'},
            {'id': 'D', 'text': '169'}
        ],
        'correct_answer': 'A',
        'explanation': 'The magnitude is calculated as sqrt(3^2 + (-4)^2 + 12^2) = sqrt(9 + 16 + 144) = sqrt(169) = 13.',
        'prerequisite_hint': 'Use the Euclidean norm formula: |v| = sqrt(x^2 + y^2 + z^2).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Unit Vector Along a Direction',
        'prompt': 'What is the unit vector in the direction of vector a = 2i + 3j + 6k?',
        'options': [
            {'id': 'A', 'text': '(2i + 3j + 6k) / 7'},
            {'id': 'B', 'text': '(2i + 3j + 6k) / 49'},
            {'id': 'C', 'text': '(2i + 3j + 6k) / 11'},
            {'id': 'D', 'text': 'i + j + k'}
        ],
        'correct_answer': 'A',
        'explanation': 'The magnitude of a is sqrt(2^2 + 3^2 + 6^2) = sqrt(4 + 9 + 36) = sqrt(49) = 7. The unit vector is a / |a| = (2i + 3j + 6k) / 7.',
        'prerequisite_hint': 'A unit vector has length 1 and equals vector divided by its magnitude.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Scalar Dot Product Evaluation',
        'prompt': 'If vector a = i + 2j + 3k and vector b = 4i - j + 2k, calculate the scalar product a . b.',
        'options': [
            {'id': 'A', 'text': '8'},
            {'id': 'B', 'text': '12'},
            {'id': 'C', 'text': '6'},
            {'id': 'D', 'text': '14'}
        ],
        'correct_answer': 'A',
        'explanation': 'The dot product is a . b = (1)(4) + (2)(-1) + (3)(2) = 4 - 2 + 6 = 8.',
        'prerequisite_hint': 'Multiply corresponding components and take their algebraic sum.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Vector Cross Product Magnitude',
        'prompt': 'Given |a| = 10, |b| = 2, and a . b = 12, what is the magnitude of the cross product |a x b|?',
        'options': [
            {'id': 'A', 'text': '16'},
            {'id': 'B', 'text': '8'},
            {'id': 'C', 'text': '20'},
            {'id': 'D', 'text': '12'}
        ],
        'correct_answer': 'A',
        'explanation': 'Using Lagranges identity: |a x b|^2 = |a|^2 |b|^2 - (a . b)^2 = (100)(4) - 144 = 400 - 144 = 256. Taking square root gives 16.',
        'prerequisite_hint': 'Recall |a x b|^2 + (a . b)^2 = |a|^2 |b|^2.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Projection of a Vector',
        'prompt': 'Find the projection of vector a = 2i + 3j + 2k on vector b = i + 2j + k.',
        'options': [
            {'id': 'A', 'text': '5 sqrt(6) / 3'},
            {'id': 'B', 'text': '10 / 6'},
            {'id': 'C', 'text': '6 / sqrt(10)'},
            {'id': 'D', 'text': '2 sqrt(6)'}
        ],
        'correct_answer': 'A',
        'explanation': 'Projection of a on b is (a . b) / |b|. Here a . b = 2(1) + 3(2) + 2(1) = 10, and |b| = sqrt(1 + 4 + 1) = sqrt(6). 10 / sqrt(6) simplifies to 5 sqrt(6) / 3.',
        'prerequisite_hint': 'Projection of a on b equals dot product of a and b divided by magnitude of b.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Angle Between Two Vectors',
        'prompt': 'Find the angle between the vectors a = i + j and b = j + k.',
        'options': [
            {'id': 'A', 'text': '60 degrees'},
            {'id': 'B', 'text': '45 degrees'},
            {'id': 'C', 'text': '90 degrees'},
            {'id': 'D', 'text': '30 degrees'}
        ],
        'correct_answer': 'A',
        'explanation': 'a . b = (1)(0) + (1)(1) + (0)(1) = 1. |a| = sqrt(2) and |b| = sqrt(2). cos(theta) = 1 / (sqrt(2) sqrt(2)) = 1/2, so theta = 60 degrees.',
        'prerequisite_hint': 'cos(theta) = (a . b) / (|a| |b|).',
        'difficulty': 'MEDIUM',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Collinear Vectors Condition',
        'prompt': 'If vectors a = 2i + 4j - 6k and b = -3i - 6j + m k are collinear, determine the value of m.',
        'options': [
            {'id': 'A', 'text': '9'},
            {'id': 'B', 'text': '-9'},
            {'id': 'C', 'text': '6'},
            {'id': 'D', 'text': '-6'}
        ],
        'correct_answer': 'A',
        'explanation': 'For collinear vectors, components are proportional: 2 / (-3) = 4 / (-6) = -6 / m. Equating gives 2m = 18, so m = 9.',
        'prerequisite_hint': 'Two vectors are collinear if a_1 / b_1 = a_2 / b_2 = a_3 / b_3.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Direction Cosines of a Line in 3D',
        'prompt': 'If a line in space makes angles 60 degrees with the x-axis and 60 degrees with the y-axis, what acute angle does it make with the z-axis?',
        'options': [
            {'id': 'A', 'text': '45 degrees'},
            {'id': 'B', 'text': '30 degrees'},
            {'id': 'C', 'text': '60 degrees'},
            {'id': 'D', 'text': '90 degrees'}
        ],
        'correct_answer': 'A',
        'explanation': 'Direction cosines satisfy cos^2(alpha) + cos^2(beta) + cos^2(gamma) = 1. cos^2(60) + cos^2(60) + cos^2(gamma) = 1/4 + 1/4 + cos^2(gamma) = 1, so cos^2(gamma) = 1/2, giving gamma = 45 degrees.',
        'prerequisite_hint': 'The sum of squares of direction cosines l^2 + m^2 + n^2 always equals 1.',
        'difficulty': 'HARD',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Scalar Triple Product & Volume',
        'prompt': 'Find the volume of the parallelepiped whose coterminous edges are represented by vectors a = i + j + k, b = i - j + k, and c = i + 2j - k.',
        'options': [
            {'id': 'A', 'text': '4 cubic units'},
            {'id': 'B', 'text': '6 cubic units'},
            {'id': 'C', 'text': '2 cubic units'},
            {'id': 'D', 'text': '8 cubic units'}
        ],
        'correct_answer': 'A',
        'explanation': 'Volume is the absolute value of determinant with rows [1, 1, 1], [1, -1, 1], [1, 2, -1]. Evaluating gives 1(1 - 2) - 1(-1 - 1) + 1(2 - (-1)) = -1 + 2 + 3 = 4 cubic units.',
        'prerequisite_hint': 'The scalar triple product [a b c] evaluates to the 3x3 determinant of vector components.',
        'difficulty': 'HARD',
        'points': 20
    },

    # =========================================================================
    # PHYSICS
    # =========================================================================
    # 1D & 2D Kinematics (TOP-PHYS-01)
    {
        'topic_code': 'TOP-PHYS-01',
        'title': 'Projectile Range & Angle',
        'prompt': 'At what launch angle θ relative to horizontal does a projectile launched on flat ground achieve maximum horizontal range?',
        'options': [
            {'id': 'A', 'text': '30°'},
            {'id': 'B', 'text': '45°'},
            {'id': 'C', 'text': '60°'},
            {'id': 'D', 'text': '90°'}
        ],
        'correct_answer': 'B',
        'explanation': 'Range R = (u^2 x sin(2θ)) / g. The sine function reaches its maximum value of 1 when 2θ = 90°, which corresponds to θ = 45°.',
        'prerequisite_hint': 'Review the projectile horizontal range formula and trigonometric maximum of sin(2θ).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-01',
        'title': 'Uniform Acceleration Stopping Distance',
        'prompt': 'A vehicle traveling at velocity v skids to a stop in distance d with constant deceleration. If its initial velocity is doubled to 2v under the same braking friction, what is the new stopping distance?',
        'options': [
            {'id': 'A', 'text': '2d'},
            {'id': 'B', 'text': '3d'},
            {'id': 'C', 'text': '4d'},
            {'id': 'D', 'text': 'd^2'}
        ],
        'correct_answer': 'C',
        'explanation': 'From kinematic equation v_f^2 = v_i^2 - 2ad: 0 = v^2 - 2ad => d = v^2 / (2a). Stopping distance scales quadratically with velocity, so doubling v quadruples distance to 4d.',
        'prerequisite_hint': 'Relate initial kinetic velocity to stopping distance using v^2 = u^2 + 2as.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Newton's Laws & Friction (TOP-PHYS-02)
    {
        'topic_code': 'TOP-PHYS-02',
        'title': 'Apparent Weight in an Accelerating Elevator',
        'prompt': 'A person of mass 60 kg stands on a scale inside an elevator accelerating upward at 2 m/s^2. If g = 9.8 m/s^2, what does the scale read?',
        'options': [
            {'id': 'A', 'text': '468 N'},
            {'id': 'B', 'text': '588 N'},
            {'id': 'C', 'text': '708 N'},
            {'id': 'D', 'text': '600 N'}
        ],
        'correct_answer': 'C',
        'explanation': 'By Newton\'s Second Law: N - mg = ma => N = m(g + a) = 60 x (9.8 + 2) = 60 x 11.8 = 708 N.',
        'prerequisite_hint': 'Draw a free-body diagram: normal force points upward, gravity points downward.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-PHYS-02',
        'title': 'Static vs Kinetic Friction',
        'prompt': 'Which statement correctly characterizes static friction (μ_s) compared to kinetic friction (μ_k) for the same contact surfaces?',
        'options': [
            {'id': 'A', 'text': 'Static friction is self-adjusting up to μ_s x N, and typically μ_s > μ_k'},
            {'id': 'B', 'text': 'Kinetic friction is always greater than static friction'},
            {'id': 'C', 'text': 'Static friction has a fixed constant magnitude regardless of applied force'},
            {'id': 'D', 'text': 'Both coefficients depend directly on surface contact area'}
        ],
        'correct_answer': 'A',
        'explanation': 'Static friction adjusts to match the applied parallel force until it reaches its limiting value f_max = μ_s x N. Once motion begins, kinetic friction is slightly lower because surface asperities do not interlock as deeply.',
        'prerequisite_hint': 'Review the transition from static threshold to sliding kinetic friction.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Work, Energy & Power (TOP-PHYS-03)
    {
        'topic_code': 'TOP-PHYS-03',
        'title': 'Work-Energy Theorem Application',
        'prompt': 'A 2 kg block slides across a rough horizontal surface with initial kinetic energy of 50 J. Friction does -30 J of work on the block. What is its final speed?',
        'options': [
            {'id': 'A', 'text': '4.47 m/s'},
            {'id': 'B', 'text': '5.0 m/s'},
            {'id': 'C', 'text': '20 m/s'},
            {'id': 'D', 'text': '2.0 m/s'}
        ],
        'correct_answer': 'A',
        'explanation': 'W_net = ΔK => KE_final = 50 - 30 = 20 J. KE = (1/2) m v^2 => 20 = (1/2)(2) v^2 => v^2 = 20 => v = √20 ≈ 4.47 m/s.',
        'prerequisite_hint': 'The net work done by all forces equals the change in kinetic energy: W_net = K_f - K_i.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Universal Gravitation (TOP-PHYS-04)
    {
        'topic_code': 'TOP-PHYS-04',
        'title': 'Gravitational Field vs Altitude',
        'prompt': 'At what altitude h above Earth\'s surface (radius R) does gravitational acceleration reduce to g / 4?',
        'options': [
            {'id': 'A', 'text': 'h = R/2'},
            {'id': 'B', 'text': 'h = R'},
            {'id': 'C', 'text': 'h = 2R'},
            {'id': 'D', 'text': 'h = 4R'}
        ],
        'correct_answer': 'B',
        'explanation': 'g(h) = GM / (R + h)^2 = g x [R / (R + h)]^2. For g(h) = g / 4, R / (R + h) = 1/2 => R + h = 2R => h = R.',
        'prerequisite_hint': 'Remember that radial distance r in Newton\'s law is measured from the planetary center of mass: r = R + h.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Coulomb's Law & Electric Field (TOP-PHYS-05)
    {
        'topic_code': 'TOP-PHYS-05',
        'title': 'Electric Dipole in Uniform Field',
        'prompt': 'What net force and net torque act on an electric dipole p in a uniform electric field E?',
        'options': [
            {'id': 'A', 'text': 'Net force = 0, Net torque = p × E'},
            {'id': 'B', 'text': 'Net force = qE, Net torque = 0'},
            {'id': 'C', 'text': 'Net force = p · E, Net torque = 0'},
            {'id': 'D', 'text': 'Both net force and net torque are zero'}
        ],
        'correct_answer': 'A',
        'explanation': 'In a uniform electric field, the forces on +q and -q are equal in magnitude and opposite in direction, so net force is 0. However, their lines of action differ, creating a torque τ = p × E.',
        'prerequisite_hint': 'Sum forces on equal and opposite charges +q and -q in an identical electric field.',
        'difficulty': 'HARD',
        'points': 20
    },

    # Current Electricity & Kirchhoff's Rules (TOP-PHYS-06)
    {
        'topic_code': 'TOP-PHYS-06',
        'title': 'Kirchhoff\'s Junction and Loop Laws',
        'prompt': 'Kirchhoff\'s Junction Rule (currents at a node) and Loop Rule (potentials around a closed circuit) represent conservation of which two fundamental physical quantities?',
        'options': [
            {'id': 'A', 'text': 'Electric Charge and Energy, respectively'},
            {'id': 'B', 'text': 'Energy and Momentum, respectively'},
            {'id': 'C', 'text': 'Electric Charge and Magnetic Flux, respectively'},
            {'id': 'D', 'text': 'Power and Voltage, respectively'}
        ],
        'correct_answer': 'A',
        'explanation': 'Kirchhoff\'s Current Law (junction rule) enforces conservation of electric charge (Σ I_in = Σ I_out). Kirchhoff\'s Voltage Law (loop rule) enforces conservation of energy around any closed loop (Σ ΔV = 0).',
        'prerequisite_hint': 'Review the conservation laws underlying circuit analysis.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Ray Optics (TOP-PHYS-07)
    {
        'topic_code': 'TOP-PHYS-07',
        'title': 'Total Internal Reflection & Critical Angle',
        'prompt': 'A light ray passes from a denser medium with refractive index n_1 = 1.5 into air (n_2 = 1.0). What is the critical angle for total internal reflection?',
        'options': [
            {'id': 'A', 'text': 'arcsin(2/3) ≈ 41.8°'},
            {'id': 'B', 'text': 'arcsin(1.5) (impossible)'},
            {'id': 'C', 'text': '45.0°'},
            {'id': 'D', 'text': '30.0°'}
        ],
        'correct_answer': 'A',
        'explanation': 'By Snell\'s law at critical angle: n_1 x sin(θ_c) = n_2 x sin(90°) => 1.5 x sin(θ_c) = 1.0 => sin(θ_c) = 1 / 1.5 = 2/3 => θ_c = arcsin(2/3) ≈ 41.8°.',
        'prerequisite_hint': 'Total internal reflection occurs only when traveling from a higher refractive index to a lower refractive index.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # =========================================================================
    # CHEMISTRY
    # =========================================================================
    # Bohr Model & Quantum Numbers (TOP-CHEM-01)
    {
        'topic_code': 'TOP-CHEM-01',
        'title': 'Quantum Numbers of 3d Subshell',
        'prompt': 'What are the principal quantum number (n) and azimuthal quantum number (l) for an electron occupying a 3d orbital?',
        'options': [
            {'id': 'A', 'text': 'n = 3, l = 2'},
            {'id': 'B', 'text': 'n = 3, l = 1'},
            {'id': 'C', 'text': 'n = 3, l = 3'},
            {'id': 'D', 'text': 'n = 2, l = 1'}
        ],
        'correct_answer': 'A',
        'explanation': 'The principal quantum number is the shell level (n = 3). The orbital angular momentum quantum number l corresponds to subshells: s (l=0), p (l=1), d (l=2), f (l=3). Hence for 3d, n = 3 and l = 2.',
        'prerequisite_hint': 'Review subshell notation: s=0, p=1, d=2, f=3.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CHEM-01',
        'title': 'De Broglie Wavelength',
        'prompt': 'According to de Broglie\'s hypothesis, what is the matter wavelength λ of a particle of mass m moving with velocity v?',
        'options': [
            {'id': 'A', 'text': 'λ = h / (m x v)'},
            {'id': 'B', 'text': 'λ = (m x v) / h'},
            {'id': 'C', 'text': 'λ = h x m x v'},
            {'id': 'D', 'text': 'λ = h / c'}
        ],
        'correct_answer': 'A',
        'explanation': 'De Broglie demonstrated wave-particle duality where momentum p = mv relates to wavelength via λ = h / p = h / (mv).',
        'prerequisite_hint': 'Recall Planck\'s constant relationship with linear momentum.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Periodic Properties & Bonding (TOP-CHEM-02)
    {
        'topic_code': 'TOP-CHEM-02',
        'title': 'First Ionization Enthalpy Trend',
        'prompt': 'Why is the first ionization enthalpy of Nitrogen (Z=7) higher than that of Oxygen (Z=8), despite Oxygen having a higher nuclear charge?',
        'options': [
            {'id': 'A', 'text': 'Nitrogen has a stable half-filled 2p^3 electronic configuration'},
            {'id': 'B', 'text': 'Oxygen has a smaller atomic radius'},
            {'id': 'C', 'text': 'Nitrogen has stronger shielding effect from 1s electrons'},
            {'id': 'D', 'text': 'Oxygen forms diatomic molecules while nitrogen does not'}
        ],
        'correct_answer': 'A',
        'explanation': 'Nitrogen has the valence configuration 2s^2 2p_x^1 2p_y^1 2p_z^1. The half-filled 2p subshell possesses extra exchange stabilization energy, requiring more energy to remove an electron compared to oxygen (2p^4), where paired electron repulsion eases ionization.',
        'prerequisite_hint': 'Review Hund\'s rule of maximum multiplicity and exchange energy of half-filled subshells.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # VSEPR & Hybridization (TOP-CHEM-03)
    {
        'topic_code': 'TOP-CHEM-03',
        'title': 'Molecular Geometry of SF4',
        'prompt': 'According to VSEPR theory, what is the molecular shape and hybridization of the central Sulfur atom in SF4?',
        'options': [
            {'id': 'A', 'text': 'See-saw shape with sp3d hybridization'},
            {'id': 'B', 'text': 'Square planar with sp3d2 hybridization'},
            {'id': 'C', 'text': 'Tetrahedral with sp3 hybridization'},
            {'id': 'D', 'text': 'Trigonal bipyramidal with sp3d hybridization'}
        ],
        'correct_answer': 'A',
        'explanation': 'Sulfur has 6 valence electrons. 4 bond pairs with fluorine leave 1 lone pair (steric number = 4 + 1 = 5, hence sp3d). To minimize 90° lone-pair repulsions, the lone pair occupies an equatorial position, giving a See-saw molecular geometry.',
        'prerequisite_hint': 'Steric number = bonded atoms + lone pairs on central atom.',
        'difficulty': 'HARD',
        'points': 20
    },
    {
        'topic_code': 'TOP-CHEM-03',
        'title': 'Hybridization in Ethyne (Acetylene)',
        'prompt': 'What is the hybridization and bond angle between Carbon atoms in ethyne (HC≡CH)?',
        'options': [
            {'id': 'A', 'text': 'sp hybridization with 180° bond angle'},
            {'id': 'B', 'text': 'sp2 hybridization with 120° bond angle'},
            {'id': 'C', 'text': 'sp3 hybridization with 109.5° bond angle'},
            {'id': 'D', 'text': 'dsp2 hybridization with 90° bond angle'}
        ],
        'correct_answer': 'A',
        'explanation': 'Each carbon in HC≡CH forms one σ-bond with Hydrogen and one σ-bond with the other Carbon (plus two unhybridized p-orbitals forming two π-bonds). Two electron domains result in linear geometry (180°) and sp hybridization.',
        'prerequisite_hint': 'Triple bonds consist of one sigma (σ) bond and two pi (π) bonds.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Thermodynamics & Gibbs Energy (TOP-CHEM-04)
    {
        'topic_code': 'TOP-CHEM-04',
        'title': 'Spontaneity and Gibbs Free Energy',
        'prompt': 'Under constant temperature and pressure, a chemical reaction is thermodynamically spontaneous at all temperatures when:',
        'options': [
            {'id': 'A', 'text': 'ΔH < 0 (exothermic) and ΔS > 0 (entropy increases)'},
            {'id': 'B', 'text': 'ΔH > 0 and ΔS < 0'},
            {'id': 'C', 'text': 'ΔH > 0 and ΔS > 0'},
            {'id': 'D', 'text': 'ΔH < 0 and ΔS < 0'}
        ],
        'correct_answer': 'A',
        'explanation': 'From the Gibbs-Helmholtz equation ΔG = ΔH - TΔS. If ΔH is negative and ΔS is positive, then -TΔS is always negative for any absolute temperature T > 0, ensuring ΔG < 0 (spontaneous) universally.',
        'prerequisite_hint': 'Review the criteria for spontaneity: a negative change in Gibbs free energy (ΔG < 0).',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Chemical Equilibrium & Le Chatelier (TOP-CHEM-05)
    {
        'topic_code': 'TOP-CHEM-05',
        'title': 'Le Chatelier Effect on Haber Process',
        'prompt': 'For the exothermic synthesis of ammonia N_2(g) + 3H_2(g) ⇌ 2NH_3(g) (ΔH = -92 kJ/mol), how will increasing pressure and decreasing temperature shift the equilibrium?',
        'options': [
            {'id': 'A', 'text': 'Both changes shift equilibrium forward toward NH_3'},
            {'id': 'B', 'text': 'Both changes shift equilibrium backward toward reactants'},
            {'id': 'C', 'text': 'Increasing pressure shifts forward, decreasing temperature shifts backward'},
            {'id': 'D', 'text': 'Neither change affects the equilibrium position'}
        ],
        'correct_answer': 'A',
        'explanation': 'Increasing pressure favors the side with fewer gas moles (4 moles on left vs 2 on right -> shifts forward). Since the reaction is exothermic, cooling removes heat and shifts equilibrium forward to generate more heat.',
        'prerequisite_hint': 'Le Chatelier\'s principle states that a system in equilibrium will shift to counteract any imposed disturbance.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Organic Chemistry Foundations (TOP-CHEM-06)
    {
        'topic_code': 'TOP-CHEM-06',
        'title': 'Markovnikov\'s Rule in Electrophilic Addition',
        'prompt': 'When propene (CH_3-CH=CH_2) reacts with dry HBr, what is the major product according to Markovnikov\'s rule?',
        'options': [
            {'id': 'A', 'text': '2-Bromopropane (CH3-CHBr-CH3)'},
            {'id': 'B', 'text': '1-Bromopropane (CH3-CH2-CH2Br)'},
            {'id': 'C', 'text': '1,2-Dibromopropane'},
            {'id': 'D', 'text': 'Propyl bromide'}
        ],
        'correct_answer': 'A',
        'explanation': 'Electrophilic attack by H+ creates the more stable secondary carbocation (CH3-CH+-CH3) rather than the primary carbocation. Bromide ion attacks this secondary carbocation, producing 2-bromopropane as the major product.',
        'prerequisite_hint': 'Carbocation stability order: 3° > 2° > 1° > methyl.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # =========================================================================
    # BIOLOGY
    # =========================================================================
    # Cell Organelles & Membrane (TOP-BIO-01)
    {
        'topic_code': 'TOP-BIO-01',
        'title': 'Fluid Mosaic Model of Cell Membrane',
        'prompt': 'In the Singer and Nicolson Fluid Mosaic Model of the plasma membrane, what is the primary structural bilayer component?',
        'options': [
            {'id': 'A', 'text': 'Amphipathic phospholipid bilayer with embedded integral/peripheral proteins'},
            {'id': 'B', 'text': 'Rigid cellulose matrix surrounded by lipoproteins'},
            {'id': 'C', 'text': 'Continuous protein sheet with interior lipid pores'},
            {'id': 'D', 'text': 'Cholesterol lattice bounded by oligosaccharides'}
        ],
        'correct_answer': 'A',
        'explanation': 'The plasma membrane consists of a quasi-fluid bilayer of amphipathic phospholipids whose hydrophobic tails face inward and hydrophilic heads face aqueous intra/extracellular environments, hosting embedded transport proteins.',
        'prerequisite_hint': 'Hydrophobic fatty acid chains face inward away from water.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-BIO-01',
        'title': 'Mitochondrial ATP Synthesis',
        'prompt': 'Across which mitochondrial structure is the proton electrochemical gradient established to drive ATP synthase?',
        'options': [
            {'id': 'A', 'text': 'Inner mitochondrial membrane (into the intermembrane space)'},
            {'id': 'B', 'text': 'Outer mitochondrial membrane'},
            {'id': 'C', 'text': 'Nuclear envelope pores'},
            {'id': 'D', 'text': 'Thylakoid stroma'}
        ],
        'correct_answer': 'A',
        'explanation': 'The electron transport chain complexes pump H+ protons from the mitochondrial matrix across the inner mitochondrial membrane into the intermembrane space, generating the proton motive force that drives ATP synthase.',
        'prerequisite_hint': 'Chemiosmotic hypothesis by Peter Mitchell.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Mitosis & Meiosis (TOP-BIO-02)
    {
        'topic_code': 'TOP-BIO-02',
        'title': 'Crossing Over in Meiosis',
        'prompt': 'During which specific stage of Prophase I of Meiosis does genetic crossing over (chiasma formation) occur between non-sister chromatids?',
        'options': [
            {'id': 'A', 'text': 'Pachytene'},
            {'id': 'B', 'text': 'Leptotene'},
            {'id': 'C', 'text': 'Zygotene'},
            {'id': 'D', 'text': 'Diakinesis'}
        ],
        'correct_answer': 'A',
        'explanation': 'Prophase I stages: Leptotene (chromatin condenses), Zygotene (synapsis and synaptonemal complex), Pachytene (crossing over mediated by recombinase), Diplotene (chiasmata visible), Diakinesis (terminalization).',
        'prerequisite_hint': 'Remember the sequence: Leptotene -> Zygotene -> Pachytene -> Diplotene -> Diakinesis.',
        'difficulty': 'HARD',
        'points': 20
    },

    # Mendelian Genetics (TOP-BIO-03)
    {
        'topic_code': 'TOP-BIO-03',
        'title': 'Dihybrid Cross Phenotypic Ratio',
        'prompt': 'What is the classic Mendelian phenotypic ratio in the F2 generation of a dihybrid cross involving two independent, unlinked heterozygous traits (e.g., RrYy x RrYy)?',
        'options': [
            {'id': 'A', 'text': '9 : 3 : 3 : 1'},
            {'id': 'B', 'text': '1 : 2 : 1'},
            {'id': 'C', 'text': '3 : 1'},
            {'id': 'D', 'text': '9 : 7'}
        ],
        'correct_answer': 'A',
        'explanation': 'Mendel\'s law of independent assortment dictates that two independent heterozygous pairs yield 9 (dominant for both) : 3 (dominant A, recessive B) : 3 (recessive A, dominant B) : 1 (recessive for both).',
        'prerequisite_hint': 'Combine two independent 3:1 monohybrid cross ratios: (3:1) x (3:1) = 9:3:3:1.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-BIO-03',
        'title': 'Incomplete Dominance in Snapdragon',
        'prompt': 'In snapdragon plants (Antirrhinum majus), flower color exhibits incomplete dominance. When a red flower (RR) is crossed with a white flower (rr), what are the phenotypic results of self-pollinating the F1 generation (Rr)?',
        'options': [
            {'id': 'A', 'text': '1 Red : 2 Pink : 1 White'},
            {'id': 'B', 'text': '3 Red : 1 White'},
            {'id': 'C', 'text': 'All Pink flowers'},
            {'id': 'D', 'text': '3 Pink : 1 Red'}
        ],
        'correct_answer': 'A',
        'explanation': 'In incomplete dominance, the heterozygous genotype produces an intermediate phenotype (Pink). Self-pollinating Rr x Rr produces 1 RR (Red) : 2 Rr (Pink) : 1 rr (White), where genotypic and phenotypic ratios coincide as 1:2:1.',
        'prerequisite_hint': 'Neither allele is completely dominant over the other.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # DNA Replication & Central Dogma (TOP-BIO-04)
    {
        'topic_code': 'TOP-BIO-04',
        'title': 'Leading vs Lagging Strand Synthesis',
        'prompt': 'Why is the lagging strand in eukaryotic DNA replication synthesized discontinuously as Okazaki fragments?',
        'options': [
            {'id': 'A', 'text': 'DNA polymerase can only catalyze nucleotide addition in the 5\' to 3\' direction'},
            {'id': 'B', 'text': 'Helicase unwinds DNA only intermittently'},
            {'id': 'C', 'text': 'RNA primers are not recognized on the lagging strand'},
            {'id': 'D', 'text': 'Topoisomerase blocks continuous polymerization on both strands'}
        ],
        'correct_answer': 'A',
        'explanation': 'Because DNA double helices are antiparallel and DNA polymerase requires a free 3\'-OH group (synthesizing strictly in the 5\' -> 3\' direction), the strand replicating away from the replication fork must be synthesized in short discontinuous segments known as Okazaki fragments.',
        'prerequisite_hint': 'Check the direction of catalytic addition of deoxynucleotides by DNA Polymerase.',
        'difficulty': 'HARD',
        'points': 20
    },

    # Photosynthesis & Calvin Cycle (TOP-BIO-05)
    {
        'topic_code': 'TOP-BIO-05',
        'title': 'Primary Carbon Dioxide Acceptor in C3 Plants',
        'prompt': 'What is the primary CO_2 acceptor molecule in the stroma during the carboxylation phase of the Calvin cycle in C3 plants?',
        'options': [
            {'id': 'A', 'text': 'Ribulose-1,5-bisphosphate (RuBP)'},
            {'id': 'B', 'text': 'Phosphoenolpyruvate (PEP)'},
            {'id': 'C', 'text': 'Oxaloacetic acid (OAA)'},
            {'id': 'D', 'text': '3-phosphoglycerate (3-PGA)'}
        ],
        'correct_answer': 'A',
        'explanation': 'The enzyme RuBisCO catalyzes the addition of CO_2 to the 5-carbon sugar Ribulose-1,5-bisphosphate (RuBP), forming an unstable 6-carbon intermediate that immediately cleaves into two molecules of 3-PGA.',
        'prerequisite_hint': 'RuBisCO stands for Ribulose-1,5-bisphosphate carboxylase-oxygenase.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Human Circulatory System (TOP-BIO-06)
    {
        'topic_code': 'TOP-BIO-06',
        'title': 'Natural Pacemaker of the Human Heart',
        'prompt': 'Which specialized nodal tissue in the human heart initiates spontaneous rhythmic action potentials and is designated the primary cardiac pacemaker?',
        'options': [
            {'id': 'A', 'text': 'Sinoatrial (SA) Node'},
            {'id': 'B', 'text': 'Atrioventricular (AV) Node'},
            {'id': 'C', 'text': 'Bundle of His'},
            {'id': 'D', 'text': 'Purkinje Fibers'}
        ],
        'correct_answer': 'A',
        'explanation': 'The SA node, located in the right upper wall of the right atrium, exhibits the highest inherent rate of autorhythmicity (70-75 action potentials/min) and depolarizes the atria first.',
        'prerequisite_hint': 'Trace the electrical conduction path: SA node -> AV node -> Bundle of His -> Purkinje fibers.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Ecosystem Dynamics (TOP-BIO-07)
    {
        'topic_code': 'TOP-BIO-07',
        'title': 'Lindeman\'s 10% Energy Transfer Law',
        'prompt': 'According to Lindeman\'s 10% law of trophic efficiency, if primary producers synthesize 10,000 kJ of net energy, how much energy is typically transferred to tertiary consumers?',
        'options': [
            {'id': 'A', 'text': '10 kJ'},
            {'id': 'B', 'text': '100 kJ'},
            {'id': 'C', 'text': '1,000 kJ'},
            {'id': 'D', 'text': '1 kJ'}
        ],
        'correct_answer': 'A',
        'explanation': 'Producers = 10,000 kJ. Primary consumers receive 10% = 1,000 kJ. Secondary consumers receive 10% = 100 kJ. Tertiary consumers receive 10% = 10 kJ.',
        'prerequisite_hint': 'Each successive trophic level retains approximately 10% of energy.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Probability & Statistics (TOP-STAT-01)
    {
        'topic_code': 'TOP-STAT-01',
        'title': 'Bayes Theorem Conditional Probability',
        'prompt': 'A medical screening test for a rare condition (prevalence 1%) has a sensitivity of 95% and false positive rate of 5%. If a random patient tests positive, what is the approximate probability they actually have the condition?',
        'options': [
            {'id': 'A', 'text': 'Approximately 16%'},
            {'id': 'B', 'text': '95%'},
            {'id': 'C', 'text': '50%'},
            {'id': 'D', 'text': '5%'}
        ],
        'correct_answer': 'A',
        'explanation': 'P(Condition|+) = P(+|Condition)P(Condition) / [P(+|Condition)P(Condition) + P(+|No Condition)P(No Condition)] = (0.95 x 0.01) / [(0.95 x 0.01) + (0.05 x 0.99)] = 0.0095 / (0.0095 + 0.0495) ≈ 0.161 (16.1%).',
        'prerequisite_hint': 'Review Bayes Theorem formula: P(A|B) = [P(B|A) x P(A)] / P(B).',
        'difficulty': 'HARD',
        'points': 20
    },
    {
        'topic_code': 'TOP-STAT-01',
        'title': 'Binomial Distribution Variance',
        'prompt': 'For a binomial distribution with n independent trials and success probability p, what is the variance?',
        'options': [
            {'id': 'A', 'text': 'n x p x (1 - p)'},
            {'id': 'B', 'text': 'n x p'},
            {'id': 'C', 'text': '√(n x p)'},
            {'id': 'D', 'text': 'n x p^2'}
        ],
        'correct_answer': 'A',
        'explanation': 'For a binomial random variable X ~ B(n, p), mean μ = np and variance Var(X) = np(1 - p) = npq.',
        'prerequisite_hint': 'Recall the variance of a single Bernoulli trial is p(1-p).',
        'difficulty': 'EASY',
        'points': 10
    },

    # Planetary Motion (TOP-PHYS-04)
    {
        'topic_code': 'TOP-PHYS-04',
        'title': 'Kepler\'s Third Law of Planetary Motion',
        'prompt': 'Kepler\'s Third Law of planetary motion states that the square of orbital period T is proportional to which power of the semi-major axis a?',
        'options': [
            {'id': 'A', 'text': 'T^2 ∝ a^3'},
            {'id': 'B', 'text': 'T^2 ∝ a^2'},
            {'id': 'C', 'text': 'T ∝ a^3'},
            {'id': 'D', 'text': 'T^3 ∝ a^2'}
        ],
        'correct_answer': 'A',
        'explanation': 'By equating centripetal force to gravitational force: m x (4π^2 r / T^2) = GMm / r^2 => T^2 = (4π^2 / GM) x r^3, hence T^2 ∝ a^3.',
        'prerequisite_hint': 'Equate gravitational force to centripetal acceleration: GMm/r^2 = mv^2/r.',
        'difficulty': 'EASY',
        'points': 10
    },

    # Electrochemistry (TOP-CHEM-07)
    {
        'topic_code': 'TOP-CHEM-07',
        'title': 'Nernst Equation at 298 K',
        'prompt': 'What is the standard form of the Nernst equation for an electrochemical cell at 25°C (298 K)?',
        'options': [
            {'id': 'A', 'text': 'E_cell = E°_cell - (0.0591 / n) x log_10(Q)'},
            {'id': 'B', 'text': 'E_cell = E°_cell + (0.0591 x n) x log_10(Q)'},
            {'id': 'C', 'text': 'E_cell = E°_cell - (RT / n) x log_10(Q)'},
            {'id': 'D', 'text': 'E_cell = E°_cell / Q'}
        ],
        'correct_answer': 'A',
        'explanation': 'At 298 K, (2.303 x R x T) / F evaluates to approximately 0.05916 V, giving E_cell = E°_cell - (0.0591 / n) x log_10(Q).',
        'prerequisite_hint': 'Recall the relationship between cell potential and standard free energy: ΔG = -nFE.',
        'difficulty': 'MEDIUM',
        'points': 15
    },

    # Transcription & RNA (TOP-BIO-04)
    {
        'topic_code': 'TOP-BIO-04',
        'title': 'RNA Transcription Direction',
        'prompt': 'During gene transcription in eukaryotes, RNA Polymerase reads the template DNA strand in which direction, and synthesizes mRNA in which direction?',
        'options': [
            {'id': 'A', 'text': 'Reads template 3\' to 5\', synthesizes mRNA 5\' to 3\''},
            {'id': 'B', 'text': 'Reads template 5\' to 3\', synthesizes mRNA 3\' to 5\''},
            {'id': 'C', 'text': 'Synthesizes both strands bidirectionally'},
            {'id': 'D', 'text': 'Reads template 5\' to 3\', synthesizes mRNA 5\' to 3\''}
        ],
        'correct_answer': 'A',
        'explanation': 'Like all nucleic acid polymerases, RNA polymerase synthesizes RNA 5\' to 3\'. Because nucleic acids hybridize antiparallel, it must traverse the DNA template strand in the 3\' to 5\' direction.',
        'prerequisite_hint': 'All nucleic acids grow at the 3\'-hydroxyl terminus.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Cross Product of Standard Unit Vectors',
        'prompt': 'What is the value of i x (j x k) + j x (k x i) + k x (i x j)?',
        'options': [{'id': 'A', 'text': '0 (zero vector)'}, {'id': 'B', 'text': 'i + j + k'}, {'id': 'C', 'text': '3(i + j + k)'}, {'id': 'D', 'text': '-1'}],
        'correct_answer': 'A',
        'explanation': 'Since j x k = i, k x i = j, and i x j = k, the expression becomes i x i + j x j + k x k. The cross product of any vector with itself is 0, so the sum is the zero vector.',
        'prerequisite_hint': 'The cross product of parallel or identical vectors is zero: v x v = 0.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Area of Triangle Using Cross Product',
        'prompt': 'Find the area of a triangle having adjacent sides given by vectors a = 3i + 4j and b = -5i + 7j.',
        'options': [{'id': 'A', 'text': '20.5 square units'}, {'id': 'B', 'text': '41 square units'}, {'id': 'C', 'text': '18.5 square units'}, {'id': 'D', 'text': '25 square units'}],
        'correct_answer': 'A',
        'explanation': 'Area of a triangle with adjacent vectors a and b is (1/2)|a x b|. a x b = (3)(7) - (4)(-5) k = (21 + 20)k = 41k. Magnitude is 41, so area = 41/2 = 20.5 square units.',
        'prerequisite_hint': 'Area of a triangle with vector sides is half the magnitude of their cross product.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Coplanar Vectors Condition',
        'prompt': 'Find the value of lambda for which the three vectors a = i - j + k, b = 2i + j - k, and c = lambda i - j + lambda k are coplanar.',
        'options': [{'id': 'A', 'text': 'lambda = 1'}, {'id': 'B', 'text': 'lambda = 0'}, {'id': 'C', 'text': 'lambda = -2'}, {'id': 'D', 'text': 'lambda = 3'}],
        'correct_answer': 'A',
        'explanation': 'Three vectors are coplanar if their scalar triple product is 0. Setting the 3x3 determinant of [1, -1, 1], [2, 1, -1], [lambda, -1, lambda] to zero gives 1(lambda - 1) - (-1)(2lambda - (-lambda)) + 1(-2 - lambda) = 0, which solves to lambda = 1.',
        'prerequisite_hint': 'Three vectors are coplanar if and only if their scalar triple product [a b c] = 0.',
        'difficulty': 'HARD',
        'points': 20
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Perpendicular Vector Construction',
        'prompt': 'Find a vector of magnitude 9 that is perpendicular to both a = 4i - j + 3k and b = -2i + j - 2k.',
        'options': [{'id': 'A', 'text': '-3i + 6j + 6k'}, {'id': 'B', 'text': '3i - 6j + 2k'}, {'id': 'C', 'text': '-i + 2j + 2k'}, {'id': 'D', 'text': '6i - 3j + 6k'}],
        'correct_answer': 'A',
        'explanation': 'Cross product a x b = (-1)(-2) - (3)(1) i - (4(-2) - 3(-2)) j + (4(1) - (-1)(-2)) k = -i + 2j + 2k. Magnitude is sqrt(1 + 4 + 4) = 3. Unit vector is (-i + 2j + 2k)/3. Scaling by magnitude 9 gives 9(-i + 2j + 2k)/3 = -3i + 6j + 6k.',
        'prerequisite_hint': 'A vector perpendicular to both a and b is parallel to their cross product a x b.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Direction Ratios of a Vector',
        'prompt': 'If a vector has initial point P(2, 1, -1) and terminal point Q(4, 4, 5), what are its direction ratios?',
        'options': [{'id': 'A', 'text': '2, 3, 6'}, {'id': 'B', 'text': '6, 5, 4'}, {'id': 'C', 'text': '2, -3, 6'}, {'id': 'D', 'text': '1, 1, 3'}],
        'correct_answer': 'A',
        'explanation': 'Direction ratios of vector PQ are (x2 - x1), (y2 - y1), (z2 - z1) = (4 - 2), (4 - 1), (5 - (-1)) = 2, 3, 6.',
        'prerequisite_hint': 'Component difference gives the direction ratios: Delta x, Delta y, Delta z.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Distance from Point to a Plane',
        'prompt': 'Find the perpendicular distance from the origin (0,0,0) to the plane 2x - 3y + 6z + 14 = 0.',
        'options': [{'id': 'A', 'text': '2 units'}, {'id': 'B', 'text': '7 units'}, {'id': 'C', 'text': '14 units'}, {'id': 'D', 'text': '1 unit'}],
        'correct_answer': 'A',
        'explanation': 'Perpendicular distance d = |ax0 + by0 + cz0 + d| / sqrt(a^2 + b^2 + c^2). For origin, d = |14| / sqrt(4 + 9 + 36) = 14 / sqrt(49) = 14 / 7 = 2 units.',
        'prerequisite_hint': 'Distance formula from point (x0, y0, z0) to plane ax + by + cz + d = 0 is |ax0 + by0 + cz0 + d| / sqrt(a^2 + b^2 + c^2).',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Angle Between Two Planes',
        'prompt': 'What is the angle between the planes 2x - y + z = 6 and x + y + 2z = 3?',
        'options': [{'id': 'A', 'text': '60 degrees'}, {'id': 'B', 'text': '45 degrees'}, {'id': 'C', 'text': '90 degrees'}, {'id': 'D', 'text': '30 degrees'}],
        'correct_answer': 'A',
        'explanation': 'Normal vectors are n1 = (2, -1, 1) and n2 = (1, 1, 2). cos(theta) = |n1 . n2| / (|n1| |n2|) = |2(1) - 1(1) + 1(2)| / (sqrt(6) sqrt(6)) = 3 / 6 = 1/2. Therefore theta = 60 degrees.',
        'prerequisite_hint': 'The angle between two planes equals the angle between their normal vectors.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Vector Equation of a Line',
        'prompt': 'Find the Cartesian equation of a line passing through (1, 2, -4) and parallel to vector 2i + 3j + 6k.',
        'options': [{'id': 'A', 'text': '(x - 1)/2 = (y - 2)/3 = (z + 4)/6'}, {'id': 'B', 'text': '(x + 1)/2 = (y + 2)/3 = (z - 4)/6'}, {'id': 'C', 'text': '(x - 2)/1 = (y - 3)/2 = (z - 6)/(-4)'}, {'id': 'D', 'text': '2x + 3y + 6z = 0'}],
        'correct_answer': 'A',
        'explanation': 'The line passing through (x1, y1, z1) with direction ratios (a, b, c) has equation (x - x1)/a = (y - y1)/b = (z - z1)/c. Substituting gives (x - 1)/2 = (y - 2)/3 = (z + 4)/6.',
        'prerequisite_hint': 'Standard symmetric form of a 3D line is (x - x1)/a = (y - y1)/b = (z - z1)/c.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Shortest Distance Between Parallel Lines',
        'prompt': 'What is the condition for two lines r = a1 + lambda b and r = a2 + mu b to be parallel?',
        'options': [{'id': 'A', 'text': 'Their direction vectors are scalar multiples of the same vector b'}, {'id': 'B', 'text': 'Their dot product a1 . a2 = 0'}, {'id': 'C', 'text': 'a1 x a2 = b'}, {'id': 'D', 'text': 'Their points must lie on the same plane only'}],
        'correct_answer': 'A',
        'explanation': 'Two lines in 3D are parallel if their direction vectors are proportional (collinear), meaning both share the direction vector b or a scalar multiple thereof.',
        'prerequisite_hint': 'Parallel lines share identical or proportional direction vectors.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Linear Combination of Vectors',
        'prompt': 'If vector r = 2a + 3b - c where a, b, c are mutually orthogonal unit vectors, find the magnitude |r|.',
        'options': [{'id': 'A', 'text': 'sqrt(14)'}, {'id': 'B', 'text': '14'}, {'id': 'C', 'text': '4'}, {'id': 'D', 'text': 'sqrt(12)'}],
        'correct_answer': 'A',
        'explanation': 'For mutually orthogonal unit vectors, |r|^2 = (2)^2 + (3)^2 + (-1)^2 = 4 + 9 + 1 = 14. Therefore |r| = sqrt(14).',
        'prerequisite_hint': 'For orthonormal basis vectors, cross terms vanish in the dot product.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Vector Projection Scalar vs Vector',
        'prompt': 'The vector component of vector a along vector b is given by which formula?',
        'options': [{'id': 'A', 'text': '((a . b) / |b|^2) b'}, {'id': 'B', 'text': '((a . b) / |b|) b'}, {'id': 'C', 'text': '(a x b) / |b|'}, {'id': 'D', 'text': '(a . b) / |a|'}],
        'correct_answer': 'A',
        'explanation': 'The scalar projection is (a . b)/|b|. Multiplying by the unit vector b/|b| gives the vector projection: ((a . b) / |b|^2) b.',
        'prerequisite_hint': 'Vector projection equals scalar projection multiplied by the unit vector in direction of b.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Direction Angles of a Vector',
        'prompt': 'Can a line in 3D space make angles 45, 60, and 120 degrees with the coordinate axes?',
        'options': [{'id': 'A', 'text': 'Yes, because cos^2(45) + cos^2(60) + cos^2(120) = 1/2 + 1/4 + 1/4 = 1'}, {'id': 'B', 'text': 'No, because the angles must sum to 180 degrees'}, {'id': 'C', 'text': 'No, angles cannot exceed 90 degrees'}, {'id': 'D', 'text': 'Yes, because 45 + 60 + 120 = 225 is valid'}],
        'correct_answer': 'A',
        'explanation': 'Valid direction angles alpha, beta, gamma must satisfy cos^2(alpha) + cos^2(beta) + cos^2(gamma) = 1. Here (1/sqrt(2))^2 + (1/2)^2 + (-1/2)^2 = 1/2 + 1/4 + 1/4 = 1. Thus it is valid.',
        'prerequisite_hint': 'Direction cosines must satisfy l^2 + m^2 + n^2 = 1.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Cross Product Non-Commutativity',
        'prompt': 'If a x b = c, what is the value of b x a?',
        'options': [{'id': 'A', 'text': '-c'}, {'id': 'B', 'text': 'c'}, {'id': 'C', 'text': '1/c'}, {'id': 'D', 'text': '0'}],
        'correct_answer': 'A',
        'explanation': 'The cross product is anti-commutative: b x a = -(a x b). Therefore b x a = -c.',
        'prerequisite_hint': 'Reversing the order of vectors in a cross product flips the direction by 180 degrees.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Area of a Parallelogram',
        'prompt': 'Find the area of a parallelogram whose adjacent sides are given by a = i + 2j + 3k and b = 3i - 2j + k.',
        'options': [{'id': 'A', 'text': '8 sqrt(3) square units'}, {'id': 'B', 'text': '4 sqrt(3) square units'}, {'id': 'C', 'text': '12 square units'}, {'id': 'D', 'text': '16 square units'}],
        'correct_answer': 'A',
        'explanation': 'Area = |a x b|. a x b = (2(1) - 3(-2))i - (1(1) - 3(3))j + (1(-2) - 2(3))k = 8i + 8j - 8k. |a x b| = sqrt(64 + 64 + 64) = sqrt(192) = 8 sqrt(3) square units.',
        'prerequisite_hint': 'Area of parallelogram equals the magnitude of the cross product of its adjacent sides.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-02',
        'title': 'Scalar Product with Sum of Vectors',
        'prompt': 'If |a| = 3, |b| = 4, and |c| = 5, and each vector is perpendicular to the sum of the other two, find |a + b + c|.',
        'options': [{'id': 'A', 'text': '5 sqrt(2)'}, {'id': 'B', 'text': '12'}, {'id': 'C', 'text': '10'}, {'id': 'D', 'text': 'sqrt(50)'}],
        'correct_answer': 'A',
        'explanation': 'Given a . (b + c) = 0, b . (c + a) = 0, and c . (a + b) = 0. Adding these gives 2(a.b + b.c + c.a) = 0. Then |a + b + c|^2 = |a|^2 + |b|^2 + |c|^2 + 0 = 9 + 16 + 25 = 50. Thus |a + b + c| = sqrt(50) = 5 sqrt(2).',
        'prerequisite_hint': 'Expand |a + b + c|^2 = |a|^2 + |b|^2 + |c|^2 + 2(a.b + b.c + c.a).',
        'difficulty': 'HARD',
        'points': 20
    },
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Derivative of Composite Logarithmic Function',
        'prompt': 'Find dy/dx if y = ln(sec x + tan x).',
        'options': [{'id': 'A', 'text': 'sec x'}, {'id': 'B', 'text': 'tan x'}, {'id': 'C', 'text': 'sec x tan x'}, {'id': 'D', 'text': 'sec^2 x'}],
        'correct_answer': 'A',
        'explanation': 'By chain rule, dy/dx = (sec x tan x + sec^2 x) / (sec x + tan x) = sec x (tan x + sec x) / (sec x + tan x) = sec x.',
        'prerequisite_hint': 'Apply chain rule: d/dx(ln u) = (1/u) x du/dx.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Derivative of Inverse Trigonometric Function',
        'prompt': 'Find the derivative of y = arctan((2x) / (1 - x^2)) with respect to x.',
        'options': [{'id': 'A', 'text': '2 / (1 + x^2)'}, {'id': 'B', 'text': '1 / (1 + x^2)'}, {'id': 'C', 'text': '4x / (1 + x^2)'}, {'id': 'D', 'text': '2 / (1 - x^2)'}],
        'correct_answer': 'A',
        'explanation': 'Substitute x = tan(theta), then (2x)/(1-x^2) = tan(2theta). Thus y = arctan(tan(2theta)) = 2theta = 2 arctan(x). Differentiating yields 2 / (1 + x^2).',
        'prerequisite_hint': 'Use trigonometric substitution: 2 tan(theta) / (1 - tan^2(theta)) = tan(2 theta).',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Implicit Differentiation of Circle',
        'prompt': 'Find dy/dx for the curve x^2 + y^2 = 25 at the point (3, 4).',
        'options': [{'id': 'A', 'text': '-3/4'}, {'id': 'B', 'text': '3/4'}, {'id': 'C', 'text': '-4/3'}, {'id': 'D', 'text': '4/3'}],
        'correct_answer': 'A',
        'explanation': 'Differentiating both sides: 2x + 2y (dy/dx) = 0, so dy/dx = -x/y. At (3, 4), dy/dx = -3/4.',
        'prerequisite_hint': 'Remember d/dx(y^2) = 2y dy/dx using chain rule.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Definite Integral of Odd Function',
        'prompt': 'Evaluate the definite integral from -pi to pi of x^3 x cos(x) dx.',
        'options': [{'id': 'A', 'text': '0'}, {'id': 'B', 'text': '2 pi'}, {'id': 'C', 'text': 'pi^2'}, {'id': 'D', 'text': '1'}],
        'correct_answer': 'A',
        'explanation': 'f(-x) = (-x)^3 cos(-x) = -x^3 cos(x) = -f(x), so the integrand is an odd function. The definite integral of an odd function over symmetric limits [-a, a] is strictly 0.',
        'prerequisite_hint': 'Integral of an odd function over [-a, a] is zero.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Integral Using Partial Fractions',
        'prompt': 'Evaluate the indefinite integral: integral of 1 / (x^2 - 9) dx.',
        'options': [{'id': 'A', 'text': '(1/6) ln|(x - 3) / (x + 3)| + C'}, {'id': 'B', 'text': '(1/3) ln|x - 3| + C'}, {'id': 'C', 'text': '(1/6) ln|(x + 3) / (x - 3)| + C'}, {'id': 'D', 'text': 'arctan(x/3) + C'}],
        'correct_answer': 'A',
        'explanation': 'Decompose 1 / ((x-3)(x+3)) = (1/6)[1/(x-3) - 1/(x+3)]. Integrating yields (1/6) [ln|x-3| - ln|x+3|] = (1/6) ln|(x-3)/(x+3)| + C.',
        'prerequisite_hint': 'Standard formula: integral of 1/(x^2 - a^2) dx = (1/(2a)) ln|(x - a)/(x + a)| + C.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Trigonometric Integral Substitution',
        'prompt': 'Evaluate the integral of tan^3(x) x sec^2(x) dx.',
        'options': [{'id': 'A', 'text': '(1/4) tan^4(x) + C'}, {'id': 'B', 'text': '(1/3) tan^3(x) + C'}, {'id': 'C', 'text': '(1/2) sec^2(x) + C'}, {'id': 'D', 'text': 'tan^2(x) + C'}],
        'correct_answer': 'A',
        'explanation': 'Substitute u = tan(x), so du = sec^2(x) dx. The integral becomes integral of u^3 du = (u^4)/4 + C = (1/4) tan^4(x) + C.',
        'prerequisite_hint': 'Notice sec^2(x) is the exact derivative of tan(x).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Integration by Parts with Algebraic and Trig',
        'prompt': 'Evaluate the integral of x^2 x cos(x) dx.',
        'options': [{'id': 'A', 'text': 'x^2 sin(x) + 2x cos(x) - 2 sin(x) + C'}, {'id': 'B', 'text': 'x^2 sin(x) - 2x cos(x) + 2 sin(x) + C'}, {'id': 'C', 'text': 'x^3 sin(x) / 3 + C'}, {'id': 'D', 'text': '-x^2 sin(x) + 2x cos(x) + C'}],
        'correct_answer': 'A',
        'explanation': 'Integrate by parts twice: let u = x^2, dv = cos(x)dx => v = sin(x). First step: x^2 sin(x) - 2 integral of x sin(x)dx. Second step: integral of x sin(x)dx = -x cos(x) + sin(x). Combining: x^2 sin(x) + 2x cos(x) - 2 sin(x) + C.',
        'prerequisite_hint': 'Apply Tabular Integration or repeat integration by parts until polynomial degree reaches 0.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Definite Integral of e^(x) x (1/x - 1/x^2)',
        'prompt': 'Evaluate integral of e^x x (1/x - 1/x^2) dx.',
        'options': [{'id': 'A', 'text': '(e^x) / x + C'}, {'id': 'B', 'text': 'e^x x ln(x) + C'}, {'id': 'C', 'text': '-e^x / x^2 + C'}, {'id': 'D', 'text': 'e^x / x^2 + C'}],
        'correct_answer': 'A',
        'explanation': 'Using the standard theorem integral of e^x [f(x) + f prime(x)] dx = e^x f(x) + C. Here f(x) = 1/x, and f prime(x) = -1/x^2. Hence the integral is (e^x)/x + C.',
        'prerequisite_hint': 'Recognize the identity integral of e^x [f(x) + f prime(x)] dx = e^x f(x) + C.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-03',
        'title': 'Integral of arctan(x)',
        'prompt': 'Evaluate the integral of arctan(x) dx.',
        'options': [{'id': 'A', 'text': 'x arctan(x) - (1/2) ln(1 + x^2) + C'}, {'id': 'B', 'text': 'x arctan(x) + (1/2) ln(1 + x^2) + C'}, {'id': 'C', 'text': '1 / (1 + x^2) + C'}, {'id': 'D', 'text': 'x / (1 + x^2) + C'}],
        'correct_answer': 'A',
        'explanation': 'Let u = arctan(x) => du = 1/(1+x^2) dx, dv = dx => v = x. integral of u dv = x arctan(x) - integral of x / (1 + x^2) dx = x arctan(x) - (1/2) ln(1 + x^2) + C.',
        'prerequisite_hint': 'When integrating inverse functions, set dv = dx.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Limit of a Definite Integral as Sum',
        'prompt': 'Evaluate the limit as n approaches infinity of (1/n) x sum from r=1 to n of (r/n)^2.',
        'options': [{'id': 'A', 'text': '1/3'}, {'id': 'B', 'text': '1/2'}, {'id': 'C', 'text': '1/4'}, {'id': 'D', 'text': '1'}],
        'correct_answer': 'A',
        'explanation': 'This Riemann sum converts to the definite integral from 0 to 1 of x^2 dx = [x^3 / 3] from 0 to 1 = 1/3.',
        'prerequisite_hint': 'Convert Riemann sum to definite integral: replace r/n by x and 1/n by dx.',
        'difficulty': 'HARD',
        'points': 20
    },
    {
        'topic_code': 'TOP-CALC-01',
        'title': 'Second Order Derivative',
        'prompt': 'If y = A sin(omega t) + B cos(omega t), what is d^2y/dt^2?',
        'options': [{'id': 'A', 'text': '-omega^2 x y'}, {'id': 'B', 'text': 'omega^2 x y'}, {'id': 'C', 'text': '-omega x y'}, {'id': 'D', 'text': '0'}],
        'correct_answer': 'A',
        'explanation': 'dy/dt = A omega cos(omega t) - B omega sin(omega t). d^2y/dt^2 = -A omega^2 sin(omega t) - B omega^2 cos(omega t) = -omega^2 y.',
        'prerequisite_hint': 'Differentiating sine and cosine twice introduces a negative sign and squared frequency.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CALC-02',
        'title': 'Area Under Parabola',
        'prompt': 'Find the area enclosed by the parabola y = 4x - x^2 and the x-axis.',
        'options': [{'id': 'A', 'text': '32/3 square units'}, {'id': 'B', 'text': '16/3 square units'}, {'id': 'C', 'text': '8 square units'}, {'id': 'D', 'text': '12 square units'}],
        'correct_answer': 'A',
        'explanation': 'x-intercepts are at x = 0 and x = 4. Area = integral from 0 to 4 of (4x - x^2) dx = [2x^2 - x^3 / 3] from 0 to 4 = 2(16) - 64/3 = 32 - 64/3 = 32/3 square units.',
        'prerequisite_hint': 'Find x-intercepts by solving y = 0 to establish integration limits.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Inverse of a 2x2 Matrix',
        'prompt': 'What is the inverse of matrix A = [[2, 3], [1, 2]]?',
        'options': [{'id': 'A', 'text': '[[2, -3], [-1, 2]]'}, {'id': 'B', 'text': '[[-2, 3], [1, -2]]'}, {'id': 'C', 'text': '[[2, 1], [3, 2]]'}, {'id': 'D', 'text': '[[1, 0], [0, 1]]'}],
        'correct_answer': 'A',
        'explanation': 'det(A) = 2(2) - 3(1) = 4 - 3 = 1. A^(-1) = (1/det(A)) x [[d, -b], [-c, a]] = [[2, -3], [-1, 2]].',
        'prerequisite_hint': 'For [[a, b], [c, d]], inverse is (1/(ad - bc)) [[d, -b], [-c, a]].',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Determinant of Scalar Multiplied Matrix',
        'prompt': 'If A is a 3x3 matrix with det(A) = 5, what is det(2A)?',
        'options': [{'id': 'A', 'text': '40'}, {'id': 'B', 'text': '10'}, {'id': 'C', 'text': '30'}, {'id': 'D', 'text': '125'}],
        'correct_answer': 'A',
        'explanation': 'For an n x n matrix, det(k A) = k^n x det(A). For n = 3 and k = 2: det(2A) = 2^3 x det(A) = 8 x 5 = 40.',
        'prerequisite_hint': 'Multiplying an n x n matrix by scalar k scales its determinant by k^n.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Symmetric and Skew-Symmetric Matrices',
        'prompt': 'If A is any square matrix, which of the following expressions is always skew-symmetric?',
        'options': [{'id': 'A', 'text': 'A - A^T'}, {'id': 'B', 'text': 'A + A^T'}, {'id': 'C', 'text': 'A x A^T'}, {'id': 'D', 'text': 'A^2'}],
        'correct_answer': 'A',
        'explanation': 'Let B = A - A^T. Then B^T = (A - A^T)^T = A^T - A = -(A - A^T) = -B. Since B^T = -B, it is always skew-symmetric.',
        'prerequisite_hint': 'A matrix B is skew-symmetric if B^T = -B.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-01',
        'title': 'Projectile Motion Maximum Height',
        'prompt': 'A ball is launched with initial velocity u at angle 30 degrees to the horizontal. What is its maximum height H?',
        'options': [{'id': 'A', 'text': 'u^2 / (8g)'}, {'id': 'B', 'text': 'u^2 / (4g)'}, {'id': 'C', 'text': 'u^2 / (2g)'}, {'id': 'D', 'text': '3 u^2 / (8g)'}],
        'correct_answer': 'A',
        'explanation': 'H = (u^2 sin^2 theta) / (2g). Since sin(30) = 1/2, sin^2(30) = 1/4. H = (u^2 x 1/4) / (2g) = u^2 / (8g).',
        'prerequisite_hint': 'Formula for maximum height in projectile motion: H = (u^2 sin^2 theta) / (2g).',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-PHYS-02',
        'title': 'Frictional Force on Inclined Plane',
        'prompt': 'A block of mass m rests on an incline of angle theta. What is the minimum coefficient of static friction mu_s required to prevent it from sliding?',
        'options': [{'id': 'A', 'text': 'tan(theta)'}, {'id': 'B', 'text': 'sin(theta)'}, {'id': 'C', 'text': 'cos(theta)'}, {'id': 'D', 'text': 'cot(theta)'}],
        'correct_answer': 'A',
        'explanation': 'At impending slip, the downward force mg sin(theta) equals maximum static friction mu_s N = mu_s mg cos(theta). Equating gives mu_s = sin(theta) / cos(theta) = tan(theta).',
        'prerequisite_hint': 'Angle of repose condition: mu_s = tan(theta).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-03',
        'title': 'Work Done by Constant Force',
        'prompt': 'A force F = 3i + 4j N moves an object from (0,0) to (2, 3) meters. What is the work done?',
        'options': [{'id': 'A', 'text': '18 Joules'}, {'id': 'B', 'text': '14 Joules'}, {'id': 'C', 'text': '25 Joules'}, {'id': 'D', 'text': '7 Joules'}],
        'correct_answer': 'A',
        'explanation': 'Displacement d = 2i + 3j. Work W = F . d = (3)(2) + (4)(3) = 6 + 12 = 18 Joules.',
        'prerequisite_hint': 'Work is the dot product of force vector and displacement vector: W = F . d.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-04',
        'title': 'Escape Velocity from Earth',
        'prompt': 'How does escape velocity from Earth v_e relate to the orbital velocity v_o near Earth surface?',
        'options': [{'id': 'A', 'text': 'v_e = sqrt(2) x v_o'}, {'id': 'B', 'text': 'v_e = 2 x v_o'}, {'id': 'C', 'text': 'v_e = v_o / sqrt(2)'}, {'id': 'D', 'text': 'v_e = 4 x v_o'}],
        'correct_answer': 'A',
        'explanation': 'Escape velocity is v_e = sqrt(2GM/R) and orbital velocity is v_o = sqrt(GM/R). Therefore v_e = sqrt(2) x v_o.',
        'prerequisite_hint': 'Escape velocity requires total energy >= 0, introducing a factor of sqrt(2).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-05',
        'title': 'Electric Field of a Point Charge',
        'prompt': 'If the distance from a point charge is tripled, by what factor does the electric field intensity change?',
        'options': [{'id': 'A', 'text': 'Decreases by a factor of 9 (1/9)'}, {'id': 'B', 'text': 'Decreases by a factor of 3 (1/3)'}, {'id': 'C', 'text': 'Decreases by a factor of 27 (1/27)'}, {'id': 'D', 'text': 'Remains unchanged'}],
        'correct_answer': 'A',
        'explanation': 'Coulombs law states E is proportional to 1/r^2. When r is tripled (r prime = 3r), E prime = E / (3^2) = E / 9.',
        'prerequisite_hint': 'Electric field follows the inverse square law: E is proportional to 1/r^2.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-06',
        'title': 'Equivalent Resistance in Parallel',
        'prompt': 'Three resistors of 6 ohms, 3 ohms, and 2 ohms are connected in parallel. What is their equivalent resistance?',
        'options': [{'id': 'A', 'text': '1 ohm'}, {'id': 'B', 'text': '11 ohms'}, {'id': 'C', 'text': '2 ohms'}, {'id': 'D', 'text': '0.5 ohm'}],
        'correct_answer': 'A',
        'explanation': '1/R_eq = 1/6 + 1/3 + 1/2 = 1/6 + 2/6 + 3/6 = 6/6 = 1. Thus R_eq = 1 ohm.',
        'prerequisite_hint': 'For parallel resistors: 1/R_eq = sum of reciprocals of individual resistances.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-PHYS-07',
        'title': 'Snell Law of Refraction',
        'prompt': 'A light ray passes from glass (index 1.5) to water (index 4/3). What is the critical angle for total internal reflection?',
        'options': [{'id': 'A', 'text': 'arcsin(8/9)'}, {'id': 'B', 'text': 'arcsin(2/3)'}, {'id': 'C', 'text': 'arcsin(9/8)'}, {'id': 'D', 'text': '45 degrees'}],
        'correct_answer': 'A',
        'explanation': 'Critical angle sin(theta_c) = n2 / n1 = (4/3) / (3/2) = (4/3) x (2/3) = 8/9. Hence theta_c = arcsin(8/9).',
        'prerequisite_hint': 'Total internal reflection occurs when light travels from denser to rarer medium: sin(theta_c) = n_rare / n_dense.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CHEM-03',
        'title': 'Molecular Geometry of Xenon Tetrafluoride',
        'prompt': 'What is the shape and hybridization of XeF4 according to VSEPR theory?',
        'options': [{'id': 'A', 'text': 'Square planar with sp3d2 hybridization'}, {'id': 'B', 'text': 'Tetrahedral with sp3 hybridization'}, {'id': 'C', 'text': 'See-saw with sp3d hybridization'}, {'id': 'D', 'text': 'Octahedral with sp3d2 hybridization'}],
        'correct_answer': 'A',
        'explanation': 'Xe has 8 valence electrons. With 4 bonding pairs and 2 lone pairs, steric number is 6 (sp3d2). The two lone pairs occupy opposite axial positions, resulting in a square planar geometry.',
        'prerequisite_hint': 'Steric number = bonded atoms + lone pairs. 4 bonds + 2 lone pairs = square planar.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CHEM-04',
        'title': 'Gibbs Free Energy and Spontaneity',
        'prompt': 'For an exothermic reaction with positive entropy change (Delta H < 0 and Delta S > 0), when is the reaction spontaneous?',
        'options': [{'id': 'A', 'text': 'Spontaneous at all temperatures'}, {'id': 'B', 'text': 'Spontaneous only at low temperatures'}, {'id': 'C', 'text': 'Spontaneous only at high temperatures'}, {'id': 'D', 'text': 'Non-spontaneous at all temperatures'}],
        'correct_answer': 'A',
        'explanation': 'Delta G = Delta H - T Delta S. If Delta H is negative and Delta S is positive, Delta G is always negative regardless of temperature T, making it spontaneous at all temperatures.',
        'prerequisite_hint': 'Spontaneous processes have Delta G < 0.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CHEM-05',
        'title': 'Le Chatelier Principle Pressure Effect',
        'prompt': 'In the Haber process N2(g) + 3H2(g) <=> 2NH3(g), what happens to equilibrium when pressure is increased at constant temperature?',
        'options': [{'id': 'A', 'text': 'Shifts forward (towards ammonia production)'}, {'id': 'B', 'text': 'Shifts backward (towards reactants)'}, {'id': 'C', 'text': 'Equilibrium constant increases'}, {'id': 'D', 'text': 'No shift occurs'}],
        'correct_answer': 'A',
        'explanation': 'Reactants have 4 moles of gas (1 + 3) while products have 2 moles of gas. Increasing pressure shifts equilibrium towards the side with fewer gas moles (forward direction).',
        'prerequisite_hint': 'Higher pressure favors the side with fewer moles of gaseous species.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CHEM-06',
        'title': 'Markovnikov Rule in Alkene Addition',
        'prompt': 'What is the major product when propene (CH3-CH=CH2) reacts with HBr in the absence of peroxides?',
        'options': [{'id': 'A', 'text': '2-bromopropane'}, {'id': 'B', 'text': '1-bromopropane'}, {'id': 'C', 'text': '1,2-dibromopropane'}, {'id': 'D', 'text': 'propane'}],
        'correct_answer': 'A',
        'explanation': 'According to Markovnikovs rule, the electrophilic proton H+ adds to the carbon with more hydrogen atoms to form the more stable secondary carbocation (CH3-CH+-CH3). Bromide then attacks to give 2-bromopropane as the major product.',
        'prerequisite_hint': 'Markovnikov rule: Hydrogen adds to the carbon with more hydrogens, generating the more substituted carbocation.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-BIO-01',
        'title': 'Fluid Mosaic Model of Plasma Membrane',
        'prompt': 'According to Singer and Nicholsons Fluid Mosaic Model, what constitutes the continuous matrix of the cell membrane?',
        'options': [{'id': 'A', 'text': 'Phospholipid bilayer'}, {'id': 'B', 'text': 'Continuous protein sheet'}, {'id': 'C', 'text': 'Cholesterol network'}, {'id': 'D', 'text': 'Cellulose fibers'}],
        'correct_answer': 'A',
        'explanation': 'The fluid mosaic model describes the membrane as a quasi-fluid phospholipid bilayer in which proteins are embedded like icebergs in a lipid sea.',
        'prerequisite_hint': 'Phospholipids form the hydrophobic core and hydrophilic exterior bilayer.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-BIO-04',
        'title': 'Direction of DNA Replication',
        'prompt': 'During DNA replication, DNA polymerase synthesizes the new daughter strand in which direction?',
        'options': [{'id': 'A', 'text': '5 prime to 3 prime only'}, {'id': 'B', 'text': '3 prime to 5 prime only'}, {'id': 'C', 'text': 'Both directions simultaneously'}, {'id': 'D', 'text': 'Dependent on RNA primer direction'}],
        'correct_answer': 'A',
        'explanation': 'DNA polymerases can only add free deoxyribonucleotides to the 3 prime -OH group of an existing strand. Therefore, synthesis proceeds exclusively in the 5 prime to 3 prime direction.',
        'prerequisite_hint': 'DNA synthesis strictly requires a free 3 prime -OH group, driving 5 prime to 3 prime extension.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-BIO-06',
        'title': 'Cardiac Cycle Pacemaker',
        'prompt': 'Which structure serves as the natural primary pacemaker of the human heart by generating action potentials at the highest rate?',
        'options': [{'id': 'A', 'text': 'Sinoatrial (SA) node'}, {'id': 'B', 'text': 'Atrioventricular (AV) node'}, {'id': 'C', 'text': 'Bundle of His'}, {'id': 'D', 'text': 'Purkinje fibers'}],
        'correct_answer': 'A',
        'explanation': 'The Sinoatrial (SA) node located in the upper right atrium auto-generates rhythmic action potentials at 70-75 bpm, setting the pace for the entire heart.',
        'prerequisite_hint': 'SA node initiates cardiac impulses and is known as the heart pacemaker.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Rank of an Identity Matrix',
        'prompt': 'What is the rank of an n x n identity matrix I_n?',
        'options': [{'id': 'A', 'text': 'n'}, {'id': 'B', 'text': '1'}, {'id': 'C', 'text': '0'}, {'id': 'D', 'text': 'n - 1'}],
        'correct_answer': 'A',
        'explanation': 'An n x n identity matrix has n non-zero pivot rows and its determinant is 1. All n column and row vectors are linearly independent, so its rank is strictly n.',
        'prerequisite_hint': 'Rank of a matrix is the number of linearly independent rows or columns.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Trace of a Square Matrix',
        'prompt': 'If matrix A has diagonal elements 3, -1, and 5, what is the trace of matrix 3A?',
        'options': [{'id': 'A', 'text': '21'}, {'id': 'B', 'text': '7'}, {'id': 'C', 'text': '15'}, {'id': 'D', 'text': '-15'}],
        'correct_answer': 'A',
        'explanation': 'Trace of A is the sum of its main diagonal elements: 3 + (-1) + 5 = 7. For scalar multiple, trace(k A) = k x trace(A) = 3 x 7 = 21.',
        'prerequisite_hint': 'Trace is linear: trace(c A) = c x trace(A).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Orthogonal Matrix Determinant Property',
        'prompt': 'If Q is an orthogonal matrix (Q^T x Q = I), what are the possible values for det(Q)?',
        'options': [{'id': 'A', 'text': '+1 or -1'}, {'id': 'B', 'text': '0 only'}, {'id': 'C', 'text': 'Any positive real number'}, {'id': 'D', 'text': '1 only'}],
        'correct_answer': 'A',
        'explanation': 'det(Q^T x Q) = det(Q^T) x det(Q) = (det(Q))^2. Since Q^T x Q = I and det(I) = 1, (det(Q))^2 = 1, which implies det(Q) = +1 or -1.',
        'prerequisite_hint': 'det(A^T) = det(A), and det(AB) = det(A) det(B).',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Adjoint of a 2x2 Matrix',
        'prompt': 'Find the adjoint of matrix A = [[4, 2], [3, 1]].',
        'options': [{'id': 'A', 'text': '[[1, -2], [-3, 4]]'}, {'id': 'B', 'text': '[[4, -2], [-3, 1]]'}, {'id': 'C', 'text': '[[-1, 2], [3, -4]]'}, {'id': 'D', 'text': '[[1, 3], [2, 4]]'}],
        'correct_answer': 'A',
        'explanation': 'For a 2x2 matrix [[a, b], [c, d]], adj(A) is obtained by swapping main diagonal elements (a and d) and negating the off-diagonal elements (-b and -c). Thus adj(A) = [[1, -2], [-3, 4]].',
        'prerequisite_hint': 'For 2x2: swap diagonal entries, change signs of off-diagonal entries.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-LA-01',
        'title': 'Eigenvalues of a Diagonal Matrix',
        'prompt': 'What are the eigenvalues of the diagonal matrix D = diag(2, -3, 5)?',
        'options': [{'id': 'A', 'text': '2, -3, 5'}, {'id': 'B', 'text': '4, 9, 25'}, {'id': 'C', 'text': '0, 1, 2'}, {'id': 'D', 'text': '1/2, -1/3, 1/5'}],
        'correct_answer': 'A',
        'explanation': 'The characteristic polynomial of any diagonal or triangular matrix is det(D - lambda I) = (2 - lambda)(-3 - lambda)(5 - lambda) = 0. Hence the eigenvalues are simply the diagonal entries: 2, -3, and 5.',
        'prerequisite_hint': 'The eigenvalues of a diagonal matrix are its diagonal elements.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-STAT-01',
        'title': 'Variance of Binomial Distribution',
        'prompt': 'For a Binomial distribution B(n, p) with n = 100 and p = 0.2, what is the standard deviation sigma?',
        'options': [{'id': 'A', 'text': '4'}, {'id': 'B', 'text': '16'}, {'id': 'C', 'text': '20'}, {'id': 'D', 'text': '2'}],
        'correct_answer': 'A',
        'explanation': 'Variance = n x p x q = 100 x 0.2 x 0.8 = 16. Standard deviation sigma is the square root of variance: sqrt(16) = 4.',
        'prerequisite_hint': 'Standard deviation is sqrt(n x p x (1 - p)).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-STAT-01',
        'title': 'Conditional Probability and Bayes Theorem',
        'prompt': 'If P(A) = 0.6, P(B) = 0.4, and P(A cap B) = 0.2, what is P(B | A)?',
        'options': [{'id': 'A', 'text': '1/3 (0.333)'}, {'id': 'B', 'text': '1/2 (0.50)'}, {'id': 'C', 'text': '2/5 (0.40)'}, {'id': 'D', 'text': '1/4 (0.25)'}],
        'correct_answer': 'A',
        'explanation': 'P(B | A) = P(A cap B) / P(A) = 0.2 / 0.6 = 2/6 = 1/3.',
        'prerequisite_hint': 'Definition of conditional probability: P(B | A) = P(A cap B) / P(A).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-STAT-01',
        'title': 'Expectation of Rolling Two Fair Dice',
        'prompt': 'What is the mathematical expectation of the sum of numbers obtained by rolling two fair 6-sided dice?',
        'options': [{'id': 'A', 'text': '7'}, {'id': 'B', 'text': '6'}, {'id': 'C', 'text': '8'}, {'id': 'D', 'text': '6.5'}],
        'correct_answer': 'A',
        'explanation': 'Expectation of one die is (1+2+3+4+5+6)/6 = 3.5. By linearity of expectation, E(X1 + X2) = E(X1) + E(X2) = 3.5 + 3.5 = 7.',
        'prerequisite_hint': 'Linearity of expectation holds even for dependent variables: E(X + Y) = E(X) + E(Y).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-ALG-01',
        'title': 'Sum and Product of Quadratic Roots',
        'prompt': 'For the quadratic equation 3x^2 - 12x + 5 = 0, what is the sum of the squares of its roots (alpha^2 + beta^2)?',
        'options': [{'id': 'A', 'text': '114/9 (38/3)'}, {'id': 'B', 'text': '16'}, {'id': 'C', 'text': '10/3'}, {'id': 'D', 'text': '144/9'}],
        'correct_answer': 'A',
        'explanation': 'alpha + beta = -(-12)/3 = 4, alpha x beta = 5/3. alpha^2 + beta^2 = (alpha + beta)^2 - 2 alpha beta = 16 - 2(5/3) = 16 - 10/3 = 38/3.',
        'prerequisite_hint': 'Recall identity: a^2 + b^2 = (a + b)^2 - 2ab.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-ALG-01',
        'title': 'Sum of Infinite Geometric Progression',
        'prompt': 'Find the sum of the infinite geometric series: 6 + 2 + 2/3 + 2/9 + ...',
        'options': [{'id': 'A', 'text': '9'}, {'id': 'B', 'text': '8'}, {'id': 'C', 'text': '12'}, {'id': 'D', 'text': '7.5'}],
        'correct_answer': 'A',
        'explanation': 'First term a = 6, common ratio r = 2/6 = 1/3. S_infinity = a / (1 - r) = 6 / (1 - 1/3) = 6 / (2/3) = 6 x (3/2) = 9.',
        'prerequisite_hint': 'Sum of infinite GP with |r| < 1 is S = a / (1 - r).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CHEM-01',
        'title': 'Bohr Radius for Hydrogen Atom',
        'prompt': 'What is the radius of the first Bohr orbit (n=1) of a hydrogen atom?',
        'options': [{'id': 'A', 'text': '0.529 Angstroms (52.9 pm)'}, {'id': 'B', 'text': '1.058 Angstroms'}, {'id': 'C', 'text': '0.264 Angstroms'}, {'id': 'D', 'text': '2.116 Angstroms'}],
        'correct_answer': 'A',
        'explanation': 'Bohr radius formula r_n = 0.529 x (n^2 / Z) Angstroms. For hydrogen (Z=1, n=1), r1 = 0.529 Angstroms = 52.9 pm.',
        'prerequisite_hint': 'Bohr orbit radius scales as n^2 / Z.',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-CHEM-02',
        'title': 'Periodic Trends in Ionization Energy',
        'prompt': 'Why does Nitrogen have a higher first ionization enthalpy than Oxygen, despite having a lower nuclear charge?',
        'options': [{'id': 'A', 'text': 'Nitrogen has a stable half-filled 2p^3 subshell'}, {'id': 'B', 'text': 'Oxygen has smaller atomic radius'}, {'id': 'C', 'text': 'Nitrogen has fewer shielding electrons'}, {'id': 'D', 'text': 'Oxygen forms diatomic molecules'}],
        'correct_answer': 'A',
        'explanation': 'Nitrogens electron configuration is 1s2 2s2 2p3, which possesses extra stability due to exactly half-filled 2p orbitals. Oxygen is 1s2 2s2 2p4, where losing one electron relieves inter-electronic repulsion.',
        'prerequisite_hint': 'Half-filled and fully-filled degenerate subshells confer exceptional thermodynamic stability.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-CHEM-07',
        'title': 'Faraday First Law of Electrolysis',
        'prompt': 'How many Coulombs of electric charge are required to deposit 1 mole of Copper from a Cu2+ solution?',
        'options': [{'id': 'A', 'text': '2 Faradays (193,000 Coulombs)'}, {'id': 'B', 'text': '1 Faraday (96,500 Coulombs)'}, {'id': 'C', 'text': '0.5 Faraday'}, {'id': 'D', 'text': '4 Faradays'}],
        'correct_answer': 'A',
        'explanation': 'Cu2+ + 2e- -> Cu(s). Each mole of Cu requires 2 moles of electrons. Total charge Q = n x F = 2 x 96,485 C = approx 193,000 Coulombs.',
        'prerequisite_hint': 'Each mole of electrons corresponds to 1 Faraday (approx 96,500 C).',
        'difficulty': 'EASY',
        'points': 10
    },
    {
        'topic_code': 'TOP-BIO-05',
        'title': 'Light Reaction and Water Splitting',
        'prompt': 'During oxygenic photosynthesis, photolysis of water occurs associated with which complex?',
        'options': [{'id': 'A', 'text': 'Photosystem II (PS II) on the luminal side of thylakoid'}, {'id': 'B', 'text': 'Photosystem I (PS I) on the stroma side'}, {'id': 'C', 'text': 'ATP synthase complex'}, {'id': 'D', 'text': 'Cytochrome b6f complex'}],
        'correct_answer': 'A',
        'explanation': 'The Oxygen-Evolving Complex (OEC) containing a manganese cluster is physically linked with Photosystem II (P680) on the lumen side of the thylakoid membrane.',
        'prerequisite_hint': 'PS II photolyses water: 2H2O -> 4H+ + 4e- + O2.',
        'difficulty': 'MEDIUM',
        'points': 15
    },
    {
        'topic_code': 'TOP-BIO-07',
        'title': 'Ten Percent Law of Energy Transfer',
        'prompt': 'According to Lindemans 10% law, if primary producers synthesize 10,000 Joules of energy, how much is available to tertiary consumers?',
        'options': [{'id': 'A', 'text': '10 Joules'}, {'id': 'B', 'text': '100 Joules'}, {'id': 'C', 'text': '1,000 Joules'}, {'id': 'D', 'text': '1 Joule'}],
        'correct_answer': 'A',
        'explanation': 'Producers (10,000 J) -> Primary Consumers (1,000 J) -> Secondary Consumers (100 J) -> Tertiary Consumers (10 J). Each step transfers only 10%.',
        'prerequisite_hint': 'Only 10% of energy is transferred to each successive trophic level.',
        'difficulty': 'EASY',
        'points': 10
    },
]

