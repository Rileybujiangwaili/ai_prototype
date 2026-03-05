# Database Guide — Where Data Lives & How to Extract It

## Where is the database?

Your app uses **SQLite**, a single-file database:

```
tax_ai_agent/
└── instance/
    └── tax_data.db    ← All tax calculations are stored here
```

Full path: `/Users/ruilinwu/Desktop/github-riley/tax_ai_agent/instance/tax_data.db`

This file is created automatically when you first run `python app.py` and submit a calculation.

---

## When does data get written?

1. User fills out the tax form and clicks "Calculate tax"
2. `app.py` → `calculate()` validates the form
3. `run_tax_calculation()` computes the tax
4. A new `TaxResult` row is inserted into the database
5. User is redirected to the results page

Each calculation = one row in the `tax_results` table.

---

## Table structure: `tax_results`

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Auto-increment ID |
| client_name | String | Optional |
| client_email | String | Optional |
| filing_status | String | single, married_joint, head_of_household |
| gross_income | Numeric | |
| standard_deduction | Numeric | |
| additional_deductions | Numeric | |
| total_deductions | Numeric | |
| taxable_income | Numeric | |
| tax_before_credits | Numeric | |
| tax_owed | Numeric | |
| federal_withheld | Numeric | |
| refund_or_owed | Numeric | Positive = refund, negative = owed |
| is_refund | Boolean | True if refund |
| created_at | DateTime | When the row was saved |

---

## How to view / extract data

### Option 1: Firm portal (built-in)

1. Go to **http://localhost:5000/firm/login**
2. Log in: `emp001` / `tax2025`
3. You see a table of all client returns with Date, Name, Email, Filing status, Gross income, Refund/Owed
4. Click "View" on any row to see full details

This is the simplest way — no command line needed.

---

### Option 2: Run the export script

A script `export_data.py` is in your project. Run:

```bash
cd /Users/ruilinwu/Desktop/github-riley/tax_ai_agent
python export_data.py
```

It prints all records to the terminal. You can also redirect to a file:

```bash
python export_data.py > my_data.txt
```

---

### Option 3: SQLite command line

If you have SQLite installed:

```bash
cd /Users/ruilinwu/Desktop/github-riley/tax_ai_agent
sqlite3 instance/tax_data.db
```

Then run SQL:

```sql
-- List all tables
.tables

-- See all rows
SELECT * FROM tax_results;

-- Export to CSV
.mode csv
.output export.csv
SELECT * FROM tax_results;
.output stdout
```

---

### Option 4: Python REPL (interactive)

```bash
cd /Users/ruilinwu/Desktop/github-riley/tax_ai_agent
python
```

```python
from app import app, db
from app import TaxResult

with app.app_context():
    records = TaxResult.query.all()
    for r in records:
        print(r.id, r.client_name, r.gross_income, r.refund_or_owed, r.created_at)
```

---

### Option 5: DB Browser (GUI tool)

1. Install [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `instance/tax_data.db`
3. Browse tables, run SQL, export to CSV

---

## Quick reference: where in the code?

| What | Where |
|------|-------|
| DB file path | `app.py` lines 35–37: `_DB_PATH = .../instance/tax_data.db` |
| Model (table definition) | `app.py` lines 58–93: `class TaxResult(db.Model)` |
| Save to DB | `app.py` lines 182–199: `tax_record = TaxResult(...); db.session.add(...); db.session.commit()` |
| Read from DB (firm history) | `app.py` lines 284–285: `TaxResult.query.order_by(...).limit(50).all()` |
| Read by ID | `app.py` line 291: `TaxResult.query.get_or_404(id)` |
