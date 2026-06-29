"""Fake DARS (Degree Audit) records for the demo.

In-memory stand-in for a real DARS / registrar API. Keyed by the student's NAME,
because demo emails are seeded into one mailbox (so the sender address is always
the same) — we match on the name that appears in the email body instead.

get_dars(text) scans the email text for a known student name and returns that
record (with the name included), or None if no known name is found.

EVERY student has a rich record — completed_courses (with grades), current_courses,
remaining_required (with prerequisite chains), and an advisor note — so the add-in's
detail popup shows a real transcript for anyone. Course codes are realistic UTK codes
modeled on catalog.utk.edu; verify exact numbers if needed. Listed courses are a
representative sample, not the full transcript (credits_completed is the real total).
"""

DARS = {
    # ─── Jordan Lee — Biology B.S. (gateway chemistry sequence) ─────────────────
    "Jordan Lee": {
        "student_id": "000412877",
        "major": "Biology, B.S.",
        "catalog_year": "2024-2025",
        "standing": "Junior",
        "gpa": 3.42,
        "credits_completed": 61,
        "credits_in_progress": 13,
        "expected_graduation": "Spring 2027",
        "holds": [],
        "completed_courses": [
            {"code": "BIOL 150", "title": "Organismal & Ecological Biology", "credits": 4, "grade": "A"},
            {"code": "BIOL 160", "title": "Cellular & Molecular Biology", "credits": 4, "grade": "B+"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "B"},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
        ],
        "current_courses": [
            {"code": "CHEM 120", "title": "General Chemistry I", "credits": 4},
            {"code": "BIOL 240", "title": "Genetics", "credits": 3},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 2},
        ],
        "remaining_required": [
            {"code": "CHEM 130", "title": "General Chemistry II", "credits": 4, "prereqs": ["CHEM 120"]},
            {"code": "CHEM 350", "title": "Organic Chemistry I", "credits": 3, "prereqs": ["CHEM 130"]},
            {"code": "CHEM 360", "title": "Organic Chemistry II", "credits": 3, "prereqs": ["CHEM 350"]},
            {"code": "BIOL 330", "title": "Cell Biology", "credits": 3, "prereqs": ["BIOL 160", "CHEM 350"]},
        ],
        "note": (
            "Transferred into Biology as a sophomore, so completing the general "
            "chemistry sequence later than usual. CHEM 120 is the gateway: CHEM 130 -> "
            "CHEM 350 (Organic) -> CHEM 360 and BIOL 330 all chain from it, and they are "
            "only offered in sequence. Dropping CHEM 120 now pushes the whole chemistry "
            "chain back a year and delays graduation past Spring 2027. No holds; "
            "full-time at 13 hours (dropping CHEM 120 -> 9 hours, below full-time)."
        ),
        "why": (
            "CHEM 120 is the gateway to the whole chemistry sequence — dropping it "
            "delays graduation past Spring 2027 and drops her below full-time."
        ),
    },

    # ─── Priya Shah — Pre-Nursing (GPA-gated, prereq block) ─────────────────────
    "Priya Shah": {
        "student_id": "000487203",
        "major": "Nursing (pre-major)",
        "catalog_year": "2024-2025",
        "standing": "Sophomore",
        "gpa": 2.71,
        "credits_completed": 44,
        "credits_in_progress": 15,
        "expected_graduation": "Fall 2027 (if admitted to upper-division nursing)",
        "holds": ["Advising Hold"],
        "completed_courses": [
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "B"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "A-"},
            {"code": "CHEM 100", "title": "Introductory Chemistry", "credits": 4, "grade": "C+"},
            {"code": "CFS 210", "title": "Human Development", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
            {"code": "BIOL 229", "title": "Human Anatomy & Physiology I", "credits": 4},
            {"code": "NUTR 100", "title": "Introductory Nutrition", "credits": 3},
            {"code": "PSYC 220", "title": "Lifespan Psychology", "credits": 3},
            {"code": "HIST 221", "title": "US History", "credits": 2},
        ],
        "remaining_required": [
            {"code": "BIOL 239", "title": "Human Anatomy & Physiology II", "credits": 4, "prereqs": ["BIOL 229"]},
            {"code": "MICR 210", "title": "Microbiology", "credits": 4, "prereqs": ["CHEM 100"]},
            {"code": "NURS application", "title": "Upper-division nursing admission", "credits": 0,
             "prereqs": ["STAT 201", "BIOL 229", "BIOL 239", "MICR 210", "NUTR 100"]},
        ],
        "note": (
            "Pre-nursing. To apply to upper-division nursing she must finish the "
            "prerequisite block (A&P I/II, microbiology, statistics, nutrition) AND meet "
            "the 3.0 minimum competitive GPA. Current GPA is 2.71 — below the threshold. "
            "STAT 201 (in progress) is a required prerequisite; dropping it removes a "
            "prereq and pushes her nursing application back a full cycle (application is "
            "annual). An Advising Hold is active and must be cleared before any "
            "registration change can be processed."
        ),
        "why": (
            "STAT 201 is a nursing prerequisite and an Advising Hold blocks changes — "
            "dropping it pushes her nursing application back a full year."
        ),
    },

    # ─── Marcus Bell — Mechanical Engineering B.S. (probation + prereqs) ─────────
    "Marcus Bell": {
        "student_id": "000455119",
        "major": "Mechanical Engineering, B.S.",
        "catalog_year": "2024-2025",
        "standing": "Senior (by hours)",
        "gpa": 1.94,
        "credits_completed": 78,
        "credits_in_progress": 12,
        "expected_graduation": "Spring 2027 (at risk)",
        "holds": ["Bursar Hold"],
        "completed_courses": [
            {"code": "EF 151", "title": "Engineering Fundamentals I", "credits": 4, "grade": "C"},
            {"code": "EF 152", "title": "Engineering Fundamentals II", "credits": 4, "grade": "C-"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "C"},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4, "grade": "D"},
            {"code": "PHYS 231", "title": "Physics for Engineers I", "credits": 4, "grade": "C"},
            {"code": "MSE 201", "title": "Intro to Materials Science", "credits": 3, "grade": "C"},
        ],
        "current_courses": [
            {"code": "ME 231", "title": "Thermodynamics", "credits": 3},
            {"code": "MATH 231", "title": "Differential Equations", "credits": 3},
            {"code": "ME 202", "title": "Dynamics", "credits": 3},
            {"code": "ECE 255", "title": "Electrical Circuits", "credits": 3},
        ],
        "remaining_required": [
            {"code": "ME 321", "title": "Heat Transfer", "credits": 3, "prereqs": ["ME 231"]},
            {"code": "ME 366", "title": "Fluid Mechanics", "credits": 3, "prereqs": ["ME 231", "MATH 231"]},
            {"code": "ME 450", "title": "Senior Capstone Design", "credits": 4, "prereqs": ["ME 321", "ME 366"]},
        ],
        "note": (
            "78 hours completed but a 1.94 cumulative GPA places him on academic "
            "probation (below the 2.0 minimum). Thermodynamics (ME 231, in progress) is "
            "a prerequisite for Heat Transfer (ME 321) and Fluid Mechanics (ME 366), "
            "which both gate the senior capstone (ME 450) — failing or dropping ME 231 "
            "delays graduation by roughly two semesters. A Bursar Hold blocks "
            "registration. Dropping below 12 hours ends full-time status, and his GPA "
            "already puts financial-aid Satisfactory Academic Progress at risk."
        ),
        "why": (
            "ME 231 gates Heat Transfer & Fluid Mechanics, which gate senior capstone — "
            "dropping it delays graduation ~2 semesters."
        ),
    },

    # ─── Taylor Morris — Psychology B.A. (drop-deadline question) ───────────────
    "Taylor Morris": {
        "student_id": "000463012",
        "major": "Psychology, B.A.",
        "standing": "Sophomore",
        "gpa": 3.10,
        "credits_completed": 30,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "A-"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "B+"},
            {"code": "MATH 119", "title": "College Algebra", "credits": 3, "grade": "B"},
            {"code": "SOCI 120", "title": "Social Problems", "credits": 3, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "PSYC 220", "title": "Lifespan Psychology", "credits": 3},
            {"code": "PSYC 295", "title": "Research Methods", "credits": 3},
            {"code": "BIOL 101", "title": "Concepts of Biology", "credits": 4},
            {"code": "HIST 221", "title": "US History I", "credits": 3},
        ],
        "remaining_required": [
            {"code": "PSYC 300", "title": "Statistics in Psychology", "credits": 3, "prereqs": ["PSYC 295"]},
            {"code": "PSYC 320", "title": "Cognitive Psychology", "credits": 3, "prereqs": ["PSYC 300"]},
            {"code": "PSYC 460", "title": "Senior Capstone", "credits": 3, "prereqs": ["PSYC 320"]},
        ],
        "note": (
            "On track with a solid 3.10 GPA. Asking about the add/drop deadline — can "
            "drop without a 'W' until the posted deadline; dropping below 12 hours would "
            "end full-time status."
        ),
    },

    # ─── Sam Rivera — Psychology B.A., exploring a switch to CS ─────────────────
    "Sam Rivera": {
        "student_id": "000471188",
        "major": "Psychology, B.A.",
        "standing": "Junior",
        "gpa": 2.90,
        "credits_completed": 52,
        "credits_in_progress": 12,
        "holds": [],
        "completed_courses": [
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "B+"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "B"},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3, "grade": "C+"},
            {"code": "PSYC 220", "title": "Lifespan Psychology", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "COSC 102", "title": "Intro to Computer Science", "credits": 4},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4},
            {"code": "PSYC 295", "title": "Research Methods", "credits": 3},
        ],
        "remaining_required": [
            {"code": "COSC 202", "title": "Data Structures", "credits": 4, "prereqs": ["COSC 102"]},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4, "prereqs": ["MATH 141"]},
            {"code": "COSC 302", "title": "Algorithms", "credits": 3, "prereqs": ["COSC 202"]},
        ],
        "note": (
            "Wants to switch from Psychology to Computer Science. CS requires the "
            "Calculus sequence and a COSC progression (C or better in each). He's started "
            "COSC 102 and MATH 141; some credits transfer, but switching as a junior "
            "would add roughly 2-3 semesters."
        ),
    },

    # ─── Jamie Chen — Biology B.S., struggling in BIOL 130 ──────────────────────
    "Jamie Chen": {
        "student_id": "000449265",
        "major": "Biology, B.S.",
        "standing": "Sophomore",
        "gpa": 2.55,
        "credits_completed": 40,
        "credits_in_progress": 16,
        "holds": [],
        "completed_courses": [
            {"code": "BIOL 150", "title": "Organismal & Ecological Biology", "credits": 4, "grade": "C+"},
            {"code": "CHEM 120", "title": "General Chemistry I", "credits": 4, "grade": "C"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3, "grade": "B-"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "B+"},
        ],
        "current_courses": [
            {"code": "BIOL 130", "title": "Biodiversity", "credits": 4},
            {"code": "CHEM 130", "title": "General Chemistry II", "credits": 4},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
        ],
        "remaining_required": [
            {"code": "BIOL 240", "title": "Genetics", "credits": 3, "prereqs": ["BIOL 150"]},
            {"code": "CHEM 350", "title": "Organic Chemistry I", "credits": 3, "prereqs": ["CHEM 130"]},
            {"code": "BIOL 330", "title": "Cell Biology", "credits": 3, "prereqs": ["BIOL 240", "CHEM 350"]},
        ],
        "note": (
            "Struggling in BIOL 130 this term. Free tutoring and supplemental "
            "instruction are available through the Student Success Center; the withdrawal "
            "deadline is the cutoff for dropping with a 'W'. GPA (2.55) has room before "
            "the 2.0 line but a failing grade would pull it down."
        ),
    },

    # ─── Devon Parker — Business Administration B.S. (SAP / aid) ────────────────
    "Devon Parker": {
        "student_id": "000438820",
        "major": "Business Administration, B.S.",
        "standing": "Junior",
        "gpa": 2.18,
        "credits_completed": 66,
        "credits_in_progress": 13,
        "holds": [],
        "completed_courses": [
            {"code": "ACCT 200", "title": "Foundations of Accounting", "credits": 3, "grade": "C"},
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "C+"},
            {"code": "BUAD 200", "title": "Intro to Business", "credits": 3, "grade": "C"},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3, "grade": "C-"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "C+"},
        ],
        "current_courses": [
            {"code": "ACCT 210", "title": "Managerial Accounting", "credits": 3},
            {"code": "ECON 207", "title": "Macroeconomics", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
            {"code": "FINC 300", "title": "Principles of Finance", "credits": 3},
        ],
        "remaining_required": [
            {"code": "MGT 300", "title": "Principles of Management", "credits": 3, "prereqs": ["BUAD 200"]},
            {"code": "MARK 300", "title": "Principles of Marketing", "credits": 3, "prereqs": ["ECON 201"]},
            {"code": "FINC 310", "title": "Intermediate Finance", "credits": 3, "prereqs": ["FINC 300", "ACCT 210"]},
        ],
        "note": (
            "GPA of 2.18 is close to the financial-aid Satisfactory Academic Progress "
            "(SAP) minimum, and SAP also tracks completion rate. Worth a check with One "
            "Stop on exactly which SAP requirement is flagged and whether an appeal is "
            "needed."
        ),
    },

    # ─── Riley Adams — English B.A. (planning next semester) ────────────────────
    "Riley Adams": {
        "student_id": "000421746",
        "major": "English, B.A.",
        "standing": "Senior",
        "gpa": 3.61,
        "credits_completed": 90,
        "credits_in_progress": 12,
        "expected_graduation": "Spring 2026",
        "holds": [],
        "completed_courses": [
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "A-"},
            {"code": "ENGL 251", "title": "British Literature I", "credits": 3, "grade": "A"},
            {"code": "ENGL 252", "title": "American Literature", "credits": 3, "grade": "A-"},
            {"code": "HIST 221", "title": "US History I", "credits": 3, "grade": "B+"},
        ],
        "current_courses": [
            {"code": "ENGL 360", "title": "Advanced Composition", "credits": 3},
            {"code": "ENGL 401", "title": "Shakespeare", "credits": 3},
            {"code": "PHIL 110", "title": "Intro to Philosophy", "credits": 3},
            {"code": "ART 100", "title": "Art History Survey", "credits": 3},
        ],
        "remaining_required": [
            {"code": "ENGL 455", "title": "Literary Theory", "credits": 3, "prereqs": ["ENGL 360"]},
            {"code": "ENGL 480", "title": "Senior Seminar", "credits": 3, "prereqs": ["ENGL 455"]},
        ],
        "note": (
            "Strong 3.61 GPA, nearly done. Planning the final-year schedule around the "
            "remaining major requirements (Literary Theory -> Senior Seminar). Best built "
            "from the degree audit plus the registration calendar."
        ),
    },

    # ─── Alex Kim — Computer Science B.S. (academic calendar question) ──────────
    "Alex Kim": {
        "student_id": "000452907",
        "major": "Computer Science, B.S.",
        "standing": "Sophomore",
        "gpa": 3.30,
        "credits_completed": 48,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "COSC 102", "title": "Intro to Computer Science", "credits": 4, "grade": "A"},
            {"code": "COSC 202", "title": "Data Structures", "credits": 4, "grade": "B+"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "B"},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4, "grade": "B+"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "COSC 302", "title": "Data Structures II", "credits": 3},
            {"code": "COSC 311", "title": "Discrete Structures", "credits": 3},
            {"code": "MATH 251", "title": "Matrix Algebra", "credits": 3},
            {"code": "PHYS 231", "title": "Physics for Engineers I", "credits": 4},
        ],
        "remaining_required": [
            {"code": "COSC 312", "title": "Algorithm Analysis", "credits": 3, "prereqs": ["COSC 302", "COSC 311"]},
            {"code": "COSC 360", "title": "Systems Programming", "credits": 3, "prereqs": ["COSC 302"]},
            {"code": "COSC 365", "title": "Programming Languages", "credits": 3, "prereqs": ["COSC 360"]},
        ],
        "note": (
            "On track in the CS sequence with a 3.30 GPA. Asking where to find the "
            "academic calendar and registration dates — registration timing is set by "
            "class standing (time ticket)."
        ),
    },

    # ─── Casey Nguyen — Undecided (mental-health email; responds personally) ────
    "Casey Nguyen": {
        "student_id": "000490011",
        "major": "Undecided",
        "standing": "Freshman",
        "gpa": 3.00,
        "credits_completed": 24,
        "credits_in_progress": 14,
        "holds": [],
        "completed_courses": [
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B+"},
            {"code": "MATH 119", "title": "College Algebra", "credits": 3, "grade": "B"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "A-"},
            {"code": "HIST 221", "title": "US History I", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
            {"code": "SOCI 120", "title": "Social Problems", "credits": 3},
            {"code": "BIOL 101", "title": "Concepts of Biology", "credits": 4},
            {"code": "ART 100", "title": "Art History Survey", "credits": 3},
        ],
        "remaining_required": [
            {"code": "Gen-Ed", "title": "Foreign Language (2 terms)", "credits": 6},
            {"code": "Gen-Ed", "title": "Quantitative Reasoning elective", "credits": 3},
            {"code": "Major", "title": "Declare a major by ~60 hours", "credits": 0},
        ],
        "note": (
            "Undecided major, working through general-education courses. This is a "
            "mental-health email — respond personally and share the UTK Counseling Center "
            "(free, confidential, 24/7); no auto-draft."
        ),
    },

    # ─── Morgan Diaz — Sociology B.A. (critical mental-health email) ────────────
    "Morgan Diaz": {
        "student_id": "000495533",
        "major": "Sociology, B.A.",
        "standing": "Freshman",
        "gpa": 2.80,
        "credits_completed": 18,
        "credits_in_progress": 12,
        "holds": [],
        "completed_courses": [
            {"code": "SOCI 110", "title": "Intro to Sociology", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B-"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "B+"},
        ],
        "current_courses": [
            {"code": "SOCI 120", "title": "Social Problems", "credits": 3},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
            {"code": "MATH 119", "title": "College Algebra", "credits": 3},
            {"code": "BIOL 101", "title": "Concepts of Biology", "credits": 4},
        ],
        "remaining_required": [
            {"code": "SOCI 250", "title": "Research Methods", "credits": 3, "prereqs": ["SOCI 110"]},
            {"code": "SOCI 360", "title": "Social Theory", "credits": 3, "prereqs": ["SOCI 250"]},
        ],
        "note": (
            "Early in the major. This email signals hopelessness — treat as urgent, "
            "respond personally and promptly, and surface the UTK Counseling Center 24/7 "
            "crisis line; escalate if any risk of harm. No auto-draft."
        ),
    },

    # ─── Chris Taylor — History B.A. (complicated hardship situation) ───────────
    "Chris Taylor": {
        "student_id": "000467314",
        "major": "History, B.A.",
        "standing": "Senior",
        "gpa": 2.40,
        "credits_completed": 70,
        "credits_in_progress": 9,
        "holds": [],
        "completed_courses": [
            {"code": "HIST 221", "title": "US History I", "credits": 3, "grade": "C+"},
            {"code": "HIST 222", "title": "US History II", "credits": 3, "grade": "B-"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "C+"},
            {"code": "PHIL 110", "title": "Intro to Philosophy", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "HIST 350", "title": "Modern Europe", "credits": 3},
            {"code": "HIST 360", "title": "US Since 1945", "credits": 3},
            {"code": "POLS 101", "title": "American Government", "credits": 3},
        ],
        "remaining_required": [
            {"code": "HIST 401", "title": "Historical Methods", "credits": 3, "prereqs": ["HIST 221", "HIST 222"]},
            {"code": "HIST 480", "title": "Senior Seminar", "credits": 3, "prereqs": ["HIST 401"]},
        ],
        "note": (
            "Reported a family emergency and three weeks missed this term, with an "
            "instructor who won't accommodate. Options are case-by-case: a hardship/"
            "medical withdrawal or an Incomplete, handled with the instructor and the "
            "Dean of Students. Needs the advisor's judgment."
        ),
        "why": (
            "Missed three weeks from a family emergency — needs a withdrawal vs. "
            "Incomplete decision before the deadline."
        ),
    },

    # ─── Nadia Osei — Chemistry B.S. (AP credit not posted) ─────────────────────
    "Nadia Osei": {
        "student_id": "000501224",
        "major": "Chemistry, B.S.",
        "standing": "Freshman",
        "gpa": 3.55,
        "credits_completed": 14,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "B+"},
            {"code": "HIST 221", "title": "US History I", "credits": 3, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "CHEM 120", "title": "General Chemistry I", "credits": 4},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
            {"code": "BIOL 130", "title": "Biodiversity", "credits": 4},
        ],
        "remaining_required": [
            {"code": "CHEM 130", "title": "General Chemistry II", "credits": 4, "prereqs": ["CHEM 120"]},
            {"code": "CHEM 350", "title": "Organic Chemistry I", "credits": 3, "prereqs": ["CHEM 130"]},
        ],
        "note": (
            "AP Chemistry score of 4 self-reported, but no AP credit is currently posted "
            "to her record. UTK awards CHEM 120 credit for an AP Chemistry score of 4+, "
            "but only after an official College Board score report is received by the "
            "Admissions/Registrar office."
        ),
        "why": (
            "She's taking CHEM 120 now — if her AP credit posts it may be redundant, so "
            "check before the add/drop deadline."
        ),
    },

    # ─── Ethan Brooks — Economics B.A. (retaking failed MATH 141) ───────────────
    "Ethan Brooks": {
        "student_id": "000498771",
        "major": "Economics, B.A.",
        "standing": "Sophomore",
        "gpa": 2.34,
        "credits_completed": 38,
        "credits_in_progress": 13,
        "holds": [],
        "completed_courses": [
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "F"},
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "C+"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "B"},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3, "grade": "C+"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "ECON 207", "title": "Macroeconomics", "credits": 3},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
            {"code": "HIST 221", "title": "US History I", "credits": 3},
        ],
        "remaining_required": [
            {"code": "MATH 141", "title": "Calculus I (repeat)", "credits": 4},
            {"code": "ECON 311", "title": "Microeconomic Theory", "credits": 3, "prereqs": ["ECON 201", "MATH 141"]},
            {"code": "ECON 313", "title": "Macroeconomic Theory", "credits": 3, "prereqs": ["ECON 207", "MATH 141"]},
        ],
        "note": (
            "Failed MATH 141 last term. Eligible for UTK's course-repeat / grade-"
            "replacement policy: on an allowed repeat the most recent grade is counted in "
            "the GPA, while the original attempt stays on the transcript marked as "
            "repeated. Repeats are limited in number."
        ),
        "why": (
            "MATH 141 gates ECON 311/313 — retaking and passing both lifts his GPA and "
            "unblocks the economics theory courses."
        ),
    },

    # ─── Fatima Hassan — Sociology B.A. (incomplete request) ────────────────────
    "Fatima Hassan": {
        "student_id": "000496310",
        "major": "Sociology, B.A.",
        "standing": "Junior",
        "gpa": 3.18,
        "credits_completed": 64,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "SOCI 110", "title": "Intro to Sociology", "credits": 3, "grade": "A-"},
            {"code": "SOCI 120", "title": "Social Problems", "credits": 3, "grade": "B+"},
            {"code": "SOCI 250", "title": "Research Methods", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "SOCI 360", "title": "Social Theory", "credits": 3},
            {"code": "SOCI 410", "title": "Race & Ethnicity", "credits": 3},
            {"code": "PSYC 220", "title": "Lifespan Psychology", "credits": 3},
            {"code": "HIST 221", "title": "US History I", "credits": 3},
        ],
        "remaining_required": [
            {"code": "SOCI 420", "title": "Applied Sociology", "credits": 3, "prereqs": ["SOCI 250"]},
            {"code": "SOCI 460", "title": "Senior Seminar", "credits": 3, "prereqs": ["SOCI 360"]},
        ],
        "note": (
            "Strong record (3.18) but reporting serious family hardship this term. An "
            "Incomplete ('I') is granted only when most of the coursework is done and the "
            "rest can be finished by a set deadline, with the instructor's agreement — it "
            "is not automatic. A hardship withdrawal may be the alternative."
        ),
    },

    # ─── Derek Simmons — Business Administration B.S. (academic probation) ──────
    "Derek Simmons": {
        "student_id": "000493882",
        "major": "Business Administration, B.S.",
        "standing": "Sophomore",
        "gpa": 1.85,
        "credits_completed": 42,
        "credits_in_progress": 13,
        "holds": [],
        "completed_courses": [
            {"code": "ACCT 200", "title": "Foundations of Accounting", "credits": 3, "grade": "D"},
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "C-"},
            {"code": "BUAD 200", "title": "Intro to Business", "credits": 3, "grade": "D+"},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3, "grade": "C"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "C+"},
        ],
        "current_courses": [
            {"code": "ECON 207", "title": "Macroeconomics", "credits": 3},
            {"code": "ACCT 210", "title": "Managerial Accounting", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
        ],
        "remaining_required": [
            {"code": "FINC 300", "title": "Principles of Finance", "credits": 3, "prereqs": ["ACCT 200", "ECON 201"]},
            {"code": "MGT 300", "title": "Principles of Management", "credits": 3, "prereqs": ["BUAD 200"]},
            {"code": "MARK 300", "title": "Principles of Marketing", "credits": 3, "prereqs": ["ECON 201"]},
        ],
        "note": (
            "Cumulative GPA of 1.85 is below the 2.0 minimum, which is why he was placed "
            "on academic probation. Returning to good standing means raising the "
            "cumulative GPA to 2.0+, usually with an academic-recovery plan and a "
            "possible cap on credit hours."
        ),
        "why": (
            "A 1.85 GPA puts him on academic probation — he needs a recovery plan to get "
            "back above 2.0."
        ),
    },

    # ─── Leila Park — Computer Science B.S. (credit overload) ───────────────────
    "Leila Park": {
        "student_id": "000502907",
        "major": "Computer Science, B.S.",
        "standing": "Junior",
        "gpa": 3.72,
        "credits_completed": 70,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "COSC 102", "title": "Intro to Computer Science", "credits": 4, "grade": "A"},
            {"code": "COSC 202", "title": "Data Structures", "credits": 4, "grade": "A"},
            {"code": "COSC 311", "title": "Discrete Structures", "credits": 3, "grade": "A"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "A"},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "COSC 302", "title": "Data Structures II", "credits": 3},
            {"code": "COSC 360", "title": "Systems Programming", "credits": 3},
            {"code": "COSC 340", "title": "Software Engineering", "credits": 3},
            {"code": "MATH 251", "title": "Matrix Algebra", "credits": 3},
        ],
        "remaining_required": [
            {"code": "COSC 312", "title": "Algorithm Analysis", "credits": 3, "prereqs": ["COSC 302", "COSC 311"]},
            {"code": "COSC 365", "title": "Programming Languages", "credits": 3, "prereqs": ["COSC 360"]},
            {"code": "COSC 425", "title": "Capstone", "credits": 4, "prereqs": ["COSC 312", "COSC 365"]},
        ],
        "note": (
            "High GPA (3.72). Standard full-time load is up to 18 hours; an overload to "
            "19-21 hours requires advisor/college approval and typically a GPA at or "
            "above ~3.0 — she comfortably qualifies."
        ),
    },

    # ─── Owen Murphy — History B.A. (on-track-to-graduate check) ────────────────
    "Owen Murphy": {
        "student_id": "000455901",
        "major": "History, B.A.",
        "standing": "Senior",
        "gpa": 3.30,
        "credits_completed": 108,
        "credits_in_progress": 12,
        "expected_graduation": "Spring 2026",
        "holds": [],
        "completed_courses": [
            {"code": "HIST 221", "title": "US History I", "credits": 3, "grade": "B+"},
            {"code": "HIST 222", "title": "US History II", "credits": 3, "grade": "A-"},
            {"code": "HIST 350", "title": "Modern Europe", "credits": 3, "grade": "B+"},
            {"code": "HIST 360", "title": "US Since 1945", "credits": 3, "grade": "A-"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
        ],
        "current_courses": [
            {"code": "HIST 401", "title": "Historical Methods", "credits": 3},
            {"code": "HIST 480", "title": "Senior Seminar", "credits": 3},
            {"code": "POLS 101", "title": "American Government", "credits": 3},
            {"code": "ART 100", "title": "Art History Survey", "credits": 3},
        ],
        "remaining_required": [
            {"code": "HIST 460", "title": "Upper-division elective", "credits": 3, "prereqs": ["HIST 350"]},
            {"code": "Vol Core", "title": "Expanded Perspectives elective", "credits": 3},
        ],
        "note": (
            "On track by hours (108 + 12 in progress, toward 120). To graduate in May he "
            "must file the graduation application by the posted deadline and complete a "
            "final degree audit with his advisor to confirm no remaining requirements are "
            "outstanding."
        ),
    },

    # ─── Simone Grant — Economics B.A. (adding a second major) ──────────────────
    "Simone Grant": {
        "student_id": "000504113",
        "major": "Economics, B.A.",
        "standing": "Sophomore",
        "gpa": 3.21,
        "credits_completed": 46,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "B+"},
            {"code": "ECON 207", "title": "Macroeconomics", "credits": 3, "grade": "B"},
            {"code": "MATH 125", "title": "Basic Calculus", "credits": 3, "grade": "B+"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A-"},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3, "grade": "B"},
        ],
        "current_courses": [
            {"code": "ECON 311", "title": "Microeconomic Theory", "credits": 3},
            {"code": "POLS 101", "title": "American Government", "credits": 3},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
            {"code": "HIST 221", "title": "US History I", "credits": 3},
        ],
        "remaining_required": [
            {"code": "ECON 313", "title": "Macroeconomic Theory", "credits": 3, "prereqs": ["ECON 207"]},
            {"code": "ECON 423", "title": "Econometrics", "credits": 3, "prereqs": ["ECON 311", "STAT 201"]},
            {"code": "POLS 250", "title": "Political Analysis (2nd major)", "credits": 3, "prereqs": ["POLS 101"]},
        ],
        "note": (
            "Wants to add Political Science as a second major. A second major is allowed; "
            "it's declared through that department's advising office and both sets of "
            "requirements must be completed, which can extend the time to graduate. As a "
            "sophomore she has time to plan it."
        ),
    },

    # ─── Aiden Flores — Marketing B.S. (adding a Spanish minor) ─────────────────
    "Aiden Flores": {
        "student_id": "000500447",
        "major": "Marketing, B.S.",
        "standing": "Junior",
        "gpa": 3.05,
        "credits_completed": 60,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "BUAD 200", "title": "Intro to Business", "credits": 3, "grade": "B"},
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "B-"},
            {"code": "ACCT 200", "title": "Foundations of Accounting", "credits": 3, "grade": "B+"},
            {"code": "MARK 300", "title": "Principles of Marketing", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "MARK 320", "title": "Consumer Behavior", "credits": 3},
            {"code": "MARK 350", "title": "Marketing Research", "credits": 3},
            {"code": "SPAN 211", "title": "Intermediate Spanish I", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
        ],
        "remaining_required": [
            {"code": "MARK 450", "title": "Marketing Strategy", "credits": 3, "prereqs": ["MARK 320"]},
            {"code": "SPAN 311", "title": "Spanish Conversation (minor)", "credits": 3, "prereqs": ["SPAN 211"]},
            {"code": "SPAN 312", "title": "Spanish Composition (minor)", "credits": 3, "prereqs": ["SPAN 311"]},
        ],
        "note": (
            "Wants to add a Spanish minor (already in SPAN 211). Declaring a minor is "
            "done through that department; a minor is typically 15-18 hours, and whether "
            "it delays graduation depends on overlap with electives and remaining "
            "requirements."
        ),
    },

    # ─── Brianna Scott — Psychology B.A. (waitlisted for PSYC 301) ──────────────
    "Brianna Scott": {
        "student_id": "000499205",
        "major": "Psychology, B.A.",
        "standing": "Junior",
        "gpa": 3.40,
        "credits_completed": 66,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "A"},
            {"code": "PSYC 220", "title": "Lifespan Psychology", "credits": 3, "grade": "A-"},
            {"code": "PSYC 295", "title": "Research Methods", "credits": 3, "grade": "B+"},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
        ],
        "current_courses": [
            {"code": "PSYC 300", "title": "Statistics in Psychology", "credits": 3},
            {"code": "PSYC 310", "title": "Abnormal Psychology", "credits": 3},
            {"code": "BIOL 101", "title": "Concepts of Biology", "credits": 4},
            {"code": "ART 100", "title": "Art History Survey", "credits": 3},
        ],
        "remaining_required": [
            {"code": "PSYC 301", "title": "Cognitive Psychology (waitlisted)", "credits": 3, "prereqs": ["PSYC 295"]},
            {"code": "PSYC 460", "title": "Senior Capstone", "credits": 3, "prereqs": ["PSYC 301"]},
        ],
        "note": (
            "#6 on the waitlist for PSYC 301, a required major course (and a prereq for "
            "the capstone). Waitlists clear automatically as students drop; no guarantee. "
            "Backups: another required course this term, a different PSYC 301 section, or "
            "instructor permission to overfill."
        ),
    },

    # ─── Lucas Reyes — International Business B.S. (study abroad + aid) ──────────
    "Lucas Reyes": {
        "student_id": "000497740",
        "major": "International Business, B.S.",
        "standing": "Sophomore",
        "gpa": 3.28,
        "credits_completed": 48,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "BUAD 200", "title": "Intro to Business", "credits": 3, "grade": "B+"},
            {"code": "ECON 201", "title": "Microeconomics", "credits": 3, "grade": "B"},
            {"code": "ACCT 200", "title": "Foundations of Accounting", "credits": 3, "grade": "B-"},
            {"code": "SPAN 211", "title": "Intermediate Spanish I", "credits": 3, "grade": "A"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A-"},
        ],
        "current_courses": [
            {"code": "ECON 207", "title": "Macroeconomics", "credits": 3},
            {"code": "SPAN 311", "title": "Spanish Conversation", "credits": 3},
            {"code": "STAT 201", "title": "Introduction to Statistics", "credits": 3},
            {"code": "MGT 300", "title": "Principles of Management", "credits": 3},
        ],
        "remaining_required": [
            {"code": "IB 300", "title": "International Business", "credits": 3, "prereqs": ["ECON 201"]},
            {"code": "SPAN 312", "title": "Spanish Composition", "credits": 3, "prereqs": ["SPAN 311"]},
            {"code": "FINC 300", "title": "Principles of Finance", "credits": 3, "prereqs": ["ACCT 200"]},
        ],
        "note": (
            "Considering study abroad next fall. On UTK-sponsored/exchange programs "
            "federal and most institutional aid generally still applies, and courses can "
            "count toward the degree if pre-approved — both arranged ahead through the "
            "Programs Abroad office and the advisor. His Spanish track fits well."
        ),
    },

    # ─── Imani Walker — Communications B.A. (disputing a final grade) ───────────
    "Imani Walker": {
        "student_id": "000494418",
        "major": "Communications, B.A.",
        "standing": "Junior",
        "gpa": 3.36,
        "credits_completed": 68,
        "credits_in_progress": 15,
        "holds": [],
        "completed_courses": [
            {"code": "CMST 210", "title": "Public Speaking", "credits": 3, "grade": "A-"},
            {"code": "CMST 240", "title": "Business & Professional Communication", "credits": 3, "grade": "B+"},
            {"code": "JREM 200", "title": "Intro to Media Writing", "credits": 3, "grade": "B"},
            {"code": "ENGL 101", "title": "English Composition I", "credits": 3, "grade": "A"},
            {"code": "PSYC 110", "title": "General Psychology", "credits": 3, "grade": "B+"},
        ],
        "current_courses": [
            {"code": "CMST 320", "title": "Persuasion", "credits": 3},
            {"code": "JREM 300", "title": "Media Ethics", "credits": 3},
            {"code": "CMST 350", "title": "Organizational Communication", "credits": 3},
            {"code": "ENGL 102", "title": "English Composition II", "credits": 3},
        ],
        "remaining_required": [
            {"code": "CMST 460", "title": "Senior Seminar", "credits": 3, "prereqs": ["CMST 320"]},
            {"code": "JREM 400", "title": "Capstone Project", "credits": 3, "prereqs": ["JREM 300"]},
        ],
        "note": (
            "Disputing a final grade she believes was miscalculated. UTK has a formal "
            "grade-appeal procedure: start with the instructor, then escalate to the "
            "department head and college if unresolved, within published deadlines. This "
            "needs the advisor to guide the process, not an auto-reply."
        ),
    },

    # ─── Marcus Carter — Mechanical Engineering B.S. (FERPA: parent's son) ──────
    # The parent (Linda Carter) is asking for grades. The advisor may VIEW this
    # record but must NOT disclose it without the student's written consent.
    "Marcus Carter": {
        "student_id": "000506622",
        "major": "Mechanical Engineering, B.S.",
        "standing": "Sophomore",
        "gpa": 2.05,
        "credits_completed": 40,
        "credits_in_progress": 14,
        "holds": [],
        "completed_courses": [
            {"code": "EF 151", "title": "Engineering Fundamentals I", "credits": 4, "grade": "C"},
            {"code": "EF 152", "title": "Engineering Fundamentals II", "credits": 4, "grade": "C-"},
            {"code": "MATH 141", "title": "Calculus I", "credits": 4, "grade": "C"},
            {"code": "MATH 142", "title": "Calculus II", "credits": 4, "grade": "D+"},
            {"code": "CHEM 120", "title": "General Chemistry I", "credits": 4, "grade": "C"},
        ],
        "current_courses": [
            {"code": "ME 202", "title": "Dynamics", "credits": 3},
            {"code": "MATH 231", "title": "Differential Equations", "credits": 3},
            {"code": "PHYS 231", "title": "Physics for Engineers I", "credits": 4},
            {"code": "EF 230", "title": "Engineering Computing", "credits": 2},
        ],
        "remaining_required": [
            {"code": "ME 231", "title": "Thermodynamics", "credits": 3, "prereqs": ["ME 202"]},
            {"code": "ME 321", "title": "Heat Transfer", "credits": 3, "prereqs": ["ME 231"]},
        ],
        "note": (
            "Parent (Linda Carter) is asking for his grades. FERPA prohibits disclosing a "
            "student's education records to a parent without the student's written "
            "consent, even when the parent pays tuition. The advisor can see this record "
            "but cannot share it with the parent."
        ),
    },
}


def get_dars(text: str) -> dict | None:
    """Find a known student name in the email text and return their record (or None).

    Returns a copy with the matched "name" included, so the frontend can show it.
    """
    if not text:
        return None
    lowered = text.lower()
    for name, record in DARS.items():
        if name.lower() in lowered:
            return {"name": name, **record}
    return None
