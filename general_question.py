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
#this funciton just prototype so fix this in detail later 

def generate_canonical(email_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""
            Convert this student email to a general 
            anonymized policy question.

            Rules:
            - Remove ALL names, student IDs, GPAs, 
              specific grades, specific course codes
            - Convert specifics to generals
            - "CHEM 101" becomes "a science course"
            - "GPA 1.8" becomes "low academic standing"
            
            Return JSON only:
            {{
              "canonical_question": "general question",
              "safe_to_store": true/false,
              "pii_removed": ["list what you removed"]
            }}
            
            Email: {email_text}
            """
        }]
    )
    return safe_parse(response.choices[0].message.content)

