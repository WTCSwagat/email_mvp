import os

from dotenv import load_dotenv
from groq import Groq

from knowledge_base import get_knowledge

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



def get_context(category: str) -> dict:

    # Fallback: no KB entry for this category, so ask the model.
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=150,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a UTK (University of Tennessee, Knoxville) academic "
                    "policy assistant helping an advisor triage a student email. "
                    "Be concise, practical, and accurate.\n"
                    "Rules:\n"
                    "- Only state policy you are confident is correct for UTK.\n"
                    "- Never invent specifics: no exact dates, dollar amounts, GPA "
                    "cutoffs, or office names. Say 'the posted deadline' instead of "
                    "a date.\n"
                    "- If you do NOT have reliable UTK policy information for this "
                    "topic, reply with exactly: NO_INFO — and nothing else. "
                    "When in doubt, prefer NO_INFO over guessing."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"An advisor received a student email categorized as: {category}\n\n"
                    "In 2-3 sentences, summarize the most relevant UTK policy and what "
                    "the advisor needs to know to respond. If you're not confident "
                    "about the actual UTK policy, reply with NO_INFO."
                ),
            },
        ],
    )
#review this function later 
    answer = response.choices[0].message.content.strip()

    if "NO_INFO" in answer.upper():
        entry = get_knowledge(category)
        if entry:
            return {"text": entry["answer"], "link": entry["source"],
                    "source": "verified knowledge base"}
        return {"text": "Refer the student to One Stop for guidance.",
                "link": "", "source": "fallback"}

    return {"text": answer, "link": "", "source": "AI-generated"}
    

