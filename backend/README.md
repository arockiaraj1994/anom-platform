# 🧠 Anom Platform

A **generic anomaly detection and event intelligence platform** designed to monitor diverse business activities — from **Apache Camel integrations** to **daily finance tracking**, **IoT streams**, or any other event-driven workflow.

It allows users to **define their own business cases via UI or API**, ingest data in a normalized format, define (or auto-discover) rules, and visualize anomalies across systems.

---

## 🚀 Vision

Instead of hardcoding specific logic for Camel logs or any single use case, **Anom Platform** lets users describe their own “business” via configuration:

- **Business Definition:** What are we tracking? (e.g. SFTP file flow, expense entry)
- **Schema Definition:** What fields exist in this business? (e.g. timestamp, amount, duration)
- **Rules:** How to detect anomalies or thresholds?
- **Views:** How to visualize the events and alerts?
- **Sources:** Where data originates from (API push, UI form, or stream)

So the platform becomes **generic and self-describing**.

---

## 🧩 Core Ideas

### 1. Dynamic Business Use Cases
Users can create new “businesses” directly from the UI — each representing a unique use case:
- Example 1: Monitor **Camel SFTP route timings**
- Example 2: Track **daily personal expenses**
- Example 3: Capture **IoT temperature readings**

Each business comes with its own schema, rules, and dashboards.

---

### 2. Rule System (API-First)
Rules are defined via API (no complex UI editor required initially):

- **Immediate rules:** simple conditions (e.g., `durationMs > 5000`)
- **Window rules:** time-based checks (e.g., “no file in 20 minutes”)
- **Aggregate rules:** (e.g., “sum(amount) > 2000 today”)

Later, the system will **auto-learn patterns** from data (profiling engine).

---

### 3. Auto Pattern Learning (future)
The platform will analyze historical data and automatically **propose rules** such as:
> “Typical file arrival for `SFTP-BANK-A` is every 15 min. Alert if no file for > 20 min.”

Users can review and approve these **suggested rules** instead of defining them manually.

---

### 4. Generic UI
A thin frontend where users can:
- View all defined businesses
- Inspect recent events
- See alerts
- Review rule suggestions
- Manage definitions (fields, rules, views)

---

## 🌿 Architecture Overview

### 1️⃣ Ingestion Layer
Receives normalized events via API and validates them against the business schema.  
Stores raw events in a time-series database and emits them to the rule engine.

### 2️⃣ Definition Layer
Stores the metadata:
- Business definitions
- Schema fields
- Rules and their conditions
- View configurations
- Sources and tokens

### 3️⃣ Processing Layer
Two major engines:
- **Real-Time Rule Engine**: evaluates new events and raises alerts.
- **Profile Engine**: analyzes history to derive typical behavior and suggest rules.

### 4️⃣ Storage Layer
Logical databases:
- **Event Store** – time-series events  
- **Definition Store** – metadata and configuration  
- **Alert Store** – anomalies, acknowledgements, history  
- **Cache Layer** – fast access for active rules and last-seen timestamps

### 5️⃣ Presentation Layer
- FastAPI REST API (for ingestion, definitions, and querying)
- React frontend for monitoring and configuration
- Alert notifications via Slack, email, or webhooks

---

## 🐍 Backend (Python / FastAPI)

This section explains **only** the backend part in depth. The idea is to keep the backend generic so it can support *any* business you define from the UI/API.

### 1. Goals
- Accept **business definitions** (your use cases)
- Accept **schema/field definitions** for those businesses
- Accept **events** for those businesses (Camel logs, daily expenses, IoT data…)
- Evaluate **rules** on the incoming events
- Emit **alerts** when rules match
- Later: **learn patterns** and propose rules automatically

The backend must **not** hardcode a domain like “Camel” or “Finance”. It only understands: business → schema → events → rules → alerts.

---

### 2. Backend Structure

```text
backend/
├── pyproject.toml
├── README.md
├── scripts/
├── alembic/
└── src/
    └── anom/
        ├── core/               # shared infra (config, db, cache, errors)
        ├── common_models/      # IDs, time helpers, shared pydantic bits
        ├── modules/            # ← real features live here
        │   ├── business_def/   # define businesses, fields, sources, views
        │   ├── ingestion/      # ingest & validate events
        │   ├── rules/          # store rules (API-first)
        │   ├── rule_engine/    # run rules on events (real-time)
        │   ├── alerts/         # store & manage alerts
        │   ├── suggestions/    # future: auto-rule / pattern discovery
        │   └── views/          # optional: UI view configs
        ├── api/                # FastAPI app + router wiring
        └── cli/                # workers / engines you run separately
```

This gives you **one Python project** with **multiple logical modules**, which you can later split out if needed.

---

### 3. Core Layer (`src/anom/core/`)
Holds things every module needs:
- `config.py` → reads env / settings / URLs
- `db.py` → creates DB engine + session
- `cache.py` → Redis or in-memory cache (for last-seen timestamps, rule cache)
- `security.py` → API keys / auth (future)
- `errors.py` → a few base exceptions so modules can raise consistent errors

Keeping this in one place prevents circular imports between feature modules.

---

### 4. Modules (the real features)
Each module follows the same pattern:

```text
modules/<name>/
  ├── domain.py   # pure models, no DB
  ├── repo.py     # persistence (SQLAlchemy or similar)
  ├── service.py  # orchestration / use cases
  └── api.py      # FastAPI router
```

This **repeatable pattern** means adding a new capability (e.g. audit logs) is easy: make a new module with those 4 files.

---

