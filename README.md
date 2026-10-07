# ⚖️ C.I.D. SYSTEM — Criminal Investigation Database

> **A full-stack web application for managing criminal investigations, built as a 2nd-Year B.Tech DBMS Mini-Project.**  
> Stack: **Python Flask · MySQL 8 · Vanilla JS · Chart.js**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Database Design](#database-design)
4. [Features](#features)
5. [Project Structure](#project-structure)
6. [Setup Instructions](#setup-instructions)
7. [API Reference](#api-reference)
8. [User Roles & Permissions](#user-roles--permissions)
9. [Database Objects](#database-objects)
10. [Analytical Queries](#analytical-queries)
11. [UI Pages](#ui-pages)
12. [Deliverables Checklist](#deliverables-checklist)

---

## Project Overview

The **C.I.D. SYSTEM** (Criminal Investigation Database System) is a web application that simulates the backend a detective department would use to manage investigations. It tracks:

- **Cases** — criminal investigations with full lifecycle management
- **Suspects** — persons of interest and repeat offenders
- **Evidence** — forensic evidence linked to cases and suspects (M:N)
- **Crime Scenes** — geolocated scenes with timestamps
- **Officers** — investigating officers and their performance
- **Witnesses** — witness records and statements
- **Interrogations** — officer–suspect interrogation logs
- **DNA Samples & Fingerprints** — forensic sub-records

This project demonstrates:
- ER modeling with 13 tables and 3 junction tables
- Normalization to 3NF
- Many-to-many relationships via junction tables
- SQL views, triggers, stored procedures
- Flask REST API + MySQL backend
- Dark-themed responsive web UI

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3 (custom dark theme), Vanilla JavaScript (Fetch API) |
| **Charting** | Chart.js v4 (bar + doughnut charts) |
| **Backend** | Python 3.10+, Flask 3.x, Flask-CORS |
| **Database** | MySQL 8.x |
| **DB Driver** | `mysql-connector-python` |
| **Auth** | Flask sessions + `werkzeug.security` (bcrypt password hashing) |
| **Fonts** | Inter (sans-serif), JetBrains Mono (monospace) — Google Fonts |

---

## Database Design

### Entity-Relationship Overview

```
Officers ──(1:N)──> Cases ──(1:N)──> Crime_Scenes
                      │
                      ├──(1:N)──> Evidence ──(1:N)──> DNA_Samples
                      │                └──(1:N)──> Fingerprints
                      │
                      ├──(M:N via Case_Suspects)──> Suspects
                      ├──(M:N via Case_Witnesses)──> Witnesses
                      │
                      └──(1:N)──> Victims
                                   └──> Interrogations ──> Officers
```

### Tables (13 total)

| # | Table | Description |
|---|---|---|
| 1 | `Officers` | Law enforcement personnel |
| 2 | `Cases` | Investigation records |
| 3 | `Suspects` | Persons of interest |
| 4 | `Victims` | Case victims |
| 5 | `Crime_Scenes` | Physical locations of incidents |
| 6 | `Evidence` | All forensic evidence items |
| 7 | `Witnesses` | Witness registry |
| 8 | `Interrogations` | Officer–suspect interrogation logs |
| 9 | `DNA_Samples` | DNA sub-records linked to Evidence |
| 10 | `Fingerprints` | Fingerprint sub-records linked to Evidence |
| 11 | `Case_Suspects` *(junction)* | M:N — Cases ↔ Suspects, with `role` column |
| 12 | `Case_Witnesses` *(junction)* | M:N — Cases ↔ Witnesses, with `statement` column |
| 13 | `Evidence_Suspects` *(junction)* | M:N — Evidence ↔ Suspects |

### `Users` Table (auth)
A 14th table `Users` stores login credentials (hashed) and maps to an `officer_id`.

### Normalization
All tables satisfy **3NF**:
- 1NF: Atomic columns, single-valued attributes
- 2NF: No partial dependencies (all non-key attributes depend on the full composite key)
- 3NF: No transitive dependencies (e.g., `date_closed` is derived via a trigger, not stored redundantly)

---

## Features

### 🎨 UI/UX
- **Premium dark theme** with animated grid background, glassmorphism topbar
- **Animated stat counters** (count-up on page load)
- **Live sidebar clock** and system status indicator
- **Toast notification system** (success/error/warning/info)
- **Mobile-responsive** with slide-in sidebar and overlay
- **Global search** bar (searches across cases)
- **Sortable table columns** (click headers to sort)
- **Dual view mode** on Suspects page (Table ↔ Card Grid)

### 🗂️ Case Management (Officials)
- Create, read, update, delete cases
- Filter cases by status (Open / Active / Solved / Cold Case)
- Client-side search by title or officer name
- Click-through to full case detail page
- **Tabbed case detail**: Scenes | Suspects | Evidence
- Link suspects to cases with role assignment
- Log new evidence against a case

### 📊 Dashboard Analytics
- **5 stat cards**: Total Cases, Open Cases, Solved Cases, Suspects, Evidence Items
- **Officer Leaderboard** — visual bar chart + ranked list
- **Case Status Doughnut Chart** — breakdown by status
- **Critical Alerts panel** — Cases missing any forensic evidence
- **Recent Activity feed** — last 8 cases opened, with status indicators
- **Cross-Scene Fingerprint Matches** — forensic intelligence panel (Officials)
- **Solve Rate** bar for Casual users

### 🔍 Suspects Intelligence (Officials only)
- Full suspect database with criminal records
- Repeat offender detection and badge flagging
- Statistics: total suspects, repeat count, avg cases per suspect
- Filter: All | Repeat Offenders | Has Criminal Record
- Card-grid view with threat-level styling

### 🔐 Authentication
- Login / Register with tab-switching UI
- Password hashing via `werkzeug.security`
- Session-based auth with role-based access control
- Auto-redirect to login for unauthenticated requests

---

## Project Structure

```
f:\Criminal_Investigation\
│
├── schema.sql                       # Full DB schema (tables, views, triggers, procedures)
├── dummy_data.sql                   # Realistic sample data for all 13 tables
├── project_outline.md               # Original project brief
├── README.md                        # ← You are here
│
└── crime-investigation-db/          # Flask application root
    │
    ├── app.py                       # Application factory, blueprint registration
    ├── config.py                    # DB + app configuration
    ├── requirements.txt             # Python dependencies
    ├── .env                         # Environment variables (DB credentials)
    │
    ├── db/
    │   └── connection.py            # MySQL connection helper (get_db_connection)
    │
    ├── routes/
    │   ├── auth.py                  # /login, /api/logout, /api/register
    │   ├── dashboard.py             # /api/stats/* endpoints
    │   ├── cases.py                 # /cases, /api/cases CRUD + special queries
    │   ├── suspects.py              # /suspects, /api/suspects + repeat offenders
    │   └── evidence.py             # /api/evidence + fingerprint cross-scene
    │
    ├── templates/
    │   ├── base.html                # App shell (sidebar, topbar, toast system)
    │   ├── login.html               # Auth page (Login + Register tabs)
    │   ├── dashboard.html           # Command center
    │   ├── cases.html               # Case list with filters
    │   ├── case_detail.html         # Individual case file (tabbed)
    │   └── suspects.html            # Suspects database
    │
    └── static/
        ├── css/
        │   └── style.css            # Complete design system (dark theme)
        └── js/
            ├── dashboard.js         # Dashboard data fetching + charts
            ├── cases.js             # Cases table with search/filter/sort
            └── suspects.js          # Suspects table/card dual view
```

---

## Setup Instructions

### Prerequisites
- Python 3.10 or newer
- MySQL 8.x server running locally
- A terminal (PowerShell / CMD / Bash)

### Step 1 — Clone / Download
```bash
cd f:\Criminal_Investigation
```

### Step 2 — Create the Database
Open MySQL Workbench (or terminal) and run:
```sql
CREATE DATABASE crime_db;
USE crime_db;
SOURCE f:/Criminal_Investigation/schema.sql;
SOURCE f:/Criminal_Investigation/dummy_data.sql;
```

Or via command line:
```bash
mysql -u root -p < schema.sql
mysql -u root -p crime_db < dummy_data.sql
```

### Step 3 — Configure Environment
Edit `crime-investigation-db/.env`:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=crime_db
DB_USER=root
DB_PASSWORD=your_mysql_password
SECRET_KEY=your-secret-key-here
```

### Step 4 — Install Python Dependencies
```bash
cd crime-investigation-db
pip install -r requirements.txt
```

`requirements.txt` includes:
```
Flask
Flask-CORS
mysql-connector-python
werkzeug
python-dotenv
```

### Step 5 — Run the Application
```bash
python app.py
```

The server starts at **http://localhost:5000**

### Step 6 — Create an Account
1. Navigate to http://localhost:5000/login
2. Click **Create Account** tab
3. Register a username and password
4. *Note: New accounts get **Casual** access by default.*

### Step 7 — Grant Official Access (Optional)
To give yourself Official (officer) access:
```sql
UPDATE Users SET role = 'Official' WHERE username = 'your_username';
```

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/login` | Login page |
| `POST` | `/login` | Authenticate (JSON body: `{username, password}`) |
| `POST` | `/api/logout` | Clear session |
| `POST` | `/api/register` | Register new Casual user |

### Dashboard Stats

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/stats/overview` | Card numbers: total/open/solved cases, suspects, evidence |
| `GET` | `/api/stats/officer-leaderboard` | Top 5 officers by cases solved |
| `GET` | `/api/stats/case-status` | Case counts grouped by status |
| `GET` | `/api/stats/recent-cases` | 8 most recently opened cases |

### Cases

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `GET` | `/cases` | Cases list page | All |
| `GET` | `/cases/<id>` | Case detail page | All |
| `GET` | `/api/cases` | All cases JSON (uses `View_Case_Summary`) | All |
| `POST` | `/api/cases` | Create new case | Official |
| `PUT` | `/api/cases/<id>` | Update case title/status/officer | Official |
| `DELETE` | `/api/cases/<id>` | Delete case (cascades) | Official |
| `POST` | `/api/cases/<id>/suspects` | Link suspect to case | Official |
| `GET` | `/api/cases/no-evidence` | Cases with zero forensic evidence (Query 4) | Official |

### Suspects

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `GET` | `/suspects` | Suspects list page | Official |
| `GET` | `/api/suspects` | All suspects JSON | Official |
| `GET` | `/api/suspects/repeat-offenders` | Suspects in > 1 case (Query 1) | Official |

### Evidence & Forensics

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `GET` | `/api/evidence` | All evidence items | Official |
| `POST` | `/api/evidence` | Log new evidence | Official |
| `POST` | `/api/evidence/<id>/suspects` | Link evidence to suspect | Official |
| `GET` | `/api/fingerprints/cross-scene` | Fingerprints at > 1 scene (Query 2) | Official |

---

## User Roles & Permissions

| Feature | Casual (Public) | Official (Officer) |
|---|---|---|
| View dashboard stats | ✅ | ✅ |
| View case list | ✅ | ✅ |
| View case detail (scenes only) | ✅ | ✅ |
| View suspects & evidence per case | ❌ Classified | ✅ |
| Access Suspects database | ❌ | ✅ |
| Create / Edit / Delete cases | ❌ | ✅ |
| Log evidence | ❌ | ✅ |
| Link suspects to cases | ❌ | ✅ |
| View officer leaderboard | ❌ | ✅ |
| View critical alerts | ❌ | ✅ |
| View fingerprint matches | ❌ | ✅ |
| View recent activity feed | ❌ | ✅ |

---

## Database Objects

### Views (3)

| View | Purpose |
|---|---|
| `View_Case_Summary` | Aggregates case data with lead officer name, suspect count, evidence count |
| `View_Officer_Performance` | Total cases, solved cases per officer |
| `View_Suspect_Cases` | All cases each suspect is linked to |

### Triggers (3)

| Trigger | Event | Action |
|---|---|---|
| `trg_log_interrogation` | After INSERT on Interrogations | Writes to audit log table |
| `trg_auto_close_date` | Before UPDATE on Cases | Sets `date_closed = NOW()` when status changes to 'Solved' |
| `trg_block_suspect_delete` | Before DELETE on Suspects | Raises error if suspect has matched fingerprint evidence |

### Stored Procedures (3)

| Procedure | Parameters | Purpose |
|---|---|---|
| `GetCaseDetails` | `case_id INT` | Returns full case info: suspects, evidence, scenes |
| `AddSuspectToCase` | `case_id, suspect_id, role` | Safely inserts into `Case_Suspects` junction table |
| `CountCasesSolvedByOfficer` | `officer_id INT` | Returns count of solved cases for a given officer |

---

## Analytical Queries

These 4 queries are the academic deliverables that must be demonstrated through the UI:

### Query 1 — Repeat Offenders
> *"Find all suspects who appear in more than one investigation."*

```sql
SELECT s.suspect_id, s.name, COUNT(cs.case_id) AS case_count
FROM Suspects s
JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id
GROUP BY s.suspect_id, s.name
HAVING COUNT(cs.case_id) > 1;
```
**UI Location:** Suspects page — flagged with 🚨 Repeat badge. Also shown in stats panel.

### Query 2 — Cross-Scene Fingerprint Matches
> *"Find fingerprints that were found at more than one crime scene (potential serial link)."*

```sql
SELECT f.match_reference, COUNT(DISTINCT f.scene_id) AS scene_count
FROM Fingerprints f
WHERE f.match_reference IS NOT NULL
GROUP BY f.match_reference
HAVING COUNT(DISTINCT f.scene_id) > 1;
```
**UI Location:** Dashboard → Cross-Scene Fingerprint Matches panel (Officials only).

### Query 3 — Top Officer by Solved Cases
> *"Find the officer who has solved the most cases."*

```sql
SELECT o.name, COUNT(*) AS solved_cases
FROM Officers o
JOIN Cases c ON o.officer_id = c.lead_officer_id
WHERE c.status = 'Solved'
GROUP BY o.officer_id, o.name
ORDER BY solved_cases DESC
LIMIT 1;
```
**UI Location:** Dashboard → Officer Leaderboard (top rank).

### Query 4 — Cases Without Evidence
> *"Find all cases that have no forensic evidence logged."*

```sql
SELECT c.case_id, c.case_title
FROM Cases c
LEFT JOIN Evidence e ON c.case_id = e.case_id
WHERE e.evidence_id IS NULL;
```
**UI Location:** Dashboard → Critical Alerts panel (Officials only).

---

## UI Pages

### 1. Login Page (`/login`)
- Tab-based Login / Register interface
- Animated gradient background
- Real-time error/success feedback
- Auto-redirect if already logged in

### 2. Command Dashboard (`/`)
- 5 animated stat cards (count-up animation)
- Hero banner with quick actions
- Officer Leaderboard (bar chart + ranked list)
- Case Status Doughnut Chart
- Critical Alerts panel (Query 4)
- Recent Activity feed (last 8 cases)
- Cross-Scene Fingerprint panel (Query 2)

### 3. Case Directory (`/cases`)
- Searchable, filterable table
- Status filter buttons (All / Open / Active / Solved / Cold Case)
- Sortable columns (click headers)
- Inline "View" + "Edit" actions per row
- New Case modal with form validation
- Edit Case modal with full fields
- URL query param search (`/cases?q=riverside`)

### 4. Case Detail (`/cases/<id>`)
- Case header with title, status badge, officer, opened date
- Tabbed interface: Crime Scenes | Suspects | Evidence
- Per-tab count badges
- Inline modals: Edit Case, Link Suspect, Log Evidence
- Delete case with confirmation

### 5. Suspects Database (`/suspects`) — Officials only
- Summary stats (total, repeat offenders, avg cases)
- Search by name/ID
- Filter buttons (All / Repeat Offenders / Has Record)
- Toggle between Table view and Card Grid view
- Repeat offenders highlighted in red

---

## Deliverables Checklist

| Item | Status |
|---|---|
| ER Diagram (draw.io / Workbench) | 📝 Create separately |
| `schema.sql` (tables, views, triggers, procedures) | ✅ Included |
| Flask source code (`routes/`, `templates/`, `static/`) | ✅ Included |
| `requirements.txt` | ✅ Included |
| Seed data (`dummy_data.sql`) | ✅ Included |
| README with setup instructions | ✅ This file |
| Screenshots: dashboard, case detail, all 4 queries | 📝 Take during demo |
| Short normalization report | 📝 Write separately |

### Demo Script (Viva Prep)

1. **Login** as Official user → show dashboard with live stats
2. **Cases page** → filter by "Open", search by name, sort by suspect count
3. **New Case** → create a case, verify it appears in table
4. **Case Detail** → open a case, switch tabs, link a suspect, log evidence
5. **Delete trigger** → try deleting a suspect with matched fingerprints → show error
6. **Dashboard alerts** → point out cases with no evidence (Query 4)
7. **Fingerprint panel** → show cross-scene matches (Query 2)
8. **Suspects page** → filter Repeat Offenders, toggle to Card View
9. **Officer Leaderboard** → explain the View and the query behind it

**Expected viva questions:**
- *"Why did you use a junction table for Case_Suspects?"*  
  → A case can have many suspects, and a suspect can appear in many cases — classic M:N.
- *"What does ON DELETE CASCADE do in Evidence?"*  
  → Deleting a case automatically removes all linked evidence, preventing orphan rows.
- *"Why ON DELETE SET NULL on lead_officer_id?"*  
  → Deleting an officer shouldn't delete the case — just clear the assignment.
- *"Walk me through the trigger for closing a case."*  
  → BEFORE UPDATE on Cases — if NEW.status = 'Solved', set NEW.date_closed = CURDATE().

---

*Built by [Your Name] — B.Tech CSE, 2nd Year DBMS Mini-Project*  
*2026*
# Criminal_Investigation
# criminal_investigation
# criminal_investigation
