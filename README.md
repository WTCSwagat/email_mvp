# Advise Assist

AI-powered Outlook add-in for academic advisors at UTK. When an advisor opens an email, the add-in reads the message, scrubs PII locally, categorizes the request with Groq, and surfaces relevant UTK policy context and referral guidance.

## Architecture

```
Outlook (taskpane)
    │
    ▼
Cloudflare tunnel ──► http-server :3000  (addin/)
    │
    │  POST /process-email
    ▼
Cloudflare tunnel ──► FastAPI :8000
                          │
                          ├── scrubber.py   (local PII removal)
                          ├── categorize.py (Groq)
                          ├── canonical.py  (Groq)
                          ├── context.py    (UTK policy snippets)
                          └── referral.py   (office routing)
```

The frontend and backend each need their own public HTTPS URL. Cloudflare quick tunnels (`trycloudflare.com`) are used for local development so Outlook can reach both services.

## Prerequisites

- Python 3.11+
- Node.js (for `npx http-server`)
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (`brew install cloudflared`)
- A [Groq API key](https://console.groq.com/) they hhave free api key for decent usuage. 
- Outlook desktop (Mac or Windows) for sideloading the add-in

## Setup

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
```

## Running locally

You need four terminals running at the same time.

**Terminal 1 — Backend**

```bash
source .venv/bin/activate
python -m uvicorn main:app --reload
```

**Terminal 2 — Frontend static server**

```bash
cd addin
npx http-server -p 3000
```

**Terminal 3 — Frontend tunnel**

```bash
cloudflared tunnel --url http://localhost:3000
```

Copy the printed URL (e.g. `https://something.trycloudflare.com`).

**Terminal 4 — Backend tunnel**

```bash
cloudflared tunnel --url http://localhost:8000
```

Copy the printed URL (e.g. `https://something-else.trycloudflare.com`).

### Update URLs after starting tunnels

Cloudflare quick tunnel URLs change every time you restart `cloudflared`. Update these files with the new URLs (no trailing spaces):

1. **`addin/taskpane.js`** — set `BACKEND_URL` to the backend tunnel URL
2. **`addin/manifest.xml`** — update all frontend URLs and both `<AppDomain>` entries, then bump `<Version>`

After changing the manifest, remove and re-add the add-in in Outlook so it picks up the new version.

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

## Project structure

```
email_mvp/
├── addin/
│   ├── manifest.xml      # Outlook add-in manifest
│   ├── taskpane.html     # Add-in UI
│   ├── taskpane.js       # Reads email, calls backend
│   ├── taskpane.css
│   └── assets/           # Icons
├── main.py               # FastAPI app
├── scrubber.py           # Local PII scrubbing (spaCy + regex)
├── categorize.py         # Email categorization (Groq)
├── canonical.py          # Canonical question generation (Groq)
├── context.py            # UTK policy context lookup
├── referral.py           # Office referral routing
├── requirements.txt
└── .env                  # GROQ_API_KEY (not committed)
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Could not reach backend" | Backend tunnel not running, or `BACKEND_URL` in `taskpane.js` is wrong |
| Add-in loads but API call fails | Backend `<AppDomain>` missing or has a trailing space in `manifest.xml` |
| Manifest changes not applied | Bump `<Version>` and re-sideload the add-in in Outlook |
| `500 Internal Server Error` on `/process-email` | Check uvicorn terminal for traceback; often a Groq JSON parse issue |
| Tunnel URL changed | Restarting `cloudflared` generates a new URL — update `taskpane.js` and `manifest.xml` |

**Verify the backend is reachable:**

```bash
curl https://your-backend-tunnel.trycloudflare.com/
```

**Verify the frontend is serving the add-in:**

```bash
curl https://your-frontend-tunnel.trycloudflare.com/taskpane.html
```
