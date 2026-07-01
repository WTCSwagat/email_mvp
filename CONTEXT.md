# Advise Assist — Project Context (for a fresh Claude chat)

Paste/point a new chat at this file to get oriented without re-explaining. It's a
**demo/MVP**, not production — bias toward the simplest thing that works, don't
over-engineer. (Last updated late June 2026.)

---

## What it is
An **Outlook add-in (task pane) + FastAPI backend** that helps **UTK academic
advisors** triage student emails. When an advisor opens a student email, the pane:
categorizes it, surfaces relevant UTK policy, and **pre-drafts a reply** — using a
fake "DARS" (degree-audit) record so the reply is personalized to the student. It can
also **bulk-categorize the whole inbox** with native Outlook color tags (one button).

## The goal (immediate)
A **validation pilot**: give ~5 real advisors a demo Outlook account seeded with fake
student emails and measure **"is this helpful?"** via a Google Form. **Target ~July 1,
2026.** Everything is **fake data** — we're showing the use cases.

## Two-stage go-to-market
1. **Advisors** validate the value (champions) — this pilot.
2. **Provost / buyer** demo later — pitch the *whole* product incl. **DPA, PII
   scrubbing, FERPA, real DARS integration**. The demo shows the experience; the
   pitch sells the production architecture. Be honest: the demo bypasses scrubbing
   and uses fake DARS; production does the real thing.
- **Moat** is NOT the AI (commodity). It's the hard, slow stuff built in production:
  real SIS/DARS integration + signed DPAs, FERPA/compliance trust, a curated
  per-institution policy KB, and advisor-champion distribution. Pitch that, not "smarter AI."

---

## Pipeline (`POST /process-email`)
scrub (BYPASSED in demo) → categorize → canonical question → policy context
→ DARS lookup → judge (decision + draft + checklist) → referral. Returns ONE JSON
"contract" the frontend renders. **The frontend calls this ONCE per email** (on open /
`ItemChanged`) and slices the single response across the whole UI — tab switching,
editing the draft, opening the record popup do NOT re-hit the backend.

**Response contract:** `category, urgency, complexity, contains_pii,
canonical_question, context{text,link,source}, decision (yes|partly|no), draft,
checklist[], used_record, dars{...}, referral{office,action,link}`

## Key files (backend, Python)
- `main.py` — FastAPI; `/process-email`, `/draft-reply`, `/categorize-batch`. Both
  `/process-email` and `/categorize-batch` have a **canned fast-path** (demo branch)
  keyed by subject → zero LLM calls; `/categorize-batch` also returns `name` (from the
  DARS match) per email.
- `categorize.py` — category/urgency/complexity via Groq `llama-3.1-8b-instant`. Has `safe_parse`.
- `general_question.py` — anonymized "canonical question."
- `context.py` — `get_context`: **AI-first**, falls back to the fake KB on the `NO_INFO` sentinel.
- `knowledge_base.py` — fake in-memory KB of verified policy answers + `get_knowledge`.
- `judge.py` — `judge_context`: reasoning brain → `decision` + `draft` + `checklist`; sees full email + DARS. Swappable to Claude later.
- `fake_dars.py` — fake degree records **keyed by NAME**, matched by scanning the email body. **EVERY student now has a RICH record** (completed_courses + current_courses + remaining_required with prereq chains + note; some have a short `why`). 24 students incl. the FERPA son "Marcus Carter".
- `fake_emails.py` — **27** fake student emails; **each body starts with the student's name** (that's how DARS is matched). Verified: each email resolves to exactly one student (no name collisions).
- `referral.py` — referral map + `generate_referral_draft`.
- `demo_answers.py` — **`demo` branch ONLY**: canned "perfect" answers keyed by subject (zero LLM calls). **Covers all 27 subjects** incl. mental-health (no draft) and FERPA (decline + cite FERPA).

## Key files (frontend, `addin/`)
- `taskpane.html/css/js` — the task pane. Current UI (top → bottom):
  - **Categorize Inbox** button (silent — tags inbox via Graph, brief "✓ Categorized", no summary panel).
  - Per-email view: status banner (yes/partly/no) + category & urgency pills.
  - **Rich student record card** — stat tiles (GPA red on probation, in-progress, of-120-done), graduation progress bar, hold badge, "why it matters" line. **Tap it → detail popup** (`darsModal`) with full transcript + prereq chains.
  - **Context / Pre-drafted tabs** below the record. *Context* = related policy + source badge (verified KB vs AI) + referral office. *Pre-drafted* = **editable** draft (`<textarea>`) + checklist + Insert button (or no-draft note). Defaults to Pre-drafted when a draft exists, Context otherwise.
  - **"✓ Already responded" banner** — set when the advisor clicks Insert (keyed on `item.itemId` in `localStorage`; resets on reseed).
  - Feedback thumbs → open `FEEDBACK_FORM_URL` (still empty — TODO).
