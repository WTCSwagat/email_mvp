# Advise Assist

AI-powered Outlook add-in for academic advisors at UTK. When an advisor opens an email, the add-in reads the message, scrubs PII locally, categorizes the request with Groq, and surfaces relevant UTK policy context and referral guidance.

## Try the demo (for teammates / testers)

You don't need to clone or build anything — the add-in is already deployed. To try it:

**Requirements (important):**
- Use a **personal outlook.com account** — the add-in's Microsoft sign-in is registered for personal accounts only (work/school accounts won't work).
- Use **Outlook on the web in Chrome** — *not* the desktop app (category tags lag behind there) and *not* Safari (it blocks the sign-in popup).
- For the full experience, sign into the **shared demo mailbox** (`advise.assist@outlook.com`), which is seeded with 27 fake student emails. On your own mailbox the polished canned answers only fire for those exact demo subjects.

**Steps:**
1. Open [outlook.com](https://outlook.com) in **Chrome** and sign into the demo mailbox.
2. Settings (gear) → search "add-in" → **Manage add-ins** → **My add-ins** → **Custom Addins** → **+ Add a custom add-in** → **Add from file**.
3. Upload `addin/manifest.xml` from this repo → **Install**.
4. Open any student email → click **Advise Assist** in the message toolbar (or the `···` / Apps menu) → you'll see the category, urgency, a pre-drafted reply, and the student's DARS record.
5. Click **Categorize Inbox** → approve the Microsoft sign-in once → the whole inbox gets sorted and color-tagged. Switch Outlook to **Arrange by: Categories** to see the grouped view.

**Heads-up:**
- The backend runs on Render's free tier and **sleeps after ~15 min idle**. The first click after idle can show "Failed to fetch" / "could not reach backend" for ~30–60s while it wakes — just wait and click again. (A keep-warm pinger avoids this for live demos.)
- The pane **updates automatically** when you select a different email, but it does **not stay pinned** open across emails (pinning isn't supported on personal accounts) — reopen it per email.

## Architecture

```
Outlook (taskpane)
    │
    ▼
Vercel  ──►  static add-in files (addin/)
    │         https://email-mvp-roan.vercel.app
    │
    │  POST /process-email, /draft-reply
    ▼
Render  ──►  FastAPI service
                https://advise-assist-api.onrender.com
                          │
                          ├── scrubber.py   (local PII removal)
                          ├── categorize.py (Groq)
                          ├── general_question.py (Groq canonical question)
                          ├── context.py    (UTK policy snippets)
                          └── referral.py   (office routing + draft generation)
```

The frontend (static add-in assets) is hosted on **Vercel**. The backend (FastAPI) is hosted on **Render**. Both get stable public HTTPS URLs, so Outlook can reach them without local tunnels.

## Prerequisites

- Python 3.11+
- Node.js (only needed for local frontend preview)
- A [Groq API key](https://console.groq.com/) — free tier is fine for decent usage
- A [Vercel](https://vercel.com/) account (frontend hosting)
- A [Render](https://render.com/) account (backend hosting)
- Outlook desktop (Mac or Windows) for sideloading the add-in

## Local development

### 1. Clone and create a virtual environment

```bash
cd email_mvp
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

### 4. Run the backend locally

```bash
source .venv/bin/activate
python -m uvicorn main:app --reload
```

The API is now at `http://127.0.0.1:8000` (interactive docs at `/docs`).

### 5. Preview the frontend locally (optional)

```bash
cd addin
npx http-server -p 3000
```

For local end-to-end testing against Outlook you can point `BACKEND_URL` in `addin/taskpane.js` at `http://localhost:8000`, but the recommended path is to deploy to Vercel + Render (below), which gives you stable HTTPS URLs Outlook can always reach.

## Deployment

### Backend → Render

The repo ships with a `render.yaml` blueprint:

```yaml
services:
  - type: web
    name: advise-assist-api
    runtime: python
    plan: free
    buildCommand: "pip install -r requirements.txt && python -m spacy download en_core_web_sm"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

1. Push this repo to GitHub.
2. In Render, create a **New → Blueprint** and point it at the repo (Render auto-detects `render.yaml`), or create a **Web Service** manually with the build/start commands above.
3. Set the environment variables in the Render dashboard (these are **not** committed):
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
4. Deploy. Your backend will be live at a URL like `https://advise-assist-api.onrender.com`.
5. Verify: `curl https://advise-assist-api.onrender.com/` should return `{ "status": "Advise Assist backend running" }`.

> Note: Render's free tier spins the service down after inactivity, so the first request after idle can take ~30–60s to wake up.

### Frontend → Vercel

The static add-in lives in `addin/` and is configured by `addin/vercel.json`:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": null,
  "buildCommand": null,
  "installCommand": null,
  "outputDirectory": "."
}
```

1. In Vercel, **import the project** from GitHub.
2. Deploy. The add-in assets are served from a URL like `https://email-mvp-roan.vercel.app`, with files reachable under `/addin/...` (e.g. `/addin/taskpane.html`).
3. Verify: open `https://email-mvp-roan.vercel.app/addin/taskpane.html` in a browser.

### Wire the two together

After both are deployed, make sure the URLs line up (no trailing spaces):

1. **`addin/taskpane.js`** — set `BACKEND_URL` to your Render URL:

   ```js
   const BACKEND_URL = "https://advise-assist-api.onrender.com";
   ```

2. **`addin/manifest.xml`** — all `<bt:Url>`, `IconUrl`, `SourceLocation`, and icon URLs should point at your Vercel domain, and both backend + frontend domains must be listed under `<AppDomains>`:

   ```xml
   <AppDomains>
     <AppDomain>https://email-mvp-roan.vercel.app</AppDomain>
     <AppDomain>https://advise-assist-api.onrender.com</AppDomain>
   </AppDomains>
   ```

3. Whenever you change the manifest, bump `<Version>` and re-sideload the add-in in Outlook so it picks up the new version.

## Sideloading in Outlook

1. Open Outlook desktop.
2. Go to **Get Add-ins** → **My Add-ins** → **Add a custom add-in** → **Add from file**.
3. Select `addin/manifest.xml`.
4. Open any email and click **Advise Assist** in the ribbon to open the taskpane.

## API

### `GET /`

Health check.

```json
{ "status": "Advise Assist backend running" }
```

### `POST /process-email`

**Request body:**

```json
{
  "email_text": "Full email body text",
  "subject": "Email subject",
  "sender": "student@utk.edu"
}
```

**Response:**

```json
{
  "category": "add_drop",
  "urgency": "routine",
  "complexity": "moderate",
  "contains_pii": false,
  "canonical_question": "...",
  "safe_to_store": true,
  "pii_removed": ["names", "student IDs"],
  "context": {
    "text": "Relevant UTK policy summary...",
    "link": "https://catalog.utk.edu/"
  },
  "referral": {
    "office": "Registrar",
    "action": "Direct student to complete add/drop form...",
    "link": "https://registrar.utk.edu/"
  }
}
```

### `POST /draft-reply`

Generates a student-facing referral reply from PII-free fields. Names stay as `[name]` / `[Advisor name]` placeholders and are filled in locally by the add-in.

**Request body:**

```json
{
  "category": "add_drop",
  "canonical_question": "...",
  "policy_context": "..."
}
```

**Response:**

```json
{ "draft": "Hi [name], ... Best, [Advisor name]" }
```

## Project structure

```
email_mvp/
├── addin/
│   ├── manifest.xml      # Outlook add-in manifest
│   ├── taskpane.html     # Add-in UI
│   ├── taskpane.js       # Reads email, calls backend
│   ├── taskpane.css
│   ├── vercel.json       # Vercel static-hosting config
│   └── assets/           # Icons
├── main.py               # FastAPI app
├── scrubber.py           # Local PII scrubbing (spaCy + regex)
├── categorize.py         # Email categorization (Groq)
├── general_question.py   # Canonical question generation (Groq)
├── context.py            # UTK policy context lookup
├── referral.py           # Office referral routing + draft generation
├── db.py                 # Supabase client
├── render.yaml           # Render deployment blueprint
├── requirements.txt
└── .env                  # GROQ_API_KEY / SUPABASE_* (not committed)
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Could not reach backend" | Render service is asleep/waking, or `BACKEND_URL` in `taskpane.js` is wrong |
| First request very slow (~30–60s) | Render free tier cold start — the service spins up on demand |
| Add-in loads but API call fails | Backend `<AppDomain>` missing or has a trailing space in `manifest.xml` |
| Manifest changes not applied | Bump `<Version>` and re-sideload the add-in in Outlook |
| `500 Internal Server Error` on `/process-email` | Check Render logs for traceback; often a Groq JSON parse issue |
| Frontend 404 on Vercel | Confirm the path includes `/addin/` (e.g. `/addin/taskpane.html`) |

**Verify the backend is reachable:**

```bash
curl https://advise-assist-api.onrender.com/
```

**Verify the frontend is serving the add-in:**

```bash
curl https://email-mvp-roan.vercel.app/addin/taskpane.html
```
