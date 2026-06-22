from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scrubber import scrub_pii
from categorize import categorize_email
from general_question import generate_canonical
from context import get_context
from referral import get_referral, generate_referral_draft

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This defines what data comes in 
class EmailRequest(BaseModel):
    email_text: str
    subject: str
    sender: str


# Draft requests only carry PII-free fields (never raw email text).
class DraftRequest(BaseModel):
    category: str
    canonical_question: str = ""
    policy_context: str = ""


@app.get("/")
def root():
    return {"status": "Advise Assist backend running"}


@app.post("/process-email")
async def process_email(request: EmailRequest):

    # Scrub PII locally before anything touches Groq.
    clean_text = scrub_pii(request.email_text)

    # Step 1: Categorize (redacted text only)
    category_data = categorize_email(clean_text)

    # Step 2: Generate canonical question (redacted text only)
    canonical_data = generate_canonical(clean_text)

    # Step 3: Surface relevant policy context
    category = category_data.get("category", "general")
    context = get_context(category)

    # Step 4: Get referral
    referral = get_referral(category)

    return {
        "category": category,
        "urgency": category_data.get("urgency", "routine"),
        "complexity": category_data.get("complexity", "moderate"),
        "contains_pii": category_data.get("contains_pii", False),
        "canonical_question": canonical_data.get("canonical_question"),
        "safe_to_store": canonical_data.get("safe_to_store", False),
        "pii_removed": canonical_data.get("pii_removed", []),
        "context": context,
        "referral": referral
    }

@app.post("/draft-reply")
async def draft_reply(request: DraftRequest):
    # All inputs here are already PII-free. The draft comes back with
    # [name] / [Advisor name] placeholders that the add-in fills locally.
    draft = generate_referral_draft(
        request.category, 
        request.canonical_question,
        request.policy_context,
    )
    return {"draft": draft}


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)