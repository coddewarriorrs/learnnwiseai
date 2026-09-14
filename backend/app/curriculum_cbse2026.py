# CBSE / NCERT Official Syllabus Database (Academic Session 2026-27)
# Comprehensive hierarchy: Board -> AcademicYear -> AcademicClass -> Subject -> Unit -> Chapter -> Topic -> SubTopic -> LearningOutcome -> Question

CBSE_2026_SYLLABUS = {
    "board": {
        "name": "Central Board of Secondary Education",
        "code": "CBSE",
        "country": "India",
        "description": "National level board of education in India for public and private schools"
    },
    "academic_year": {
        "year_code": "2026-27",
        "title": "CBSE Academic Session 2026-2027",
        "is_current": True
    },
    "classes": [
        # =========================================================================
        # CLASS 8 (CBSE 2026-27): Mathematics + Integrated Science
        # =========================================================================
        {
            "class_number": 8,
            "title": "Class 8",
            "code": "CBSE-2026-CLASS-08",
            "description": "CBSE Class 8 Curriculum 2026-27",
            "order_index": 1,
            "subjects": [
                {
                    "name": "Mathematics",
                    "code": "CBSE-08-MATH",
                    "is_integrated_science": False,
                    "description": "NCERT Class 8 Mathematics",
                    "order_index": 1,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Number Systems & Arithmetic",
                            "code": "CBSE-08-MATH-U1",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Rational Numbers",
                                    "code": "CBSE-08-MATH-CH01",
                                    "topics": [
                                        {
                                            "title": "Properties of Rational Numbers",
                                            "code": "CBSE-08-MATH-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Closure, Commutativity & Associativity", "Role of Zero and One", "Distributive Property"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-01-01", "statement": "Verify and apply closure, commutative, and associative properties to rational arithmetic", "bloom_level": "APPLY"},
                                                {"code": "LO-08-MATH-01-02", "statement": "Determine additive and multiplicative inverses of rational numbers", "bloom_level": "UNDERSTAND"}
                                            ]
                                        },
                                        {
                                            "title": "Representation on Number Line & Density",
                                            "code": "CBSE-08-MATH-CH01-T02",
                                            "prerequisites": ["CBSE-08-MATH-CH01-T01"],
                                            "subtopics": ["Plotting rational numbers on number line", "Finding rational numbers between two rational numbers"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-01-03", "statement": "Represent positive and negative rational fractions accurately on a number line", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Squares and Square Roots",
                                    "code": "CBSE-08-MATH-CH02",
                                    "topics": [
                                        {
                                            "title": "Square Numbers & Properties",
                                            "code": "CBSE-08-MATH-CH02-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Units digits of squares", "Pythagorean triplets"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-02-01", "statement": "Identify square number patterns and evaluate Pythagorean triplets", "bloom_level": "UNDERSTAND"}
                                            ]
                                        },
                                        {
                                            "title": "Square Roots by Prime Factorisation & Long Division",
                                            "code": "CBSE-08-MATH-CH02-T02",
                                            "prerequisites": ["CBSE-08-MATH-CH02-T01"],
                                            "subtopics": ["Prime factorisation square roots", "Division method for whole numbers and decimals"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-02-02", "statement": "Calculate square roots of integers and decimals using long division", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Cubes and Cube Roots",
                                    "code": "CBSE-08-MATH-CH03",
                                    "topics": [
                                        {
                                            "title": "Cube Numbers & Prime Factorisation",
                                            "code": "CBSE-08-MATH-CH03-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH02-T02"],
                                            "subtopics": ["Hardy-Ramanujan numbers", "Cube roots by prime factorisation"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-03-01", "statement": "Find cube root of perfect cubes using prime factorisation triplets", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Exponents and Powers",
                                    "code": "CBSE-08-MATH-CH04",
                                    "topics": [
                                        {
                                            "title": "Negative Exponents & Laws of Exponents",
                                            "code": "CBSE-08-MATH-CH04-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH01-T01"],
                                            "subtopics": ["Powers with negative exponents", "Laws of integral exponents", "Standard scientific form"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-04-01", "statement": "Simplify expressions using laws of exponents with negative powers", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Algebra",
                            "code": "CBSE-08-MATH-U2",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 5,
                                    "title": "Linear Equations in One Variable",
                                    "code": "CBSE-08-MATH-CH05",
                                    "topics": [
                                        {
                                            "title": "Solving Linear Equations",
                                            "code": "CBSE-08-MATH-CH05-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH01-T01"],
                                            "subtopics": ["Equations with linear expression on one side", "Variables on both sides", "Word problems"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-05-01", "statement": "Solve linear algebraic equations with variables on both sides and apply to real-world age and number problems", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 6,
                                    "title": "Algebraic Expressions and Identities",
                                    "code": "CBSE-08-MATH-CH06",
                                    "topics": [
                                        {
                                            "title": "Multiplication of Polynomials & Standard Identities",
                                            "code": "CBSE-08-MATH-CH06-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH05-T01"],
                                            "subtopics": ["Monomials by polynomials", "Standard algebraic identities (a+b)^2, (a-b)^2, a^2-b^2"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-06-01", "statement": "Apply standard algebraic identities to expand products and evaluate numerical squares", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 7,
                                    "title": "Factorisation",
                                    "code": "CBSE-08-MATH-CH07",
                                    "topics": [
                                        {
                                            "title": "Methods of Factorisation",
                                            "code": "CBSE-08-MATH-CH07-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH06-T01"],
                                            "subtopics": ["Common factors", "Regrouping terms", "Using identities", "Splitting middle term"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-07-01", "statement": "Factorise quadratic expressions by regrouping and splitting the middle term", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Geometry, Mensuration & Graphs",
                            "code": "CBSE-08-MATH-U3",
                            "weightage_marks": 30,
                            "chapters": [
                                {
                                    "chapter_number": 8,
                                    "title": "Understanding Quadrilaterals",
                                    "code": "CBSE-08-MATH-CH08",
                                    "topics": [
                                        {
                                            "title": "Polygons & Angle Sum Property",
                                            "code": "CBSE-08-MATH-CH08-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Classification of polygons", "Sum of exterior angles", "Parallelogram properties"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-08-01", "statement": "Determine unknown angles in polygons and apply diagonal properties of rhombuses and rectangles", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 9,
                                    "title": "Mensuration",
                                    "code": "CBSE-08-MATH-CH09",
                                    "topics": [
                                        {
                                            "title": "Area of Trapezium & Polygons",
                                            "code": "CBSE-08-MATH-CH09-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH08-T01"],
                                            "subtopics": ["Area of trapezium and general quadrilateral", "Surface area of cuboid, cube, cylinder"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-09-01", "statement": "Calculate surface area and volume of cylinders, cuboids, and trapeziums", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 10,
                                    "title": "Direct and Inverse Proportions",
                                    "code": "CBSE-08-MATH-CH10",
                                    "topics": [
                                        {
                                            "title": "Direct vs Inverse Variation",
                                            "code": "CBSE-08-MATH-CH10-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH01-T01"],
                                            "subtopics": ["Direct proportion formula x/y = k", "Inverse proportion formula xy = k", "Word problems on work and time"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-10-01", "statement": "Distinguish between direct and inverse variations and solve multi-step rate problems", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 11,
                                    "title": "Introduction to Graphs",
                                    "code": "CBSE-08-MATH-CH11",
                                    "topics": [
                                        {
                                            "title": "Line Graphs & Coordinate Axes",
                                            "code": "CBSE-08-MATH-CH11-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Bar graphs vs Line graphs", "Cartesian coordinates (x, y)", "Linear graphs"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-MATH-11-01", "statement": "Plot coordinates on Cartesian axes and interpret continuous line graphs", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Science",
                    "code": "CBSE-08-SCI",
                    "is_integrated_science": True,
                    "description": "NCERT Class 8 Integrated Science (Physics, Chemistry, Biology domains)",
                    "order_index": 2,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Food & Living World",
                            "code": "CBSE-08-SCI-U1",
                            "weightage_marks": 28,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Crop Production and Management",
                                    "code": "CBSE-08-SCI-CH01",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Agricultural Practices & Soil Preparation",
                                            "code": "CBSE-08-SCI-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Kharif vs Rabi crops", "Preparation of soil", "Sowing and seed drill"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-01-01", "statement": "Differentiate seasonal crop cycles and describe scientific soil preparation methods", "bloom_level": "UNDERSTAND"}
                                            ]
                                        },
                                        {
                                            "title": "Irrigation, Manures & Fertilizers",
                                            "code": "CBSE-08-SCI-CH01-T02",
                                            "prerequisites": ["CBSE-08-SCI-CH01-T01"],
                                            "subtopics": ["Organic manure vs Chemical fertilizer", "Drip and sprinkler irrigation systems"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-01-02", "statement": "Compare modern water-saving irrigation methods with traditional techniques", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Microorganisms: Friend and Foe",
                                    "code": "CBSE-08-SCI-CH02",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Classification & Commercial Uses",
                                            "code": "CBSE-08-SCI-CH02-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Bacteria, Fungi, Protozoa, Algae", "Fermentation and Yeast", "Antibiotics and Vaccines"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-02-01", "statement": "Explain microbial roles in nitrogen fixation, fermentation, and vaccine preparation", "bloom_level": "UNDERSTAND"}
                                            ]
                                        },
                                        {
                                            "title": "Pathogenic Microbes & Food Preservation",
                                            "code": "CBSE-08-SCI-CH02-T02",
                                            "prerequisites": ["CBSE-08-SCI-CH02-T01"],
                                            "subtopics": ["Communicable disease transmission", "Pasteurization and chemical preservatives"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-02-02", "statement": "Evaluate methods of food preservation including pasteurization and salting", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Reproduction in Animals",
                                    "code": "CBSE-08-SCI-CH03",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Sexual vs Asexual Reproduction",
                                            "code": "CBSE-08-SCI-CH03-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Binary fission in Amoeba", "Budding in Hydra", "Internal vs External fertilization"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-03-01", "statement": "Contrast internal and external fertilization across aquatic and terrestrial species", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Materials & Chemical Substances",
                            "code": "CBSE-08-SCI-U2",
                            "weightage_marks": 24,
                            "chapters": [
                                {
                                    "chapter_number": 4,
                                    "title": "Coal and Petroleum",
                                    "code": "CBSE-08-SCI-CH04",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Fossil Fuels & Fractional Distillation",
                                            "code": "CBSE-08-SCI-CH04-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Carbonisation of coal", "Coke, Coal Tar and Coal Gas", "Fractional distillation of crude petroleum"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-04-01", "statement": "Describe fractional distillation fractions of petroleum and environmental impact of fossil fuel depletion", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 5,
                                    "title": "Combustion and Flame",
                                    "code": "CBSE-08-SCI-CH05",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Conditions for Combustion & Flame Structure",
                                            "code": "CBSE-08-SCI-CH05-T01",
                                            "prerequisites": ["CBSE-08-SCI-CH04-T01"],
                                            "subtopics": ["Ignition temperature", "Fire extinguisher chemistry", "Luminous vs non-luminous flame zones"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-05-01", "statement": "Identify zones of a candle flame and determine calorific values of fuels", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 6,
                                    "title": "Chemical Effects of Electric Current",
                                    "code": "CBSE-08-SCI-CH06",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Conduction in Liquids & Electroplating",
                                            "code": "CBSE-08-SCI-CH06-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Electrolytes and ion conduction", "Electroplating mechanisms and industrial utility"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-06-01", "statement": "Demonstrate electrolyte conduction and explain chromium electroplating for corrosion resistance", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Motion, Force & Pressure",
                            "code": "CBSE-08-SCI-U3",
                            "weightage_marks": 28,
                            "chapters": [
                                {
                                    "chapter_number": 7,
                                    "title": "Force and Pressure",
                                    "code": "CBSE-08-SCI-CH07",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Types of Forces & Net Force",
                                            "code": "CBSE-08-SCI-CH07-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Contact vs non-contact forces", "Magnitude and direction of force", "Pressure formula P = F / A"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-07-01", "statement": "Calculate pressure exerted by solids and liquids and explain atmospheric pressure", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 8,
                                    "title": "Friction",
                                    "code": "CBSE-08-SCI-CH08",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Static, Sliding & Rolling Friction",
                                            "code": "CBSE-08-SCI-CH08-T01",
                                            "prerequisites": ["CBSE-08-SCI-CH07-T01"],
                                            "subtopics": ["Factors affecting friction", "Friction as a necessary evil", "Lubricants, ball bearings, fluid drag"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-08-01", "statement": "Compare static, sliding, and rolling friction and explain streamlining in aeroplanes", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 9,
                                    "title": "Sound",
                                    "code": "CBSE-08-SCI-CH09",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Vibration, Frequency, Amplitude & Pitch",
                                            "code": "CBSE-08-SCI-CH09-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Human vocal cords and eardrum", "Amplitude determines loudness", "Frequency determines pitch", "Audible range 20 Hz - 20,000 Hz"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-09-01", "statement": "Relate loudness to amplitude and pitch to frequency of acoustic oscillations", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 10,
                                    "title": "Light",
                                    "code": "CBSE-08-SCI-CH10",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Laws of Reflection & Multiple Images",
                                            "code": "CBSE-08-SCI-CH10-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Angle of incidence equals reflection", "Regular vs diffused reflection", "Human eye anatomy and vision care"],
                                            "learning_outcomes": [
                                                {"code": "LO-08-SCI-10-01", "statement": "Apply laws of reflection to plane mirrors and describe cornea, iris, and retina functions", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # =========================================================================
        # CLASS 9 (CBSE 2026-27): Mathematics + Integrated Science
        # =========================================================================
        {
            "class_number": 9,
            "title": "Class 9",
            "code": "CBSE-2026-CLASS-09",
            "description": "CBSE Class 9 Curriculum 2026-27",
            "order_index": 2,
            "subjects": [
                {
                    "name": "Mathematics",
                    "code": "CBSE-09-MATH",
                    "is_integrated_science": False,
                    "description": "NCERT Class 9 Mathematics",
                    "order_index": 1,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Number Systems",
                            "code": "CBSE-09-MATH-U1",
                            "weightage_marks": 10,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Number Systems",
                                    "code": "CBSE-09-MATH-CH01",
                                    "topics": [
                                        {
                                            "title": "Irrational Numbers & Real Number Operations",
                                            "code": "CBSE-09-MATH-CH01-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH01-T01"],
                                            "subtopics": ["Proof of irrationality root 2, root 3", "Rationalising denominators of 1/(a + b root x)"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-01-01", "statement": "Rationalise binomial radical denominators and represent square root of x geometrically", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Algebra",
                            "code": "CBSE-09-MATH-U2",
                            "weightage_marks": 20,
                            "chapters": [
                                {
                                    "chapter_number": 2,
                                    "title": "Polynomials",
                                    "code": "CBSE-09-MATH-CH02",
                                    "topics": [
                                        {
                                            "title": "Remainder & Factor Theorems",
                                            "code": "CBSE-09-MATH-CH02-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH07-T01"],
                                            "subtopics": ["Zeroes of polynomial", "Factor theorem for quadratics and cubics", "Algebraic identities"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-02-01", "statement": "Factorise cubic polynomials using the Factor Theorem and synthetic division", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Linear Equations in Two Variables",
                                    "code": "CBSE-09-MATH-CH03",
                                    "topics": [
                                        {
                                            "title": "Solutions & Graph of ax + by + c = 0",
                                            "code": "CBSE-09-MATH-CH03-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH05-T01", "CBSE-08-MATH-CH11-T01"],
                                            "subtopics": ["Standard form of linear equation", "Graphing straight lines through two points"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-03-01", "statement": "Plot linear equations in two variables and establish that every point on the line is a solution", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Geometry",
                            "code": "CBSE-09-MATH-U3",
                            "weightage_marks": 27,
                            "chapters": [
                                {
                                    "chapter_number": 4,
                                    "title": "Lines and Angles",
                                    "code": "CBSE-09-MATH-CH04",
                                    "topics": [
                                        {
                                            "title": "Parallel Lines & Transversals",
                                            "code": "CBSE-09-MATH-CH04-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Alternate interior angles", "Consecutive interior angles sum to 180 degrees"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-04-01", "statement": "Prove and apply angle relationships created by a transversal cutting parallel lines", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 5,
                                    "title": "Triangles",
                                    "code": "CBSE-09-MATH-CH05",
                                    "topics": [
                                        {
                                            "title": "Congruence Criteria (SAS, ASA, AAS, SSS, RHS)",
                                            "code": "CBSE-09-MATH-CH05-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH04-T01"],
                                            "subtopics": ["Axiom SAS", "Theorems on isosceles triangles", "Inequalities in triangles"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-05-01", "statement": "Formulate rigorous geometric proofs using triangle congruence criteria", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 6,
                                    "title": "Circles",
                                    "code": "CBSE-09-MATH-CH06",
                                    "topics": [
                                        {
                                            "title": "Chords, Arcs & Cyclic Quadrilaterals",
                                            "code": "CBSE-09-MATH-CH06-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH05-T01"],
                                            "subtopics": ["Perpendicular from centre bisects chord", "Angle subtended by arc at centre is double", "Opposite angles of cyclic quadrilateral sum to 180"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-06-01", "statement": "Prove circle theorems concerning subtended arc angles and cyclic quadrilateral properties", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 4,
                            "title": "Unit IV: Mensuration & Statistics",
                            "code": "CBSE-09-MATH-U4",
                            "weightage_marks": 23,
                            "chapters": [
                                {
                                    "chapter_number": 7,
                                    "title": "Heron's Formula",
                                    "code": "CBSE-09-MATH-CH07",
                                    "topics": [
                                        {
                                            "title": "Area of Triangle using Semi-perimeter",
                                            "code": "CBSE-09-MATH-CH07-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH09-T01"],
                                            "subtopics": ["Heron formula sqrt[s(s-a)(s-b)(s-c)]", "Area of quadrilaterals by partitioning"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-07-01", "statement": "Compute triangle areas using semi-perimeter when heights are unknown", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 8,
                                    "title": "Surface Areas and Volumes",
                                    "code": "CBSE-09-MATH-CH08",
                                    "topics": [
                                        {
                                            "title": "Cones, Spheres & Hemispheres",
                                            "code": "CBSE-09-MATH-CH08-T01",
                                            "prerequisites": ["CBSE-08-MATH-CH09-T01"],
                                            "subtopics": ["Curved surface area of cone pi*r*l", "Volume of sphere 4/3*pi*r^3", "Hemisphere formulas"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-MATH-08-01", "statement": "Calculate total surface area and volume of right circular cones and spheres", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Science",
                    "code": "CBSE-09-SCI",
                    "is_integrated_science": True,
                    "description": "NCERT Class 9 Integrated Science",
                    "order_index": 2,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Matter – Nature and Behaviour",
                            "code": "CBSE-09-SCI-U1",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Matter in Our Surroundings",
                                    "code": "CBSE-09-SCI-CH01",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "States of Matter & Latent Heat",
                                            "code": "CBSE-09-SCI-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Kinetic theory of particles", "Latent heat of fusion and vaporisation", "Evaporation factors"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-01-01", "statement": "Explain phase transitions using latent heat and cooling caused by evaporation", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Atoms and Molecules",
                                    "code": "CBSE-09-SCI-CH02",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Chemical Combination & Mole Concept",
                                            "code": "CBSE-09-SCI-CH02-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH01-T01"],
                                            "subtopics": ["Law of conservation of mass", "Law of constant proportions", "Writing chemical formulas with valency"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-02-01", "statement": "Write chemical formulas using criss-cross valency method and calculate formula unit mass", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Structure of the Atom",
                                    "code": "CBSE-09-SCI-CH03",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Subatomic Particles & Bohr Model",
                                            "code": "CBSE-09-SCI-CH03-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH02-T01"],
                                            "subtopics": ["Rutherford alpha scattering experiment", "Bohr-Bury electron distribution rules", "Atomic number and isotopes"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-03-01", "statement": "Deduce atomic structure, valence electrons, and isotope notation", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Organization in the Living World",
                            "code": "CBSE-09-SCI-U2",
                            "weightage_marks": 22,
                            "chapters": [
                                {
                                    "chapter_number": 4,
                                    "title": "The Fundamental Unit of Life",
                                    "code": "CBSE-09-SCI-CH04",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Cell Structure & Organelles",
                                            "code": "CBSE-09-SCI-CH04-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Plasma membrane and osmosis", "Nucleus, ER, Golgi apparatus, Mitochondria", "Plant vs Animal cell"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-04-01", "statement": "Explain endosmosis, exosmosis, and functions of ATP-producing mitochondria", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 5,
                                    "title": "Tissues",
                                    "code": "CBSE-09-SCI-CH05",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Plant & Animal Tissues",
                                            "code": "CBSE-09-SCI-CH05-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH04-T01"],
                                            "subtopics": ["Meristematic vs permanent plant tissue", "Xylem and Phloem", "Epithelial, muscular, nervous, connective animal tissues"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-05-01", "statement": "Classify plant vascular tissues and animal muscular/connective tissues", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Motion, Force and Work",
                            "code": "CBSE-09-SCI-U3",
                            "weightage_marks": 27,
                            "chapters": [
                                {
                                    "chapter_number": 6,
                                    "title": "Motion",
                                    "code": "CBSE-09-SCI-CH06",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Kinematics & Equations of Motion",
                                            "code": "CBSE-09-SCI-CH06-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Distance vs displacement", "Speed vs velocity", "Equations: v=u+at, s=ut+1/2at^2, v^2=u^2+2as"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-06-01", "statement": "Derive graphically and solve kinematic equations for uniformly accelerated motion", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 7,
                                    "title": "Force and Laws of Motion",
                                    "code": "CBSE-09-SCI-CH07",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Newton's Laws & Conservation of Momentum",
                                            "code": "CBSE-09-SCI-CH07-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH06-T01"],
                                            "subtopics": ["Inertia and first law", "F = ma and second law", "Action-reaction pairs and recoil of gun"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-07-01", "statement": "Apply Newton's second law and conservation of linear momentum to collision systems", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 8,
                                    "title": "Gravitation",
                                    "code": "CBSE-09-SCI-CH08",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Universal Gravitation & Archimedes' Principle",
                                            "code": "CBSE-09-SCI-CH08-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH07-T01"],
                                            "subtopics": ["F = G M m / r^2", "Acceleration due to gravity g = 9.8 m/s^2", "Buoyancy and Archimedes principle"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-08-01", "statement": "Calculate free-fall acceleration and buoyant forces using Archimedes principle", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 9,
                                    "title": "Work and Energy",
                                    "code": "CBSE-09-SCI-CH09",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Kinetic & Potential Energy Conservation",
                                            "code": "CBSE-09-SCI-CH09-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH07-T01"],
                                            "subtopics": ["Work W = F * s", "Kinetic energy 1/2 m v^2", "Gravitational potential energy m g h", "Power P = W / t"],
                                            "learning_outcomes": [
                                                {"code": "LO-09-SCI-09-01", "statement": "Apply conservation of mechanical energy to freely falling bodies and compute electrical kilowatt-hours", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # =========================================================================
        # CLASS 10 (CBSE 2026-27): Mathematics + Integrated Science
        # =========================================================================
        {
            "class_number": 10,
            "title": "Class 10",
            "code": "CBSE-2026-CLASS-10",
            "description": "CBSE Class 10 Board Curriculum 2026-27",
            "order_index": 3,
            "subjects": [
                {
                    "name": "Mathematics",
                    "code": "CBSE-10-MATH",
                    "is_integrated_science": False,
                    "description": "NCERT Class 10 Mathematics",
                    "order_index": 1,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Number Systems",
                            "code": "CBSE-10-MATH-U1",
                            "weightage_marks": 6,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Real Numbers",
                                    "code": "CBSE-10-MATH-CH01",
                                    "topics": [
                                        {
                                            "title": "Fundamental Theorem of Arithmetic & Proof of Irrationality",
                                            "code": "CBSE-10-MATH-CH01-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH01-T01"],
                                            "subtopics": ["HCF and LCM prime factorisation", "Proving root 3 and root 5 irrational"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-01-01", "statement": "Formulate contradiction proofs for irrationality and evaluate HCF-LCM relationships", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Algebra",
                            "code": "CBSE-10-MATH-U2",
                            "weightage_marks": 20,
                            "chapters": [
                                {
                                    "chapter_number": 2,
                                    "title": "Polynomials",
                                    "code": "CBSE-10-MATH-CH02",
                                    "topics": [
                                        {
                                            "title": "Zeroes & Coefficients of Quadratic Polynomials",
                                            "code": "CBSE-10-MATH-CH02-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH02-T01"],
                                            "subtopics": ["Geometrical meaning of zeroes", "Relationship between zeroes and coefficients alpha + beta = -b/a"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-02-01", "statement": "Determine zeroes geometrically and apply sum and product formulas to construct quadratics", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Pair of Linear Equations in Two Variables",
                                    "code": "CBSE-10-MATH-CH03",
                                    "topics": [
                                        {
                                            "title": "Algebraic & Graphical Consistency",
                                            "code": "CBSE-10-MATH-CH03-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH03-T01"],
                                            "subtopics": ["Consistency conditions a1/a2 ratios", "Substitution and elimination methods", "Speed-distance upstream/downstream problems"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-03-01", "statement": "Solve simultaneous linear equations using algebraic elimination and solve upstream-downstream rate problems", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Quadratic Equations",
                                    "code": "CBSE-10-MATH-CH04",
                                    "topics": [
                                        {
                                            "title": "Quadratic Formula & Nature of Roots",
                                            "code": "CBSE-10-MATH-CH04-T01",
                                            "prerequisites": ["CBSE-10-MATH-CH02-T01"],
                                            "subtopics": ["Standard form ax^2 + bx + c = 0", "Discriminant D = b^2 - 4ac", "Real and equal roots condition"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-04-01", "statement": "Evaluate the nature of roots using discriminant and solve by quadratic formula", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 5,
                                    "title": "Arithmetic Progressions",
                                    "code": "CBSE-10-MATH-CH05",
                                    "topics": [
                                        {
                                            "title": "nth Term & Sum of n Terms of AP",
                                            "code": "CBSE-10-MATH-CH05-T01",
                                            "prerequisites": [],
                                            "subtopics": ["General term an = a + (n-1)d", "Sum formula Sn = n/2 [2a + (n-1)d]"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-05-01", "statement": "Calculate terms and sums of arithmetic sequences for daily installment and seating arrangements", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Trigonometry",
                            "code": "CBSE-10-MATH-U3",
                            "weightage_marks": 12,
                            "chapters": [
                                {
                                    "chapter_number": 6,
                                    "title": "Introduction to Trigonometry",
                                    "code": "CBSE-10-MATH-CH06",
                                    "topics": [
                                        {
                                            "title": "Ratios & Fundamental Identities",
                                            "code": "CBSE-10-MATH-CH06-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Values at 0, 30, 45, 60, 90 degrees", "Identity sin^2 A + cos^2 A = 1", "sec^2 A - tan^2 A = 1"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-06-01", "statement": "Prove trigonometric identities using fundamental Pythagorean relations", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 7,
                                    "title": "Some Applications of Trigonometry",
                                    "code": "CBSE-10-MATH-CH07",
                                    "topics": [
                                        {
                                            "title": "Heights and Distances",
                                            "code": "CBSE-10-MATH-CH07-T01",
                                            "prerequisites": ["CBSE-10-MATH-CH06-T01"],
                                            "subtopics": ["Angle of elevation and depression", "Multi-point observations of towers and ships"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-07-01", "statement": "Solve two-triangle height and distance problems using angles of elevation and depression", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 4,
                            "title": "Unit IV: Geometry & Coordinate Geometry",
                            "code": "CBSE-10-MATH-U4",
                            "weightage_marks": 21,
                            "chapters": [
                                {
                                    "chapter_number": 8,
                                    "title": "Triangles",
                                    "code": "CBSE-10-MATH-CH08",
                                    "topics": [
                                        {
                                            "title": "Similarity Criteria & Thales' Theorem",
                                            "code": "CBSE-10-MATH-CH08-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH05-T01"],
                                            "subtopics": ["Basic Proportionality Theorem (Thales)", "Criteria for similarity (AAA, SSS, SAS)"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-08-01", "statement": "Prove and apply the Basic Proportionality Theorem to similar triangle configurations", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 9,
                                    "title": "Coordinate Geometry",
                                    "code": "CBSE-10-MATH-CH09",
                                    "topics": [
                                        {
                                            "title": "Distance & Section Formulas",
                                            "code": "CBSE-10-MATH-CH09-T01",
                                            "prerequisites": ["CBSE-09-MATH-CH03-T01"],
                                            "subtopics": ["Distance formula sqrt[(x2-x1)^2 + (y2-y1)^2]", "Internal section formula (m1x2+m2x1)/(m1+m2)"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-MATH-09-01", "statement": "Calculate points of trisection and collinearity using distance and section formulas", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Science",
                    "code": "CBSE-10-SCI",
                    "is_integrated_science": True,
                    "description": "NCERT Class 10 Integrated Science (Board 2026-27)",
                    "order_index": 2,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Chemical Substances – Nature and Behaviour",
                            "code": "CBSE-10-SCI-U1",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Chemical Reactions and Equations",
                                    "code": "CBSE-10-SCI-CH01",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Balancing & Reaction Types",
                                            "code": "CBSE-10-SCI-CH01-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH02-T01"],
                                            "subtopics": ["Balancing equations", "Combination, decomposition, displacement, double displacement", "Redox reactions"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-01-01", "statement": "Balance redox equations and identify oxidation-reduction agents", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Acids, Bases and Salts",
                                    "code": "CBSE-10-SCI-CH02",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "pH Scale & Industrial Salts",
                                            "code": "CBSE-10-SCI-CH02-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH01-T01"],
                                            "subtopics": ["pH definition and indicators", "Bleaching powder, baking soda, washing soda, plaster of Paris"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-02-01", "statement": "Explain the chlor-alkali process and manufacture of Plaster of Paris and Baking Soda", "bloom_level": "UNDERSTAND"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 3,
                                    "title": "Carbon and its Compounds",
                                    "code": "CBSE-10-SCI-CH03",
                                    "domain": "Chemistry",
                                    "topics": [
                                        {
                                            "title": "Covalent Bonding & Functional Groups",
                                            "code": "CBSE-10-SCI-CH03-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH03-T01"],
                                            "subtopics": ["Catenation and tetravalency", "Homologous series and functional groups", "Soaps, detergents and micelle formation"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-03-01", "statement": "Differentiate functional isomerism and explain saponification and micelle action", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: World of Living",
                            "code": "CBSE-10-SCI-U2",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 4,
                                    "title": "Life Processes",
                                    "code": "CBSE-10-SCI-CH04",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Nutrition, Respiration, Transport & Excretion",
                                            "code": "CBSE-10-SCI-CH04-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH04-T01"],
                                            "subtopics": ["Autotrophic photosynthesis light/dark phases", "Aerobic vs anaerobic glycolysis", "Double circulation in human heart", "Nephron filtration in kidneys"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-04-01", "statement": "Trace systemic double circulation of oxygenated blood and nephron urine formation", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 5,
                                    "title": "Heredity and Evolution",
                                    "code": "CBSE-10-SCI-CH05",
                                    "domain": "Biology",
                                    "topics": [
                                        {
                                            "title": "Mendelian Inheritance & Sex Determination",
                                            "code": "CBSE-10-SCI-CH05-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH04-T01"],
                                            "subtopics": ["Mendel laws of inheritance", "Monohybrid 3:1 and Dihybrid 9:3:3:1 crosses", "XY chromosomal sex determination in humans"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-05-01", "statement": "Predict genotype and phenotype ratios using Punnett squares for monohybrid and dihybrid crosses", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Natural Phenomena & Effects of Current",
                            "code": "CBSE-10-SCI-U3",
                            "weightage_marks": 30,
                            "chapters": [
                                {
                                    "chapter_number": 6,
                                    "title": "Light – Reflection and Refraction",
                                    "code": "CBSE-10-SCI-CH06",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Spherical Mirrors & Lens Formula",
                                            "code": "CBSE-10-SCI-CH06-T01",
                                            "prerequisites": ["CBSE-08-SCI-CH10-T01"],
                                            "subtopics": ["Mirror formula 1/f = 1/v + 1/u", "Refractive index and Snell's Law", "Lens formula 1/f = 1/v - 1/u and power of lens"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-06-01", "statement": "Trace ray diagrams and calculate focal length, magnification, and image distance for concave and convex lenses", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 7,
                                    "title": "Electricity",
                                    "code": "CBSE-10-SCI-CH07",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Ohm's Law, Resistance & Joule's Heating",
                                            "code": "CBSE-10-SCI-CH07-T01",
                                            "prerequisites": ["CBSE-08-SCI-CH06-T01"],
                                            "subtopics": ["Ohm's Law V = IR", "Resistivity and factors affecting resistance", "Series and parallel combinations", "Joule's heating H = I^2 R t"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-07-01", "statement": "Calculate equivalent resistance and power consumption in mixed series-parallel DC circuits", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 8,
                                    "title": "Magnetic Effects of Electric Current",
                                    "code": "CBSE-10-SCI-CH08",
                                    "domain": "Physics",
                                    "topics": [
                                        {
                                            "title": "Magnetic Field, Fleming's Rules & Solenoid",
                                            "code": "CBSE-10-SCI-CH08-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH07-T01"],
                                            "subtopics": ["Field lines of straight wire and solenoid", "Fleming's Left-Hand Rule and electric motor principle", "Electromagnetic induction and domestic electric circuits"],
                                            "learning_outcomes": [
                                                {"code": "LO-10-SCI-08-01", "statement": "Apply Fleming's left hand rule to determine force direction on current-carrying conductors in magnetic fields", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # =========================================================================
        # CLASS 11 (CBSE 2026-27): Distinct Subjects: Math, Physics, Chemistry, Biology
        # =========================================================================
        {
            "class_number": 11,
            "title": "Class 11",
            "code": "CBSE-2026-CLASS-11",
            "description": "CBSE Class 11 Senior Secondary Curriculum 2026-27",
            "order_index": 4,
            "subjects": [
                {
                    "name": "Mathematics",
                    "code": "CBSE-11-MATH",
                    "is_integrated_science": False,
                    "description": "CBSE Class 11 Mathematics",
                    "order_index": 1,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Sets and Functions",
                            "code": "CBSE-11-MATH-U1",
                            "weightage_marks": 23,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Sets & Relations",
                                    "code": "CBSE-11-MATH-CH01",
                                    "topics": [
                                        {
                                            "title": "Set Operations, Venn Diagrams & Cartesian Products",
                                            "code": "CBSE-11-MATH-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Subsets and power sets", "Union, intersection, complement", "Cartesian product A x B"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-MATH-01-01", "statement": "Apply De Morgan's laws and compute domain and range of relations", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Trigonometric Functions",
                                    "code": "CBSE-11-MATH-CH02",
                                    "topics": [
                                        {
                                            "title": "Compound Angles & Multiple Angles",
                                            "code": "CBSE-11-MATH-CH02-T01",
                                            "prerequisites": ["CBSE-10-MATH-CH06-T01"],
                                            "subtopics": ["Radian measure", "sin(x+y), cos(x+y), tan(x+y)", "Multiple angle formulas 2x and 3x"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-MATH-02-01", "statement": "Prove compound and multiple angle trigonometric identities in radian measure", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Algebra",
                            "code": "CBSE-11-MATH-U2",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Complex Numbers & Quadratic Equations",
                                    "code": "CBSE-11-MATH-CH03",
                                    "topics": [
                                        {
                                            "title": "Modulus, Conjugate & Argand Plane",
                                            "code": "CBSE-11-MATH-CH03-T01",
                                            "prerequisites": ["CBSE-10-MATH-CH04-T01"],
                                            "subtopics": ["Algebra of complex numbers a + ib", "Modulus |z| and conjugate z*", "Polar representation"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-MATH-03-01", "statement": "Compute modulus and argument and solve quadratics with negative discriminants", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Permutations and Combinations",
                                    "code": "CBSE-11-MATH-CH04",
                                    "topics": [
                                        {
                                            "title": "Fundamental Principle of Counting & Combinatorics",
                                            "code": "CBSE-11-MATH-CH04-T01",
                                            "prerequisites": [],
                                            "subtopics": ["nPr formula", "nCr formula and properties", "Arrangements with repetition constraints"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-MATH-04-01", "statement": "Solve complex arrangement and selection problems with positional constraints", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Calculus",
                            "code": "CBSE-11-MATH-U3",
                            "weightage_marks": 12,
                            "chapters": [
                                {
                                    "chapter_number": 5,
                                    "title": "Limits and Derivatives",
                                    "code": "CBSE-11-MATH-CH05",
                                    "topics": [
                                        {
                                            "title": "Standard Limits & First Principles Differentiation",
                                            "code": "CBSE-11-MATH-CH05-T01",
                                            "prerequisites": ["CBSE-11-MATH-CH01-T01"],
                                            "subtopics": ["Intuitive idea of limits", "lim (x^n-a^n)/(x-a) and lim sinx/x = 1", "Derivative from first principle", "Product and quotient rules"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-MATH-05-01", "statement": "Evaluate indeterminate algebraic and trigonometric limits and differentiate from first principles", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Physics",
                    "code": "CBSE-11-PHYS",
                    "is_integrated_science": False,
                    "description": "CBSE Class 11 Physics (Theoretical & Practical)",
                    "order_index": 2,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Kinematics & Laws of Motion",
                            "code": "CBSE-11-PHYS-U1",
                            "weightage_marks": 23,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Motion in a Straight Line & Plane",
                                    "code": "CBSE-11-PHYS-CH01",
                                    "topics": [
                                        {
                                            "title": "Vectors, Relative Velocity & Projectile Motion",
                                            "code": "CBSE-11-PHYS-CH01-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH06-T01"],
                                            "subtopics": ["Vector addition and dot/cross products", "Projectile trajectory equation", "Maximum height and horizontal range"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-PHYS-01-01", "statement": "Derive trajectory, time of flight, and horizontal range for 2D projectile motion", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Laws of Motion",
                                    "code": "CBSE-11-PHYS-CH02",
                                    "topics": [
                                        {
                                            "title": "Free Body Diagrams & Friction Dynamics",
                                            "code": "CBSE-11-PHYS-CH02-T01",
                                            "prerequisites": ["CBSE-11-PHYS-CH01-T01"],
                                            "subtopics": ["Newton laws in vector form", "Equilibrium of concurrent forces", "Banking of circular roads"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-PHYS-02-01", "statement": "Calculate optimum and maximum safe speed on banked circular roads with friction", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Work, Energy, Gravitation & Thermodynamics",
                            "code": "CBSE-11-PHYS-U2",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Work, Energy and Power",
                                    "code": "CBSE-11-PHYS-CH03",
                                    "topics": [
                                        {
                                            "title": "Work-Energy Theorem & Collisions",
                                            "code": "CBSE-11-PHYS-CH03-T01",
                                            "prerequisites": ["CBSE-11-PHYS-CH02-T01"],
                                            "subtopics": ["Work done by variable force", "Potential energy of spring 1/2 k x^2", "Elastic and inelastic collisions in 1D"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-PHYS-03-01", "statement": "Solve 1D elastic collisions using conservation of kinetic energy and momentum", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Thermodynamics",
                                    "code": "CBSE-11-PHYS-CH04",
                                    "topics": [
                                        {
                                            "title": "First & Second Laws of Thermodynamics",
                                            "code": "CBSE-11-PHYS-CH04-T01",
                                            "prerequisites": [],
                                            "subtopics": ["First law dQ = dU + dW", "Isothermal and adiabatic processes", "Carnot engine efficiency"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-PHYS-04-01", "statement": "Calculate work done in isothermal and adiabatic gas expansions and Carnot cycle efficiency", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Chemistry",
                    "code": "CBSE-11-CHEM",
                    "is_integrated_science": False,
                    "description": "CBSE Class 11 Chemistry",
                    "order_index": 3,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Physical & Inorganic Chemistry",
                            "code": "CBSE-11-CHEM-U1",
                            "weightage_marks": 35,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Structure of Atom",
                                    "code": "CBSE-11-CHEM-CH01",
                                    "topics": [
                                        {
                                            "title": "Quantum Mechanical Model & Orbitals",
                                            "code": "CBSE-11-CHEM-CH01-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH03-T01"],
                                            "subtopics": ["de Broglie wavelength lambda = h/p", "Heisenberg uncertainty principle", "Quantum numbers (n, l, m, s)", "Aufbau principle and Hund rule"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-CHEM-01-01", "statement": "Write electronic configurations using quantum numbers and Pauli exclusion principle", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Chemical Bonding & Molecular Structure",
                                    "code": "CBSE-11-CHEM-CH02",
                                    "topics": [
                                        {
                                            "title": "VSEPR, Hybridization & Molecular Orbital Theory",
                                            "code": "CBSE-11-CHEM-CH02-T01",
                                            "prerequisites": ["CBSE-11-CHEM-CH01-T01"],
                                            "subtopics": ["Lewis structures and formal charge", "VSEPR molecular geometries", "sp, sp2, sp3 hybridization", "MOT bond order for homonuclear diatomics"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-CHEM-02-01", "statement": "Predict molecular geometry, dipole moments, and MOT bond order of diatomic molecules", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Organic Chemistry",
                            "code": "CBSE-11-CHEM-U2",
                            "weightage_marks": 35,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Organic Chemistry: Basic Principles & Techniques",
                                    "code": "CBSE-11-CHEM-CH03",
                                    "topics": [
                                        {
                                            "title": "IUPAC Nomenclature, Isomerism & Electron Displacement",
                                            "code": "CBSE-11-CHEM-CH03-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH03-T01"],
                                            "subtopics": ["Structural and stereoisomerism", "Inductive, electromeric, resonance and hyperconjugation effects", "Carbocation and free radical stability"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-CHEM-03-01", "statement": "Identify functional and position isomerism and rationalize carbocation stability via resonance and hyperconjugation", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Biology",
                    "code": "CBSE-11-BIO",
                    "is_integrated_science": False,
                    "description": "CBSE Class 11 Biology",
                    "order_index": 4,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Cell Biology & Physiology",
                            "code": "CBSE-11-BIO-U1",
                            "weightage_marks": 40,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Cell: Structure and Function",
                                    "code": "CBSE-11-BIO-CH01",
                                    "topics": [
                                        {
                                            "title": "Biomolecules & Cell Cycle (Mitosis/Meiosis)",
                                            "code": "CBSE-11-BIO-CH01-T01",
                                            "prerequisites": ["CBSE-09-SCI-CH04-T01"],
                                            "subtopics": ["Proteins, carbohydrates, lipids, nucleic acids", "Enzyme kinetics and activation energy", "Phases of cell cycle: G1, S, G2, M", "Stages of Meiosis I crossing over"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-BIO-01-01", "statement": "Explain enzyme competitive inhibition and significance of crossing over in pachytene meiosis I", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Plant Physiology",
                                    "code": "CBSE-11-BIO-CH02",
                                    "topics": [
                                        {
                                            "title": "Photosynthesis in Higher Plants",
                                            "code": "CBSE-11-BIO-CH02-T01",
                                            "prerequisites": ["CBSE-11-BIO-CH01-T01"],
                                            "subtopics": ["Z-scheme of light reactions", "Calvin C3 cycle and RuBisCO", "C4 pathway Hatch-Slack adaptation"],
                                            "learning_outcomes": [
                                                {"code": "LO-11-BIO-02-01", "statement": "Differentiate C3 and C4 photosynthetic pathways and describe photorespiration prevention", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # =========================================================================
        # CLASS 12 (CBSE 2026-27): Distinct Subjects: Math, Physics, Chemistry, Biology
        # =========================================================================
        {
            "class_number": 12,
            "title": "Class 12",
            "code": "CBSE-2026-CLASS-12",
            "description": "CBSE Class 12 Senior Secondary Board Curriculum 2026-27",
            "order_index": 5,
            "subjects": [
                {
                    "name": "Mathematics",
                    "code": "CBSE-12-MATH",
                    "is_integrated_science": False,
                    "description": "CBSE Class 12 Board Mathematics",
                    "order_index": 1,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Relations, Functions & Algebra",
                            "code": "CBSE-12-MATH-U1",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Relations and Functions",
                                    "code": "CBSE-12-MATH-CH01",
                                    "topics": [
                                        {
                                            "title": "Equivalence Relations & Bijective Functions",
                                            "code": "CBSE-12-MATH-CH01-T01",
                                            "prerequisites": ["CBSE-11-MATH-CH01-T01"],
                                            "subtopics": ["Reflexive, symmetric, transitive relations", "One-one (injective) and onto (surjective) functions", "Inverse trigonometric principal values"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-MATH-01-01", "statement": "Verify equivalence relations and compute bijective function inverses", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Matrices and Determinants",
                                    "code": "CBSE-12-MATH-CH02",
                                    "topics": [
                                        {
                                            "title": "Matrix Inversion & System of Linear Equations",
                                            "code": "CBSE-12-MATH-CH02-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Matrix multiplication properties", "Adjoint and inverse A^-1 = adj(A)/|A|", "Solving AX = B matrix method"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-MATH-02-01", "statement": "Solve consistent three-variable systems of equations using matrix inversion", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Calculus",
                            "code": "CBSE-12-MATH-U2",
                            "weightage_marks": 35,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Continuity and Differentiability",
                                    "code": "CBSE-12-MATH-CH03",
                                    "topics": [
                                        {
                                            "title": "Chain Rule, Implicit & Logarithmic Differentiation",
                                            "code": "CBSE-12-MATH-CH03-T01",
                                            "prerequisites": ["CBSE-11-MATH-CH05-T01"],
                                            "subtopics": ["Continuity at a point", "Chain rule of differentiation", "Logarithmic differentiation of variable powers", "Parametric second derivatives"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-MATH-03-01", "statement": "Differentiate complex logarithmic and parametric functions to evaluate second-order derivatives", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Integrals",
                                    "code": "CBSE-12-MATH-CH04",
                                    "topics": [
                                        {
                                            "title": "Indefinite Integrals & Integration by Parts",
                                            "code": "CBSE-12-MATH-CH04-T01",
                                            "prerequisites": ["CBSE-12-MATH-CH03-T01"],
                                            "subtopics": ["Integration by substitution", "Partial fractions integration", "Integration by parts formula", "Definite integral properties"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-MATH-04-01", "statement": "Evaluate definite and indefinite integrals using substitution, parts, and symmetry properties", "bloom_level": "EVALUATE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 3,
                            "title": "Unit III: Vectors & 3D Geometry",
                            "code": "CBSE-12-MATH-U3",
                            "weightage_marks": 20,
                            "chapters": [
                                {
                                    "chapter_number": 5,
                                    "title": "Vector Algebra & 3D Geometry",
                                    "code": "CBSE-12-MATH-CH05",
                                    "topics": [
                                        {
                                            "title": "Scalar & Vector Products, Line in 3D Space",
                                            "code": "CBSE-12-MATH-CH05-T01",
                                            "prerequisites": ["CBSE-11-PHYS-CH01-T01"],
                                            "subtopics": ["Dot product and cross product geometry", "Direction cosines and ratios", "Vector and Cartesian equation of a line", "Shortest distance between skew lines"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-MATH-05-01", "statement": "Calculate the shortest perpendicular distance between two skew lines in 3D space", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Physics",
                    "code": "CBSE-12-PHYS",
                    "is_integrated_science": False,
                    "description": "CBSE Class 12 Board Physics",
                    "order_index": 2,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Electrostatics & Current Electricity",
                            "code": "CBSE-12-PHYS-U1",
                            "weightage_marks": 28,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Electric Charges and Fields",
                                    "code": "CBSE-12-PHYS-CH01",
                                    "topics": [
                                        {
                                            "title": "Coulomb's Law, Dipole & Gauss's Theorem",
                                            "code": "CBSE-12-PHYS-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Coulomb law in vector form", "Electric field of dipole on axial and equatorial lines", "Gauss law flux and applications to infinite wire and sheet"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-PHYS-01-01", "statement": "Apply Gauss's law to derive electric field intensity of infinite uniformly charged planes and wires", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Current Electricity",
                                    "code": "CBSE-12-PHYS-CH02",
                                    "topics": [
                                        {
                                            "title": "Drift Velocity, Kirchhoff's Laws & Wheatstone Bridge",
                                            "code": "CBSE-12-PHYS-CH02-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH07-T01"],
                                            "subtopics": ["Drift velocity formula vd = -eE tau / m", "Kirchhoff junction and loop rules", "Wheatstone bridge balanced condition P/Q = R/S"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-PHYS-02-01", "statement": "Analyze multi-loop electrical networks using Kirchhoff's voltage and current laws", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Optics & Modern Physics",
                            "code": "CBSE-12-PHYS-U2",
                            "weightage_marks": 27,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Ray Optics and Optical Instruments",
                                    "code": "CBSE-12-PHYS-CH03",
                                    "topics": [
                                        {
                                            "title": "Total Internal Reflection & Lens Maker's Formula",
                                            "code": "CBSE-12-PHYS-CH03-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH06-T01"],
                                            "subtopics": ["Critical angle and optical fibres", "Refraction at spherical surfaces", "Lens maker formula 1/f = (mu-1)(1/R1 - 1/R2)", "Compound microscope magnification"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-PHYS-03-01", "statement": "Derive Lens Maker's formula and calculate resolving power of compound microscopes", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 4,
                                    "title": "Dual Nature of Radiation and Matter",
                                    "code": "CBSE-12-PHYS-CH04",
                                    "topics": [
                                        {
                                            "title": "Photoelectric Effect & Einstein's Equation",
                                            "code": "CBSE-12-PHYS-CH04-T01",
                                            "prerequisites": ["CBSE-11-CHEM-CH01-T01"],
                                            "subtopics": ["Hertz and Lenard observations", "Einstein photoelectric equation h*nu = Phi + Kmax", "de Broglie wavelength of accelerated electrons"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-PHYS-04-01", "statement": "Apply Einstein's photoelectric equation to stopping potential and threshold frequency graphs", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Chemistry",
                    "code": "CBSE-12-CHEM",
                    "is_integrated_science": False,
                    "description": "CBSE Class 12 Board Chemistry",
                    "order_index": 3,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Physical Chemistry",
                            "code": "CBSE-12-CHEM-U1",
                            "weightage_marks": 25,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Solutions",
                                    "code": "CBSE-12-CHEM-CH01",
                                    "topics": [
                                        {
                                            "title": "Raoult's Law & Colligative Properties",
                                            "code": "CBSE-12-CHEM-CH01-T01",
                                            "prerequisites": [],
                                            "subtopics": ["Henry's law of gas solubility", "Raoult law for volatile and non-volatile solutes", "Depression in freezing point and Osmotic pressure", "van 't Hoff factor i"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-CHEM-01-01", "statement": "Calculate molar mass of solutes from colligative properties adjusted by van 't Hoff factor", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "chapter_number": 2,
                                    "title": "Electrochemistry",
                                    "code": "CBSE-12-CHEM-CH02",
                                    "topics": [
                                        {
                                            "title": "Nernst Equation & Kohlrausch's Law",
                                            "code": "CBSE-12-CHEM-CH02-T01",
                                            "prerequisites": ["CBSE-11-CHEM-CH02-T01"],
                                            "subtopics": ["Electrochemical cell EMF", "Nernst equation Ecell = E0 - 0.0591/n logQ", "Kohlrausch law of independent migration of ions"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-CHEM-02-01", "statement": "Calculate cell potential and equilibrium constants using the Nernst equation", "bloom_level": "APPLY"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "unit_number": 2,
                            "title": "Unit II: Organic Chemistry",
                            "code": "CBSE-12-CHEM-U2",
                            "weightage_marks": 35,
                            "chapters": [
                                {
                                    "chapter_number": 3,
                                    "title": "Aldehydes, Ketones and Carboxylic Acids",
                                    "code": "CBSE-12-CHEM-CH03",
                                    "topics": [
                                        {
                                            "title": "Nucleophilic Addition & Name Reactions",
                                            "code": "CBSE-12-CHEM-CH03-T01",
                                            "prerequisites": ["CBSE-11-CHEM-CH03-T01"],
                                            "subtopics": ["Aldol condensation and Cannizzaro reaction", "Nucleophilic addition to carbonyl >C=O", "Tollens and Fehling distinction tests"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-CHEM-03-01", "statement": "Distinguish aldehydes from ketones and predict aldol condensation and Cannizzaro products", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Biology",
                    "code": "CBSE-12-BIO",
                    "is_integrated_science": False,
                    "description": "CBSE Class 12 Board Biology",
                    "order_index": 4,
                    "units": [
                        {
                            "unit_number": 1,
                            "title": "Unit I: Reproduction & Genetics",
                            "code": "CBSE-12-BIO-U1",
                            "weightage_marks": 35,
                            "chapters": [
                                {
                                    "chapter_number": 1,
                                    "title": "Molecular Basis of Inheritance",
                                    "code": "CBSE-12-BIO-CH01",
                                    "topics": [
                                        {
                                            "title": "DNA Replication, Transcription & Genetic Code",
                                            "code": "CBSE-12-BIO-CH01-T01",
                                            "prerequisites": ["CBSE-10-SCI-CH05-T01"],
                                            "subtopics": ["Double helix structure of DNA", "Semi-conservative replication Meselson-Stahl", "Transcription in prokaryotes vs eukaryotes", "Lac Operon regulation mechanism"],
                                            "learning_outcomes": [
                                                {"code": "LO-12-BIO-01-01", "statement": "Explain the lac operon positive and negative regulation mechanism in E. coli", "bloom_level": "ANALYZE"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
