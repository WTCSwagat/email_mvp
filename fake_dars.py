"""Fake DARS (Degree Audit) records for the demo.

In-memory stand-in for a real DARS / registrar API. Keyed by the student's NAME,
because demo emails are seeded into one mailbox (so the sender address is always
the same) — we match on the name that appears in the email body instead.

get_dars(text) scans the email text for a known student name and returns that
record (with the name included), or None if no known name is found.

The three demo students (Jordan, Priya, Marcus) have RICH records — full course
lists + prerequisite chains — so the AI can reason about how dropping a course
cascades through the degree (delays, prereqs, GPA/aid impact). Course codes are
realistic UTK codes modeled on catalog.utk.edu; verify exact numbers if needed.
Everyone else has a basic record.
"""

DARS = {
    # ─── RICH: Jordan Lee — Biology B.S. (gateway chemistry sequence) ───────────
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
            "chemistry sequence later than usual. CHEM 120 is the gateway: "
            "CHEM 130 -> CHEM 350 (Organic) -> CHEM 360 and BIOL 330 all chain from "
            "it, and they are only offered in sequence. Dropping CHEM 120 now pushes "
            "the whole chemistry chain back a year and delays graduation past Spring "
            "2027. No holds; full-time at 13 hours (dropping CHEM 120 -> 9 hours, "
            "below full-time)."
        ),
    },

    # ─── RICH: Priya Shah — Pre-Nursing (GPA-gated, prereq block) ───────────────
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
            "prerequisite block (A&P I/II, microbiology, statistics, nutrition) AND "
            "meet the 3.0 minimum competitive GPA. Current GPA is 2.71 — below the "
            "threshold. STAT 201 (in progress) is a required prerequisite; dropping "
            "it removes a prereq and pushes her nursing application back a full cycle "
            "(application is annual). An Advising Hold is active and must be cleared "
            "before any registration change can be processed."
        ),
    },

    # ─── RICH: Marcus Bell — Mechanical Engineering B.S. (probation + prereqs) ──
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
            "probation (below the 2.0 minimum). Thermodynamics (ME 231, in progress) "
            "is a prerequisite for Heat Transfer (ME 321) and Fluid Mechanics "
            "(ME 366), which both gate the senior capstone (ME 450) — failing or "
            "dropping ME 231 delays graduation by roughly two semesters. A Bursar "
            "Hold blocks registration. Dropping below 12 hours ends full-time status, "
            "and his GPA already puts financial-aid Satisfactory Academic Progress at risk."
        ),
    },

    # ─── BASIC: everyone else (name / id / credits / gpa / major / holds) ───────
    "Taylor Morris": {"student_id": "000463012", "credits_completed": 30, "credits_in_progress": 15, "gpa": 3.10, "major": "Psychology, B.A.", "holds": []},
    "Sam Rivera":    {"student_id": "000471188", "credits_completed": 52, "credits_in_progress": 12, "gpa": 2.90, "major": "Psychology, B.A.", "holds": []},
    "Jamie Chen":    {"student_id": "000449265", "credits_completed": 40, "credits_in_progress": 16, "gpa": 2.55, "major": "Biology, B.S.", "holds": []},
    "Devon Parker":  {"student_id": "000438820", "credits_completed": 66, "credits_in_progress": 13, "gpa": 2.18, "major": "Business Administration, B.S.", "holds": []},
    "Riley Adams":   {"student_id": "000421746", "credits_completed": 90, "credits_in_progress": 12, "gpa": 3.61, "major": "English, B.A.", "holds": []},
    "Alex Kim":      {"student_id": "000452907", "credits_completed": 48, "credits_in_progress": 15, "gpa": 3.30, "major": "Computer Science, B.S.", "holds": []},
    "Casey Nguyen":  {"student_id": "000490011", "credits_completed": 24, "credits_in_progress": 14, "gpa": 3.00, "major": "Undecided", "holds": []},
    "Morgan Diaz":   {"student_id": "000495533", "credits_completed": 18, "credits_in_progress": 12, "gpa": 2.80, "major": "Sociology, B.A.", "holds": []},
    "Chris Taylor":  {"student_id": "000467314", "credits_completed": 70, "credits_in_progress": 9,  "gpa": 2.40, "major": "History, B.A.", "holds": []},
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
