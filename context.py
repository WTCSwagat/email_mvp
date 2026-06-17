import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

POLICY_LINKS = {
    "add_drop": "https://registrar.utk.edu/records/withdrawal/",
    "major_change": "https://catalog.utk.edu/",
    "failing_class": "https://academicsupport.utk.edu/",
    "financial": "https://financialaid.utk.edu/sap/",
    "mental_health": "https://counselingcenter.utk.edu/",
    "general": "https://catalog.utk.edu/",
}



def get_context(category: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=150,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a UTK academic policy assistant. Be concise and "
                    "practical. Never invent specific dates - say 'posted "
                    "deadline' instead."
                ),
            },
            {
                "role": "user",
                "content": f"""An advisor received a student email categorized as: {category}

In 2-3 sentences, summarize what UTK policy says that is most relevant to this category. What does the advisor need to know?""",
            },
        ],
    )
    return {
        "text": response.choices[0].message.content.strip(),
        "link": POLICY_LINKS.get(category, POLICY_LINKS["general"]),
    }
