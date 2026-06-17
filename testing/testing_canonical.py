from canonical import generate_canonical

# ── TEST CASES ───────────────────────────────────────
pii_emails = [
    "Hi I'm John Smith and my GPA dropped to 1.8 after failing CHEM 101. Will I lose my scholarship?",
    "My student ID is 123456789 and I need to drop BIO 250 before Friday",
    "I got a D in Physics last semester, can I retake it to replace the grade?"
]

clean_emails = [
    "When is the last day to drop a class this semester?",
    "How do I change my major at UTK?",
    "What happens if I withdraw from all my classes?"
]

print("Testing PII removal...\n")

print("── Emails WITH personal details ──")
for email in pii_emails:
    result = generate_canonical(email)
    print(f"\nOriginal: {email}")
    print(f"Canonical: {result.get('canonical_question')}")
    print(f"Safe to store: {result.get('safe_to_store')}")
    print(f"PII removed: {result.get('pii_removed')}")

print("\n── Emails WITHOUT personal details ──")
for email in clean_emails:
    result = generate_canonical(email)
    print(f"\nOriginal: {email}")
    print(f"Canonical: {result.get('canonical_question')}")
    print(f"Safe to store: {result.get('safe_to_store')}")