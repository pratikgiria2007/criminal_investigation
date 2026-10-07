# Criminal Investigation Evidence Database
### A 2nd-Year B.Tech DBMS Mini-Project — Flask + MySQL + HTML/CSS/JS

---

## 1. Project Concept

A web application that mimics the backend detectives would use to manage
an investigation: cases, suspects, victims, evidence, crime scenes,
witnesses, interrogations, officers, and forensic samples (DNA and
fingerprints). It demonstrates core DBMS concepts (ER modeling,
normalization, joins, many-to-many relationships) alongside a real
Flask + MySQL + vanilla JS stack, wrapped in a dashboard UI.

**Difficulty:** ⭐⭐⭐⭐⭐ conceptually, but scoped down below to something
a two-person or solo 2nd-year team can realistically finish in 3–4 weeks.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, vanilla JavaScript (fetch API), Chart.js for dashboard graphs |
| Backend | Python 3, Flask, Flask-CORS |
| Database | MySQL 8 |
| DB Driver | `mysql-connector-python` (or `PyMySQL`) |
| Auth (optional) | Flask sessions + `werkzeug.security` password hashing |
| Dev Tools | phpMyAdmin / MySQL Workbench, Postman (for API testing) |

---

## 3. Entity Relationship Overview

**Core entities:** Officers, Cases, Suspects, Victims, Crime_Scenes,
Evidence, Witnesses, Interrogations, DNA_Samples, Fingerprints

**Relationships:**
- Officer 1—N Cases (an officer leads many cases)
- Case 1—N Crime_Scenes, Case 1—N Evidence, Case 1—N Victims
- Case M—N Suspects → junction table `Case_Suspects` (with a `role` column: Primary / Accomplice / Person of Interest)
- Case M—N Witnesses → junction table `Case_Witnesses` (with a `statement` column)
- Evidence M—N Suspects → junction table `Evidence_Suspects` (evidence can implicate several people)
- Evidence 1—N DNA_Samples, Evidence 1—N Fingerprints
- Suspect/Officer/Case 1—N Interrogations (an interrogation links all three)

This gives you **10 base tables + 3 junction tables = 13 tables total**,
which is a solid, defensible scope for a DBMS project without becoming
unmanageable.

*(Draw this as an ER diagram in draw.io or MySQL Workbench for your
submission — a picture here is worth more marks than text.)*

---

## 4. Database Setup

All `CREATE TABLE` statements, sample queries, views, triggers, and
stored procedures are in the companion file **`schema.sql`**. Run it
directly in MySQL Workbench or via:

```bash
mysql -u root -p < schema.sql
```

### What's included in schema.sql
- 13 tables with proper primary keys, foreign keys, `ON DELETE CASCADE` / `ON DELETE SET NULL` rules
- The 4 required analytical queries (repeat suspects, cross-scene fingerprint matches, top-solving officer, cases with no evidence)
- 3 views: `View_Case_Summary`, `View_Officer_Performance`, `View_Suspect_Cases`
- 3 triggers: audit-log interrogations, auto-set `date_closed` when a case is marked Solved, block deletion of a suspect with matched fingerprint evidence
- 3 stored procedures: `GetCaseDetails`, `AddSuspectToCase`, `CountCasesSolvedByOfficer`

---

## 5. Folder Structure

```
crime-investigation-db/
│
├── app.py                     # Flask app entry point
├── config.py                  # DB connection settings
├── requirements.txt
├── schema.sql                 # full DB schema (given)
│
├── routes/
│   ├── cases.py                # /api/cases endpoints
│   ├── suspects.py             # /api/suspects endpoints
│   ├── evidence.py             # /api/evidence endpoints
│   ├── officers.py             # /api/officers endpoints
│   └── dashboard.py            # /api/stats endpoints for dashboard cards/charts
│
├── db.py                      # connection helper (get_connection())
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── cases.html
│   ├── case_detail.html
│   ├── suspects.html
│   ├── evidence.html
│   └── login.html              # optional, if you add officer login
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── cases.js
│   │   └── suspects.js
│   └── img/
│
└── README.md
```

---

