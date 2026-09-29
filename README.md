# AI Tax Agent

A Flask web app for simplified federal income tax calculations (Form 1040-style). Enter your information, get an instant estimate, and optionally use the AI assistant to auto-fill the form from natural language.

## Live demo

**Live demo:** _add your Vercel URL here after deploying (e.g. `https://ai-prototype.vercel.app`)_

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FRileybujiangwaili%2Fai_prototype&env=GEMINI_API_KEY&envDescription=Google%20AI%20API%20key%20for%20AI%20Auto-Fill&envLink=https%3A%2F%2Faistudio.google.com%2Fapp%2Fapikey)

## Features

- **Tax calculator** — Enter gross income, filing status, deductions; get refund/amount owed
- **AI Auto-Fill** — Describe your situation; Gemini fills the form for you
- **Form 1040 view** — Printable/saveable tax return-style output
- **Firm portal** — Tax preparers can log in and view client calculation history
- **2025 brackets** — Uses current-year standard deductions and tax brackets (single, married filing jointly, head of household)

## Prerequisites

- **Python 3.10+**
- **Git** (for cloning)

## Quick Start

### 1. Clone the repo

```bash
git clone 
cd tax_ai_agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
# Required for AI Auto-Fill (optional — app works without it, but AI will be offline)
GEMINI_API_KEY=your_google_ai_api_key_here
# Optional: pin a specific Gemini model (defaults to gemini-flash-latest)
# GEMINI_MODEL=gemini-3.6-flash
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the app

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Deploy to Vercel

The repo includes a `vercel.json`, so it deploys as a Python serverless function.

1. Click the **Deploy with Vercel** button above (or go to [vercel.com/new](https://vercel.com/new) and import this GitHub repo).
2. When prompted, set the `GEMINI_API_KEY` environment variable (optionally `GEMINI_MODEL`).
3. Click **Deploy**. Vercel gives you a URL like `https://<project>.vercel.app` — paste it into the **Live demo** line above.

Every push to `main` then redeploys automatically, and pull requests get preview URLs.

**Database note:** Vercel's filesystem is read-only, so on Vercel the SQLite DB lives in `/tmp` and is **temporary** (it resets when the function restarts). That's fine for a demo; for persistent history, set `DATABASE_URL` to a hosted MySQL/Postgres database.

---

## Project structure

```
tax_ai_agent/
├── app.py              # Flask app, routes, validation, DB, AI
├── tax_engine.py       # Tax calculation logic (2025 brackets)
├── requirements.txt
├── vercel.json         # Vercel deployment config
├── .env                # API keys (create this, do not commit)
├── .gitignore
├── static/
│   ├── style.css
│   └── main.js
├── templates/
│   ├── base.html
│   ├── index.html      # Main form
│   ├── results.html
│   ├── tax_form.html   # Form output
│   ├── firm_login.html
│   └── history.html
├── instance/           # SQLite DB (created on first run)
│   └── tax_data.db
└── export_data.py      # CLI to export DB records
```

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | For AI | Google AI API key for Auto-Fill (`GOOGLE_API_KEY` also supported) |
| `GEMINI_MODEL` | Optional | Gemini model ID for Auto-Fill; defaults to `gemini-flash-latest` |
| `DATABASE_URL` | Optional | MySQL/PostgreSQL connection string; defaults to SQLite |

---

## Database

- **Default:** SQLite at `instance/tax_data.db` (created automatically)
- **Reset:** Delete `instance/tax_data.db` to start fresh
- **MySQL/Postgres:** Set `DATABASE_URL` in `.env`

---

## Firm portal (sample login)

For testing the preparer view:

- URL: `/firm/login`
- Credentials: `emp001` / `tax2025` or `admin` / `admin123`

**Note:** Replace with real authentication before any production use.

---

## Testing

Run the tax engine tests:

```bash
python test_tax_engine.py
```

---

## Export data

Export stored calculations to CSV:

```bash
python export_data.py
```

---

## Disclaimer

This is a **prototype** for demonstration only. Do not use it for actual tax filing. Consult a tax professional for real returns.
