# `/process-email` Response Contract (FROZEN)

This is the shape the frontend panel builds against. **Do not change field names without updating the frontend.** `fake_dars.py` and `judge.py` must produce exactly this.

## Full shape
```json
{
  "category": "add_drop",
  "urgency": "routine",
  "complexity": "low",
  "context": { "text": "...", "link": "...", "source": "verified knowledge base" },
  "referral": { "office": "...", "action": "...", "link": "..." },

  "decision": "yes | partly | no",
  "draft": "Hi [name], ... Best, [Advisor name]",   // "" when decision is "no"
  "checklist": ["..."],                               // [] unless "partly"

  "used_record": true,                                // did the judge use DARS?
  "dars": {                                           // or null if no record for this sender
    "student_id": "000123456",
    "credits_completed": 58,
    "credits_in_progress": 13,
    "gpa": 3.1,
    "major": "Biology",
    "holds": []
  }
}
```

## Example per state

### 1. YES — record resolves it (clean student)
```json
{
  "decision": "yes",
  "draft": "Hi [name],\n\nYou can drop a course without a 'W' until the posted add/drop deadline. Based on your current schedule you'd be at 10 credit hours after dropping — below full-time (12), which can affect financial aid and housing. Let's talk before you do it.\n\nBest,\n[Advisor name]",
  "checklist": [],
  "used_record": true,
  "dars": { "student_id": "000123456", "credits_completed": 58, "credits_in_progress": 13, "gpa": 3.1, "major": "Biology", "holds": [] }
}
```

### 2. PARTLY — record used, but something needs the advisor (a hold)
```json
{
  "decision": "partly",
  "draft": "Hi [name],\n\nYou can drop a course without a 'W' until the posted deadline. Before that goes through, there's a hold on your account we'll need to clear first.\n\nBest,\n[Advisor name]",
  "checklist": ["Resolve the advising hold before any drop can be processed", "Confirm dropping won't break a major requirement sequence"],
  "used_record": true,
  "dars": { "student_id": "000123457", "credits_completed": 42, "credits_in_progress": 15, "gpa": 2.3, "major": "Nursing", "holds": ["Advising hold"] }
}
```

### 3. NO RECORD — fallback (unknown sender)
```json
{
  "decision": "partly",
  "draft": "Hi [name],\n\nYou can drop a course without a 'W' until the posted deadline.\n\nBest,\n[Advisor name]",
  "checklist": ["Check their current credit hours — dropping below 12 affects full-time status and aid", "Check for any holds on the account"],
  "used_record": false,
  "dars": null
}
```

### 4. NO — policy can't answer it
```json
{
  "decision": "no",
  "draft": "",
  "checklist": [],
  "used_record": false,
  "dars": null
}
```

## Frontend rendering rules
- **decision = yes** → show `draft` as "ready to send"; no checklist.
- **decision = partly** → show `draft` + render `checklist` as ticked items.
- **decision = no** → no draft; show `context` + `referral` only.
- **dars != null** → render the "Student record (DARS)" card (credits · GPA · holds).
- **dars == null** → no card.
- **used_record = true** → show a small "✓ used student record" badge (transparency cue for the provost demo).

## Build notes
- **DARS stays OFF the scrubber path.** Scrubber cleans the inbound email *body* only. The DARS record is a separate trusted input — never route it through `scrub_pii`, or it strips the exact details the judge needs. (Comment this at the wire-in point in `main.py`.)
- **No-record path must not error.** `get_dars(sender)` returns `None` for unknown senders → judge runs without DARS → behaves as the pre-DARS version (student-specifics go to the checklist). Most test emails will hit this path, so it has to be solid.
- **Fake data matches real UTK formats** — `@vols.utk.edu` emails, 4.0 GPA scale, realistic credit-hour and student-ID formats. Looks like what advisors see in DARS daily.
- **Pick 2–3 varied scenarios, not 15 similar** — one clean student (→ yes), one with a hold/missing requirement (→ partly), and unknown senders (→ no-record fallback). Map the ~15 fake emails onto these so each demonstrates a different pipeline state.