## 6. Backend: Flask Routes to Build

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard page |
| `/api/stats/overview` | GET | Card numbers: total cases, open cases, solved cases, total suspects, total evidence |
| `/api/stats/officer-leaderboard` | GET | Uses `View_Officer_Performance` for a bar chart |
| `/api/stats/case-status` | GET | Case counts grouped by status, for a pie chart |
| `/cases` | GET | List all cases (uses `View_Case_Summary`) |
| `/cases/<id>` | GET | Case detail page — suspects, evidence, scenes, witnesses |
| `/api/cases` | POST | Create a new case |
| `/api/cases/<id>` | PUT | Update case (status change triggers `date_closed`) |
| `/api/cases/<id>` | DELETE | Delete case (cascades to scenes/evidence/victims) |
| `/suspects` | GET | List/search suspects |
| `/api/cases/<id>/suspects` | POST | Link suspect to case (calls `AddSuspectToCase` procedure) |
| `/api/suspects/repeat-offenders` | GET | Runs Query 1 (suspects in >1 case) |
| `/api/fingerprints/cross-scene` | GET | Runs Query 2 (fingerprint matches across scenes) |
| `/api/evidence` | GET/POST | List / log new evidence |
| `/api/evidence/<id>/suspects` | POST | Link evidence to a suspect (M:N) |
| `/api/cases/no-evidence` | GET | Runs Query 4 |

Keep each route file thin: parse request → call a function that runs SQL
(or calls a stored procedure) → return JSON with `jsonify()`.

---

## 7. Frontend Pages & the Dashboard

### Dashboard (`/`) — make this the centerpiece
- **Top row of stat cards:** Total Cases, Open Cases, Solved Cases, Total Suspects, Total Evidence Logged — fetched from `/api/stats/overview`
- **Bar chart:** Officer leaderboard (cases solved) — Chart.js, data from `/api/stats/officer-leaderboard`
- **Pie/donut chart:** Case status breakdown (Open / Under Investigation / Solved / Cold Case)
- **Recent activity table:** last 5 cases opened, last 5 interrogations logged
- **Alert panel:** "Cases with no forensic evidence" — a small red-flagged list, pulls Query 4 directly. This is a nice touch that shows off a real DB query on the UI.

### Visual style suggestion
- Dark "case-file" theme: charcoal background (`#1b1f24`), amber/red accent (`#e63946` or `#f4a261`) for alerts, monospace font (`'JetBrains Mono', monospace`) for case IDs/badge numbers to give it a "detective terminal" feel. Avoid default Bootstrap blue — a themed dashboard scores much better than a generic admin template.

### Other pages
- **Cases list** — searchable/filterable table (status, date range), click-through to case detail
- **Case detail** — shows linked suspects (with role tags), evidence list, crime scene(s), witnesses, and a timeline of interrogations
- **Suspects directory** — searchable list, "flag repeat offenders" badge if they appear in >1 case (Query 1 result)
- **Evidence log** — form to add new evidence, tag it to suspects (M:N), and to DNA/fingerprint sub-records

---

## 8. Suggested 4-Week Timeline

| Week | Milestone |
|---|---|
| 1 | Finalize ER diagram, run `schema.sql`, seed ~15–20 rows per table with realistic dummy data (use Faker library or manual inserts) |
| 2 | Build Flask routes + `db.py` connection layer; test every endpoint in Postman before touching the frontend |
| 3 | Build HTML/CSS pages, wire up JS `fetch()` calls, get the dashboard charts rendering with real data |
| 4 | Polish: triggers/views/procedures demo, write README, prepare ER diagram + query-output screenshots for the report, rehearse the demo (viva prep — expect: "what happens if you delete a case?", "why did you use a junction table here?") |

---

## 9. What Will Impress Evaluators (2nd-year scope, done well)

- A working ER diagram that matches the actual schema (no mismatches)
- At least one trigger demoed live (e.g., delete a suspect with matched prints → show the error)
- The 4 analytical queries answered *through the UI*, not just in a SQL console
- Clean use of `ON DELETE CASCADE` vs `ON DELETE SET NULL` — and being able to explain why each choice was made per table
- A dashboard that actually looks like a tool, not a bare HTML table dump

## 10. Stretch Goals (only if core is done early)
- Officer login/session so the "logged in officer" is auto-filled when creating interrogations
- Full-text search across suspects/evidence descriptions
- Export a case file to PDF
- A simple "case timeline" visualization (crime scene date → evidence collected → interrogation → closed)

---

## 11. Deliverables Checklist for Submission

- [ ] ER diagram (image)
- [ ] `schema.sql` (tables, views, triggers, procedures)
- [ ] Flask source code + `requirements.txt`
- [ ] Seed data script (dummy rows)
- [ ] Screenshots: dashboard, case detail, all 4 analytical queries with output
- [ ] README with setup instructions
- [ ] Short report explaining normalization (up to 3NF) and why junction tables were used for the three M:N relationships