- `fallbackauth.html` — MSAL auth page loaded inside an Office dialog (see auth note).
- `msal-browser.min.js` — **self-hosted** MSAL v2.38.1 (the alcdn CDN 404'd; serve from our own whitelisted domain).
- `manifest.xml` — `ReadWriteMailbox` perms. **No `SupportsPinning`** (see note). Id `57166ac7-...`.

---

## Decisions / non-obvious facts
- **Model:** Groq `llama-3.1-8b-instant` now; **Claude after funding** (judge is a drop-in swap).
- **DARS matched by NAME in the body**, not sender — browser-seeded demo emails all arrive from one address.
- **PII scrubber is bypassed in the demo** (`clean_text = request.email_text`). Fake data, so safe. Production scrubs.
- **Mental-health emails → NO auto-draft** (advisor responds personally); crisis resources shown. Enforced in `main.py` + canned answers.
- **FERPA email** (parent asking for grades): resolves to the son's record (advisor may view) but the canned reply **declines and cites FERPA** — never auto-shares grades.
- **Categorize Inbox NOW WORKS** (bulk). Tags each inbox email with a native Outlook **color category** via Microsoft **Graph** (`PATCH /me/messages/{id}` in throttle-safe batches with retries; creates/fixes master categories first). It's **silent** — no in-pane summary (a triage digest was built then removed as redundant with Outlook's own grouping).
- **Auth = Office Dialog API + MSAL, NOT SSO.** Personal outlook.com can't use Office SSO, and an MSAL popup is blocked inside the task-pane iframe. So `getGraphToken()` opens `fallbackauth.html` in an Office dialog, which runs MSAL and posts the token back via `messageParent`. Azure app: client id `6373ddfb-fa04-41a7-9053-e8111df6ad9d`, **personal-accounts-only**, authority `…/consumers`, delegated scope **`Mail.ReadWrite`**, SPA redirect = `…/addin/fallbackauth.html`. (The "Expose an API / add a client application" step is SSO-only — skip it on personal accounts.)
- **NO `SupportsPinning`.** It needs Mailbox requirement set 1.5, which personal outlook.com accounts don't support → the add-in installs then **silently vanishes** from the ribbon. Confirmed by bisecting. Keep the manifest at V1.0 VersionOverrides only. (Pinning becomes available if the pilot moves to a Microsoft 365 work/school account.)
- **Sideloading on personal accounts is flaky** but works; the add-in only appears in the **··· / Apps menu of an OPEN email**, not the main ribbon. Re-sideloading needs a clean remove + hard refresh.
- **Editable draft + responded banner are intentional**; mark-as-responded fires on Insert (action, not a real send).
- **Git:** do NOT add the `Co-Authored-By` trailer to commits (user preference).

## Branches & deployment
- **`main`** = clean real-AI product line. **`demo`** = `main` + canned answers + the latest add-in UI (pilot branch). (Remote also has `pranav_work`.)
- Backend: **Render** `https://advise-assist-api.onrender.com`. **Now serving `demo`** (verified live: previously-basic students return rich records). **Free tier cold-starts ~30–60s** after idle → first request can throw "failed to fetch"; **needs a keep-warm pinger**.
- Frontend: **Vercel** `https://email-mvp-roan.vercel.app`. Production branch **set to `demo`** and serving the latest. **Gotcha:** pushes sometimes land as a **Preview** — if so, **Promote to Production** in the Vercel Deployments tab (or it serves stale code).
- **Manifest changes require re-sideloading** the add-in; frontend/backend code changes don't (just redeploy + hard-refresh).

## Demo environment
- Demo mailbox: **`advise.assist@outlook.com`** (personal account).
- Seed via **`reseed_inbox.py`** (Playwright; manual login; deletes old inbox, sends the **27** emails from `fake_emails.py`). App-password/IMAP route was abandoned.

## What's left for the pilot
- [ ] **Keep-warm pinger** (UptimeRobot on Render `/` every ~10 min) — kills the cold-start "failed to fetch". Highest reliability win.
- [ ] **Re-seed the inbox** with the 27 emails (`reseed_inbox.py`).
- [ ] **Google Form** for feedback + paste link into `FEEDBACK_FORM_URL` in `taskpane.js` (currently empty).
- [ ] **Advisor onboarding** — decided: do a **short 1:1 live call** (watch them use it), not pure self-serve (they won't find the buried button / cold-start would look broken). Then leave self-serve access + form.
- [ ] **Quick-start guide / call run-sheet** for advisors (where the button is + "try these 3 emails").
- [ ] Recruit ~5 real advisors (mix of skeptic + eager).
- Done this cycle: Categorize Inbox (Graph), all-27 rich records + canned answers, editable draft, responded banner, student-record popup, Context/Pre-drafted tabs, dead-CSS cleanup, deploy both on `demo`.

## Working style the user prefers
Demo-grade, not perfect. Flag only what genuinely breaks the function; skip exhaustive
edge-case hardening. Move fast. The user often wants to *see* UI changes as a mockup
before they're built, and sometimes builds pieces themselves.
