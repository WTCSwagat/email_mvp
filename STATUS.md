# Advise Assist — Demo Status

**Goal:** a working prototype to give ~5 advisors for testing ("is this helpful?") by **July 1, 2026**. Fake data throughout — we're showing the use cases, not shipping production.

**Two-stage plan:** advisors validate the value → then demo to the provost / buyer (with fake DARS shown *transparently* as mocked) to get the real integration + budget.

---

## ✅ What we have (built & tested)

### Backend pipeline (`/process-email` runs these in order)
| File | Does |
|---|---|
| `scrubber.py` | Strips PII from the email body (kept in pipeline; harmless on fake data) |
| `categorize.py` | Category + urgency + complexity (Groq) |
| `general_question.py` | Canonical / anonymized question (Groq) |
| `knowledge_base.py` | Fake in-memory KB — 6 verified answers + `get_knowledge(category)` |
| `context.py` | Policy summary: **AI-first**, falls back to KB on `NO_INFO` |
| `judge.py` | `judge_context` → `decision` (yes/partly/no) + `draft` + `checklist` (Groq) |
| `referral.py` | Referral map + `generate_referral_draft` |
| `main.py` | `/process-email` (full pipeline) + `/draft-reply` |

- Pipeline verified end-to-end via `curl` — returns `decision`, `draft`, `checklist`.
- **Deployed:** backend on Render, frontend on Vercel.

### Frontend
- `taskpane.html` / `.css` / `.js` — redesigned panel. Shows category, urgency, policy, referral.
- ⚠️ Does **not** yet display `decision` / `draft` / `checklist`.

---

## 🔨 What we need (to build)

- [x] **`context.py` one-liner fix** — `"NO_INFO" in answer.upper()` so the KB fallback fires. *(done)*
- [x] **`fake_dars.py`** — fake records keyed by sender + `get_dars`, wired into `/process-email`, judge uses the record. *(done — 3 scenarios tested)*
- [x] **Frontend — three-state panel** — banner, DARS card, draft + Insert, checklist, policy reference, feedback. *(done — needs Outlook sideload test)*
- [ ] **Set `FEEDBACK_FORM_URL`** in `taskpane.js` once the Google Form exists. *(You)*
- [ ] **Demo environment** — 1 demo mailbox + fake student emails (send the DARS ones from `jordan.lee@`/`priya.shah@`/`marcus.bell@vols.utk.edu`, others for fallback) + add-in installed at mailbox level + keep-warm pinger. *(You)*
- [ ] **Google Form** — short "was this helpful?" feedback form. *(You)*
- [ ] **Recruit ~5 advisors** — real academic advisors, mix of skeptic + eager. *(You)*
- [ ] *(optional)* wrap the pipeline in `try/except` so a transient Groq failure degrades gracefully instead of a 500. *(You)*

---

## 🚫 Not building (deliberately deferred)
Real knowledge base / Supabase · embeddings / RAG · learning-from-replies · drift detection · auth · **real DARS integration**. Feedback is a Google Form, not an in-app DB. These are post-validation bets.

---

## Notes
- `db.py` exists but is **unused and broken** — safe to delete (we dropped Supabase).
- Fake DARS data is the FERPA-sensitive piece in the *real* product — that's the provost conversation, not a demo concern.
- Backend = your build (Python). Frontend = mine.