#### 4.1 `modules/business_def/`
**What it does:**
- Creates a **business** (e.g. "Camel Monitoring", "Daily Expenses")
- Adds **fields** to that business (name, type, required, enum, default)
- (Optionally) registers **sources** (how data comes in)
- (Optionally) registers **views** (how to display data)

**Why it’s important:** every other module *reads* from this. Ingestion asks it “what is the schema?”, rule engine asks it “does this business exist?”.

Main operations you’ll implement:
- `create_business(...)`
- `list_businesses(...)`
- `get_business(id)`
- `add_field(business_id, field_def)`
- `list_fields(business_id)`

---

#### 4.2 `modules/ingestion/`
**What it does:**
1. Receives an event for a business: `POST /ingest/{businessId}`
2. Looks up the **schema** from `business_def`
3. Validates the payload against that schema
4. Wraps it into a **standard envelope** (id, ts, business, payload, schemaVersion)
5. Stores it (event store)
6. Notifies the **rule engine** that a new event is ready

This keeps ingestion **fast** and **generic** — the business-specific logic never leaks here.

Key parts:
- `domain.py` → `EventEnvelope`, `ValidatedEvent`
- `validators.py` → required, type checks, enums
- `repo.py` → insert into `events` table (or Timescale later)
- `service.py` → ties it all together
- `api.py` → FastAPI route

---

#### 4.3 `modules/rules/`
**What it does:** stores rule definitions. This is your **API-first rule story**.

Example rule (conceptual):
```json
{
  "business_id": "camel-monitoring",
  "name": "Route slow",
  "condition": {
    "type": "field_compare",
    "field": "durationMs",
    "op": ">",
    "value": 5000
  },
  "action": {
    "type": "create_alert",
    "severity": "warning",
    "message": "Route exceeded 5s"
  },
  "enabled": true
}
```

Main operations:
- `create_rule(business_id, rule_def)`
- `list_rules(business_id)`
- `get_rule(rule_id)`
- `update_rule(rule_id, patch)`
- `delete_rule(rule_id)`
- (optional) `test_rule(...)`

This module **does not run** rules — it only **stores** them.

---

#### 4.4 `modules/rule_engine/`
**What it does:** actually **evaluates** rules when a new event arrives.

Flow:
1. Event is ingested
2. Engine loads cached rules for that business
3. Engine evaluates event vs each rule
4. If hit → tells `alerts` module to create an alert

For time-based / missing-data rules, a background runner in this module will periodically check latest timestamps.

Files:
- `evaluator.py` → logic to check 1 rule vs 1 event
- `dispatcher.py` → glue between ingestion and evaluator
- `workers.py` → periodic jobs ("no event in 20m")

---

#### 4.5 `modules/alerts/`
**What it does:** stores and manages alerts.

Alert contents (conceptually):
- `id`
- `business_id`
- `rule_id`
- `severity`
- `message`
- `event_context`
- `status` (open/acked/closed)
- `created_at`, `acked_at`, `acked_by`

Operations:
- `create_alert(...)` (usually called from rule engine)
- `list_alerts(business_id, status=...)`
- `ack_alert(alert_id, user)`
- `close_alert(alert_id)`

This is what the frontend will show in its “Alerts” page.

---

#### 4.6 `modules/suggestions/` (future)
**What it does:** reads historical events (for 1 business), detects patterns, and writes **draft rules**. Those drafts can then be promoted to real rules by the user.

This is where your idea “in future program understands pattern from data” will live.

---

### 5. API Layer (`src/anom/api/`)
This is the web entrypoint. It should:
- create a FastAPI app
- include routers from each module
- set up CORS (so your React app can talk to it)
- expose `/health`

Rough wiring:
```python
from fastapi import FastAPI
from anom.modules.business_def import api as business_api
from anom.modules.ingestion import api as ingestion_api
from anom.modules.rules import api as rules_api
from anom.modules.alerts import api as alerts_api

app = FastAPI(title="Anom Platform API")
app.include_router(business_api.router, prefix="/businesses", tags=["businesses"])
app.include_router(ingestion_api.router, prefix="/ingest", tags=["ingestion"])
app.include_router(rules_api.router, prefix="/rules", tags=["rules"])
app.include_router(alerts_api.router, prefix="/alerts", tags=["alerts"])
```

This keeps each module independent.

---

### 6. Data Flow (Backend-Only)

1. **Define**: user / UI / script calls
   - `POST /businesses`
   - `POST /businesses/{id}/fields`
   - `POST /businesses/{id}/rules`
2. **Ingest**: external system (Camel, expense app) calls
   - `POST /ingest/{businessId}`
3. **Evaluate**: rule engine picks up new event and tries all rules for that business
4. **Alert**: if rule matches → create alert in alerts module
5. **Display**: frontend calls `/alerts` and `/businesses/{id}/events`

---

### 7. Storage Model (conceptual)
You can start with **one Postgres** with tables like:
- `businesses`
- `business_fields`
- `rules`
- `events` (time-series like)
- `alerts`

Later, move `events` to TimescaleDB / ClickHouse if volume grows.

---

### 8. Dev Runbook (local)

1. Create & activate venv
2. Install deps from `pyproject.toml` / `requirements.txt`
3. Run app:
   ```bash
   uvicorn src.anom.api.main_app:app --reload
   ```
4. Open docs: `http://localhost:8000/docs`
5. Define a business
6. Ingest an event for that business
7. Create a rule
8. Ingest again → see alert

---

### 9. Why This Design Works for You
- You said: **“From the UI user should be able to add more business case.”** → that’s `business_def/`
- You said: **“I will give API to create Rule”** → that’s `rules/`
- You said: **“In future program understand pattern”** → that’s `suggestions/`
- You said: **“Camel is