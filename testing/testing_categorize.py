from categorize import categorize_email

# ── TEST EMAILS ──────────────────────────────────────
tests = [
    {
        "email": """
        Hi,

        I'm currently enrolled in four classes this semester and I'm considering dropping one of them.
        I've looked through the university website but I'm still confused about the withdrawal deadlines.
        Could you tell me when the last day is to drop a class without it affecting my transcript?

        Thanks.
        """,
        "expected_category": "add_drop",
        "expected_urgency": "routine",
        "expected_pii": False
    },
    {
        "email": """
        Hello,

        I'm really worried because I'm struggling badly in my chemistry course.
        My professor told me I should consider dropping it, but the deadline is coming up this Friday.
        If I don't drop the class before then, there's a good chance I'll fail the course.
        Can someone tell me what my options are as soon as possible?

        Thanks.
        """,
        "expected_category": "add_drop",
        "expected_urgency": "urgent",
        "expected_pii": False
    },
    {
        "email": """
        Hi Advisor,

        I'm concerned about my academic standing. My current GPA is 1.8 and I'm failing two of my classes.
        I'm receiving a merit-based scholarship, and I'm worried that these grades could affect my eligibility.
        Can you let me know whether I'm at risk of losing my scholarship and what steps I should take?

        Thank you.
        """,
        "expected_category": "failing_class",
        "expected_urgency": "urgent",
        "expected_pii": True
    },
    {
        "email": """
        Hello,

        I've been dealing with some personal challenges over the past few months, and it's becoming increasingly difficult
        to keep up with my coursework. I've missed several assignments and I'm starting to feel overwhelmed.
        At this point, I'm not sure if I'll be able to complete the semester successfully.

        Could someone advise me on what resources or support options are available?

        Thank you.
        """,
        "expected_category": "mental_health",
        "expected_urgency": "critical",
        "expected_pii": False
    },
    {
        "email": """
        Hi,

        I'm currently majoring in Biology, but after taking several programming courses this year,
        I've realized that Computer Science may be a better fit for my career goals.
        Could you explain the process for changing my major and whether there are any prerequisite courses I need to complete?

        Best regards.
        """,
        "expected_category": "major_change",
        "expected_urgency": "routine",
        "expected_pii": False
    }
]
passed = 0
for case in tests:
    result = categorize_email(case["email"])

    cat_ok = result.get("category") == case["expected_category"]
    urg_ok = result.get("urgency") == case["expected_urgency"]
    pii_ok = result.get("contains_pii") == case["expected_pii"]

    status = "✓" if all([cat_ok, urg_ok, pii_ok]) else "✗"
    if all([cat_ok, urg_ok, pii_ok]):
        passed += 1

    print(f"{status} {case['email'][:45]}...")
    if not cat_ok:
        print(f"  Category: got {result.get('category')}, expected {case['expected_category']}")
    if not urg_ok:
        print(f"  Urgency: got {result.get('urgency')}, expected {case['expected_urgency']}")
    if not pii_ok:
        print(f"  PII: got {result.get('contains_pii')}, expected {case['expected_pii']}")