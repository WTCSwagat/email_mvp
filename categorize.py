from groq import Groq
import json
import re
import os

from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_parse(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {}

def categorize_email(email_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""
            Categorize this academic advising email.

            Return valid JSON only. Do not include markdown or explanation.

            Choose exactly one category from:
            - add_drop
            - major_change
            - failing_class
            - financial
            - mental_health
            - general

            Choose exactly one urgency from:
            - routine
            - urgent
            - critical

            Choose exactly one complexity from:
            - low
            - moderate
            - high

            Return exactly this shape:
            {{
            "category": "general",
            "urgency": "routine",
            "complexity": "moderate",
            "contains_pii": false
            }}

            Email:
            {email_text}
            """
        }]
    )
    return safe_parse(response.choices[0].message.content)