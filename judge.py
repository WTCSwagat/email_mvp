from groq import Groq
from context import get_context        # at the top of judge.py
from categorize import safe_parse
import os 
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def judge_context(email_text: str, context: str, dars: dict | None = None) -> dict:
    # 1. Build the user message first; only include DARS when we actually have it.
    user_content = (
        f"Student's email: {email_text}\n\n"
        f"Relevant UTK policy: {context}\n\n"
    )
    if dars:
        user_content += f"Student's record (DARS): {dars}\n\n"
    user_content += "Decide and respond in JSON."

    # 2. Make the call, dropping in the finished user string.
    reponses = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=400,
        messages=[
            {
                "role": "system",
                "content": (
                    "You help a UTK advisor reply to a student email. You are given the "
                    "student's full email and the relevant verified UTK policy. Decide "
                    "whether policy alone can answer it, and write a reply if so.\n"
                    "Decisions:\n"
                    "- \"yes\": policy fully answers it -> write a complete reply draft.\n"
                    "- \"partly\": policy gives the general rule, but the answer also "
                    "depends on this student's specifics (credit hours, financial aid, "
                    "GPA, holds) -> write the general part as the draft AND list the "
                    "student-specific things the advisor must check in \"checklist\".\n"
                    "- \"no\": policy does not cover this / it needs the advisor's "
                    "judgment -> empty draft and empty checklist.\n"
                    "Rules: greet the student as [name] and sign off as [Advisor name] "
                    "(never invent a real name; never use a student ID or number as the name). "
                    "Use ONLY the provided policy - do not invent policy. If unsure whether "
                    "something is universal or student-specific, put it in the checklist, not the draft.\n"
                    "If you are given the student's record (DARS), USE IT CONCRETELY: "
                    "compute their credit hours after the change, note holds and GPA, and "
                    "— if the record includes course lists and prerequisite chains "
                    "(remaining_required with prereqs) — name the SPECIFIC downstream "
                    "courses that depend on the course in question and explain the resulting "
                    "graduation delay. Be specific, not generic. For example: 'Dropping "
                    "CHEM 120 means you can't take CHEM 130 in spring, which pushes Organic "
                    "(CHEM 350) and Cell Biology back a year and delays graduation.' "
                    "Only put something in the checklist if the record genuinely doesn't cover it.\n\n"
                    "Return one JSON object only, no markdown, exactly: "
                    "{\"decision\": \"...\", \"draft\": \"...\", \"checklist\": [\"...\"]}"
                ),
            },
            {"role": "user", "content": user_content},
        ],
    )

    # 3. Parse the reply and flag whether the student's record was used.
    result = safe_parse(reponses.choices[0].message.content)
    result["used_record"] = dars is not None
    return result