"""Fake in-memory knowledge base for the demo.

Mirrors the shape of the Supabase `knowledge_base` table (category, question,
answer, source, verified, usage_count) but needs no DB connection — so the demo
returns curated, verified answers instantly and never hallucinates policy.

Swap `get_knowledge` for a real Supabase query later; the return shape stays the
same.
"""

# Each entry is a verified Q&A an advisor has already vetted.
KNOWLEDGE_BASE = [
    {
        "category": "add_drop",
        "question": "How does dropping a course work and what are the consequences?",
        "answer": (
            "Students may drop a course without a 'W' until the posted add/drop "
            "deadline (typically the first ~2 weeks). After that, a drop shows as "
            "a 'W' until the withdrawal deadline. Dropping below 12 credit hours "
            "can affect full-time status, financial aid, scholarships, and housing."
        ),
        "source": "https://onestop.utk.edu/registration-records/add-drop-classes/",
        "verified": True,
        "usage_count": 47,
    },
    {
        "category": "major_change",
        "question": "How does a student change their major?",
        "answer": (
            "Major changes are processed through the student's college advising "
            "office. The student should meet with an advisor in the target program "
            "to confirm they meet entry requirements (some majors are restricted or "
            "GPA-gated) before the change is submitted."
        ),
        "source": "https://catalog.utk.edu/",
        "verified": True,
        "usage_count": 31,
    },
    {
        "category": "failing_class",
        "question": "What should a student do if they are failing a course?",
        "answer": (
            "Refer the student to free tutoring and the Academic Success Center "
            "early. Remind them of the withdrawal deadline if dropping is on the "
            "table. Repeated failures can trigger academic probation, so check the "
            "student's standing before advising next steps."
        ),
        "source": "https://academicsupport.utk.edu/",
        "verified": True,
        "usage_count": 58,
    },
    {
        "category": "financial",
        "question": "How do dropped courses or low grades affect financial aid?",
        "answer": (
            "Financial aid requires Satisfactory Academic Progress (SAP): a minimum "
            "GPA and a course-completion rate. Dropping or failing courses can put "
            "aid at risk. Students who lose aid can file a SAP appeal — refer them "
            "to the Financial Aid office."
        ),
        "source": "https://financialaid.utk.edu/sap/",
        "verified": True,
        "usage_count": 39,
    },
    {
        "category": "mental_health",
        "question": "Where should a student go for mental health support?",
        "answer": (
            "Refer the student to the UTK Counseling Center, which offers free "
            "confidential counseling and 24/7 crisis support. If the email suggests "
            "the student may be in immediate danger, treat it as urgent and surface "
            "crisis resources right away."
        ),
        "source": "https://counselingcenter.utk.edu/",
        "verified": True,
        "usage_count": 22,
    },
    {
        "category": "general",
        "question": "Where can a student get general advising help?",
        "answer": (
            "Direct the student to One Stop Student Services for general questions, "
            "or to their college advising office for program-specific guidance. "
            "Point them to the UTK catalog for official policy details."
        ),
        "source": "https://catalog.utk.edu/",
        "verified": True,
        "usage_count": 15,
    },
]


def get_knowledge(category: str) -> dict | None:
    """Return the best verified KB entry for a category, or None if there isn't one.

    Picks the most-used verified entry, mirroring an
    `.eq("verified", True).order("usage_count", desc=True).limit(1)` query.
    """
    matches = [
        entry
        for entry in KNOWLEDGE_BASE
        if entry["category"] == category and entry["verified"]
    ]
    if not matches:
        return None
    return max(matches, key=lambda e: e["usage_count"])
