import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scrubber import scrub_pii
from categorize import categorize_email
from general_question import generate_canonical
from context import get_context
from referral import get_referral, generate_referral_draft
from judge import judge_context
from fake_dars import get_dars
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


class BatchEmail(BaseModel):
    id: str
    subject: str = ""
    body: str = ""


class BatchEmailRequest(BaseModel):
    emails: list[BatchEmail]


@app.get("/")
def root():
    return {"status": "Advise Assist backend running"}


@app.post("/process-email")
async def process_email(request: EmailRequest):

    # Demo: skip PII scrubbing so the model sees the full email (fake data → richer answers).
    # Production keeps scrub_pii here; bypassed for the demo only.
    clean_text = request.email_text

    # Step 1: Categorize
    category_data = categorize_email(clean_text)

    # Step 2: Generate canonical question (kept for the response/analytics)
    canonical_data = generate_canonical(clean_text)

    # Step 3: Surface relevant policy context
    category = category_data.get("category", "general")
    context = get_context(category)

    # Step 4: Match the student's DARS record by the NAME in the email text
    # (NOT scrubbed — a separate trusted input).
    dars = get_dars(clean_text)

    # Step 5: Judge + draft. Mental-health emails are NEVER auto-drafted —
    # they need the advisor's personal response.
    if category == "mental_health":
        judge_data = {"decision": "no", "draft": "", "checklist": [], "used_record": dars is not None}
    else:
        judge_data = judge_context(clean_text, context.get("text"), dars)



    # Step 5: Get referral
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
        "decision": judge_data.get("decision"),
        "draft": judge_data.get("draft"),
        "checklist": judge_data.get("checklist"),
        "used_record": judge_data.get("used_record"),
        "dars": dars,
        "referral": referral
    }

@app.post("/categorize-batch")
async def categorize_batch(request: BatchEmailRequest):
    async def process_one(email: BatchEmail):
        clean_text = await asyncio.to_thread(scrub_pii, email.body)
        category_data = await asyncio.to_thread(categorize_email, clean_text)
        return {
            "id": email.id,
            "subject": email.subject,
            "category": category_data.get("category", "general"),
            "urgency": category_data.get("urgency", "routine"),
        }

    results = await asyncio.gather(*[process_one(e) for e in request.emails])
    return {"results": list(results)}


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