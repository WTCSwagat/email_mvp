"""Fake DARS (Degree Audit) records for the demo.

In-memory stand-in for a real DARS / registrar API. Keyed by the student's
email (the email `sender`), so an inbound email can be matched to a record.

Swap `get_dars` for a real API call later (e.g. requests.get(...)); the return
shape stays the same. This is the FERPA-sensitive piece in production — fake here.
"""

# Three deliberately varied scenarios:
#   - jordan: clean, full-time, no holds  -> judge can fully answer ("yes")
#   - priya:  advising hold               -> "partly" (hold needs the advisor)
#   - marcus: low GPA + bursar hold       -> "partly" (aid/standing risk)
# Any sender NOT in here returns None -> judge runs without DARS (fallback).
DARS = {
    "jordan.lee@vols.utk.edu": {
        "student_id": "000412877",
        "credits_completed": 61,
        "credits_in_progress": 13,
        "gpa": 3.42,
        "major": "Biology, B.S.",
        "holds": [],
    },
    "priya.shah@vols.utk.edu": {
        "student_id": "000487203",
        "credits_completed": 44,
        "credits_in_progress": 15,
        "gpa": 2.71,
        "major": "Nursing (pre-major)",
        "holds": ["Advising Hold"],
    },
    "marcus.bell@vols.utk.edu": {
        "student_id": "000455119",
        "credits_completed": 78,
        "credits_in_progress": 12,
        "gpa": 1.94,
        "major": "Mechanical Engineering, B.S.",
        "holds": ["Bursar Hold"],
    },
}


def get_dars(sender: str) -> dict | None:
    """Return the student's DARS record for this sender email, or None if unknown."""
    return DARS.get(sender)
