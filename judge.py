from groq import Groq
from context import get_context        # at the top of judge.py
from categorize import safe_parse
import os 
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def judge_context(canonical_question: str, context: str, dars: dict | None = None) -> dict:
    # 1. Build the user message first; only include DARS when we actually have it.
    user_content = (
        f"Student's question: {canonical_question}\n\n"
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
                    "student's question and the relevant verified UTK policy. Decide "
                    "whether policy alone can answer it, and write a reply if so.\n"
                    "Decisions:\n"
                    "- \"yes\": policy fully answers it -> write a complete reply draft.\n"
                    "- \"partly\": policy gives the general rule, but the answer also "
                    "depends on this student's specifics (credit hours, financial aid, "
                    "GPA, holds) -> write the general part as the draft AND list the "
                    "student-specific things the advisor must check in \"checklist\".\n"
                    "- \"no\": policy does not cover this / it needs the advisor's "
                    "judgment -> empty draft and empty checklist.\n"
                    "Rules: Always greet as [name]. Never use the student ID, email, or any number as the name."
                    "[Advisor name] (never invent a real name). Use ONLY the provided "
                    "policy - do not invent policy. If unsure whether something is "
                    "universal or student-specific, put it in the checklist, not the draft.\n"
                    "If you are given the student's record (DARS), use it to answer the "
                    "student-specific parts directly — compute credit hours, note holds, etc. — "
                    "instead of listing them in the checklist. Only checklist what the record "
                    "does not cover.\n\n"
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