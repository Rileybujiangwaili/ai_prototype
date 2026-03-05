# AI Tax Agent — Architecture & Pipeline Overview

A Flask web app that helps users calculate simplified federal income tax (Form 1040-style) with an optional AI assistant for auto-filling the form from natural language. Includes separate **client** and **firm** (tax preparer) views.

---

## Project Structure

```
tax_ai_agent/
├── app.py              # Flask app, routes, DB, AI, validation
├── tax_engine.py       # Tax calculation logic (brackets, deductions)
├── requirements.txt    # Python dependencies
├── .env                # Secrets (GEMINI_API_KEY, etc.) — not committed
├── .gitignore
├── test_tax_engine.py  # Unit tests for tax engine
├── static/
│   ├── main.js         # Client-side validation + AI Auto-Fill
│   └── style.css       # Global styles
├── templates/
│   ├── base.html       # Layout: header, footer, flash messages
│   ├── index.html      # Client: tax input form + AI assistant
│   ├── results.html    # Client: tax results summary
│   ├── tax_form.html   # Client: Form 1040-style return
│   ├── firm_login.html # Firm: employee login
│   └── history.html    # Firm: list of client calculations
└── instance/
    └── tax_data.db     # SQLite DB (created at runtime)
```

---

## File Roles

### Backend

| File | Role |
|------|-----|
| **app.py** | Flask app, routes, validation, DB models, AI API. Handles `/`, `/calculate`, `/results`, `/tax-form`, `/firm`, `/firm/login`, `/firm/logout`, `/api/parse-narrative`. |
| **tax_engine.py** | Pure tax logic: 2025-style brackets, standard deduction, tax on taxable income. Used by `app.py` for all calculations. |

### Frontend

| File | Role |
|------|-----|
| **templates/base.html** | Base layout: header ("Calculate" link), flash messages, footer ("Firm portal" link). |
| **templates/index.html** | Main client form: AI textarea, name/email, filing status, gross income, deductions, federal withheld. |
| **templates/results.html** | Displays refund/amount owed, breakdown, and link to 1040 form. |
| **templates/tax_form.html** | IRS-style Form 1040 layout (header, line numbers, amounts). |
| **templates/firm_login.html** | Firm login: Employee ID, password. Sample: `emp001` / `tax2025`. |
| **templates/history.html** | Firm-only: table of client returns (date, name, email, filing status, gross income, refund/owed) with "View" links. |

### Static Assets

| File | Role |
|------|-----|
| **static/main.js** | Form validation before submit; AI Auto-Fill button sends narrative to `/api/parse-narrative` and fills form with response. |
| **static/style.css** | Styles for forms, 1040 form, login, history table, flash messages, etc. |

### Config

| File | Role |
|------|-----|
| **requirements.txt** | Flask, Flask-SQLAlchemy, PyMySQL, google-genai. |
| **.env** | `GEMINI_API_KEY` for AI. Optional `DATABASE_URL` for MySQL/Postgres. |

---

## User Flows (Pipeline)

### Client Flow

1. **Enter info (`/`)**  
   User sees the tax form with optional AI assistant. Can either:
   - Type a short narrative → click "Auto-Fill Form" → AI extracts data → form is filled.
   - Or enter data manually (name, email, filing status, gross income, deductions, withheld).

2. **Submit (`POST /calculate`)**  
   - `validate_and_parse_form()` checks required fields and formats.  
   - On error: flash messages, redirect back to index.  
   - On success: `run_tax_calculation()` computes tax → save to DB (`TaxResult`) → store result in session → redirect to `/results`.

3. **Results (`/results`)**  
   - Renders results from session or DB (e.g. after refresh).  
   - Shows refund/owed, breakdown (gross income, deductions, taxable income, tax, etc.).  
   - Links to "View tax return form" and "Start over".

4. **Form 1040 (`/tax-form`)**  
   - Shows IRS-style Form 1040 with calculated values.  
   - Can print or save as PDF.

