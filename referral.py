import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

REFERRAL_MAP = {
    "add_drop": {
        "office": "Registrar",
        "action": "Direct student to complete add/drop form before the posted deadline.",
        "link": "https://registrar.utk.edu/",
    },
    "major_change": {
        "office": "Academic Advising",
        "action": "Schedule a major change advising appointment.",
        "link": "https://advising.utk.edu/",
    },
    "failing_class": {
        "office": "Academic Support",
        "action": "Refer student to tutoring and academic support resources.",
        "link": "https://academicsupport.utk.edu/",
    },
    "financial": {
        "office": "One Stop Student Services",
        "action": "Direct student to One Stop for financial aid and scholarship questions.",
        "link": "https://onestop.utk.edu/",
    },
    "mental_health": {
        "office": "Counseling Center",
        "action": "Refer student to the UTK Counseling Center. If urgent, note crisis resources.",
        "link": "https://counselingcenter.utk.edu/",
    },
    "general": {
        "office": "One Stop Student Services",
        "action": "Direct student to One Stop for general advising questions.",
        "link": "https://onestop.utk.edu/",
    },
}


def get_referral(category: str) -> dict:
    return REFERRAL_MAP.get(category, REFERRAL_MAP["general"])


def generate_referral_draft(
    category: str,
    canonical_question: str = "",
    policy_context: str = "",
) -> str:
    """Ask Groq to write a student-facing referral reply.

    Only PII-free inputs are passed in. The model must leave the student name
    and advisor name as the literal placeholders [name] and [Advisor name] so
    they can be filled in locally (client-side) without PII ever reaching Groq.
    """
    referral = get_referral(category)

    tone = (
        "Use a supportive, caring tone. Gently mention that the UTK Counseling "
        "Center offers crisis resources and that help is available 24/7."
        if category == "mental_health"
        else "Use a warm, professional, encouraging tone."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a UTK academic advisor writing a short reply to a "
                    "student email. Write only the email body: 3-5 short "
                    "sentences, no subject line, no markdown.\n"
                    "CRITICAL: Greet the student with the LITERAL placeholder "
                    "[name] and sign off with the LITERAL placeholder "
                    "[Advisor name]. Never invent, guess, or use a real name. "
                    "Output the placeholders exactly as written.\n\n"
                    "Example:\n"
                    "Hi [name],\n\n"
                    "Thanks for reaching out. The best next step is to contact "
                    "the Registrar, who can walk you through the add/drop form "
                    "before the posted deadline. You can start here: "
                    "https://registrar.utk.edu/. Please let me know if you'd "
                    "like to talk it through.\n\n"
                    "Best,\n[Advisor name]"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Category: {category}\n"
                    f"Refer the student to: {referral['office']} "
                    f"({referral['link']})\n"
                    f"Recommended action: {referral['action']}\n"
                    f"Student's anonymized question: {canonical_question}\n"
                    f"Relevant UTK policy context: {policy_context}\n\n"
                    f"{tone}\n"
                    "Write the reply now, using [name] and [Advisor name]."
                ),
            },
        ],
    )
    return response.choices[0].message.content.strip()