### Firm Flow (Tax preparer)

1. **Login (`/firm/login`)**  
   - Employee ID + password. Sample: `emp001` / `tax2025` or `admin` / `admin123`.  
   - On success: store `firm_employee_id` in session, redirect to `/firm`.

2. **Client history (`/firm`)**  
   - Protected: redirects to login if not logged in.  
   - Lists up to 50 client returns (date, name, email, filing status, gross income, refund/owed).  
   - "View" opens `/results/<id>` for that return.

3. **Logout (`/firm/logout`)**  
   - Clears `firm_employee_id` from session, redirects to index.

---

## Data Flow

```
┌─────────────────┐     POST /calculate      ┌──────────────────┐
│  index.html     │ ───────────────────────► │  app.py          │
│  (form)        │     validated form data   │  validate + calc │
└────────┬────────┘                          └────────┬─────────┘
         │                                            │
         │ Auto-Fill   POST /api/parse-narrative      │
         │ ──────────────────────────────────────────►│
         │            { narrative }                   │
         │◄────────────────────────────────────────── │
         │            { gross_income, filing_status,   │
         │              additional_deductions,        │
         │              federal_withheld }             │
         │                                            │
         │                                            ▼
         │                                   ┌──────────────────┐
         │                                   │ tax_engine.py    │
         │                                   │ run_tax_calc     │
         │                                   └────────┬─────────┘
         │                                            │
         │                                            ▼
         │                                   ┌──────────────────┐
         │                                   │ TaxResult (DB)   │
         │                                   │ + session        │
         │                                   └────────┬─────────┘
         │                                            │
         │                                            ▼
         │                                   ┌──────────────────┐
         │                                   │ results.html     │
         │                                   │ tax_form.html    │
         │                                   └──────────────────┘
```

---

## Key Components

### Tax Engine (`tax_engine.py`)

- Uses **Decimal** for all monetary values.  
- **Standard deductions** and **brackets** by filing status (single, married_joint, head_of_household).  
- `run_tax_calculation()` returns a dict with: gross_income, standard_deduction, additional_deductions, total_deductions, taxable_income, tax_before_credits, tax_owed, federal_withheld, refund_or_owed, is_refund.

### AI Agent (`app.py` → `/api/parse-narrative`)

- Uses **Google Gemini** (`gemini-2.0-flash`).  
- Prompt: extract `gross_income`, `filing_status`, `additional_deductions`, `federal_withheld` from the narrative.  
- Returns JSON, which the frontend uses to populate the form.

### Database

- **TaxResult**: client_name, client_email, filing_status, gross_income, standard_deduction, additional_deductions, total_deductions, taxable_income, tax_before_credits, tax_owed, federal_withheld, refund_or_owed, is_refund, created_at.  
- SQLite by default; can switch to MySQL/Postgres via `DATABASE_URL`.  
- Migration on startup adds `client_name` and `client_email` to existing DBs if missing.

### Session

- `tax_result` — dict of last calculation (for results and 1040 form).  
- `tax_result_id` — DB id for the last calculation.  
- `firm_employee_id` — logged-in firm user.

---

## Routes Summary

| Route | Methods | Purpose |
|-------|---------|---------|
| `/` | GET | Client: main tax input form |
| `/calculate` | POST | Validate form, compute tax, save to DB, redirect to results |
| `/results` | GET | Client: show tax results |
| `/results/<id>` | GET | Client: show specific result (from firm history) |
| `/tax-form` | GET | Client: Form 1040 view |
| `/firm/login` | GET, POST | Firm: login page |
| `/firm/logout` | GET | Firm: log out |
| `/firm` | GET | Firm: client history (requires login) |
| `/history` | GET | Redirect to `/firm/login` |
| `/api/parse-narrative` | POST | AI: extract tax fields from narrative |

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (for AI Auto-Fill)
export GEMINI_API_KEY="your-key"   # or add to .env

# Run app
python app.py
```

App runs at `http://localhost:5000`. DB and tables are created on first run.
