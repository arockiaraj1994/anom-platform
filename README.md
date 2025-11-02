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

Backend lives in `backend/` and follows a **modular domain-driven** layout.

```
backend/
└── src/anom/
    ├── core/              # shared: config, db, cache, utils
    ├── common_models/     # reusable types and primitives
    ├── modules/
    │   ├── business_def/  # define businesses, schemas, sources
    │   ├── ingestion/     # event ingestion and validation
    │   ├── rules/         # API for rule definitions
    │   ├── rule_engine/   # executes rules in real time
    │   ├── alerts/        # alert storage and lifecycle
    │   ├── suggestions/   # pattern learning (future)
    │   └── views/         # dashboard/view configuration
    ├── api/               # app entrypoint, routers
    └── cli/               # background workers
```

Each module has:
```
domain.py   – business logic entities
repo.py     – DB interactions
service.py  – operations / use cases
api.py      – FastAPI routers
```

---

## 🖥️ Frontend (React / Vite)

Frontend lives in `frontend/` and mirrors backend capabilities:

```
frontend/
└── src/
    ├── pages/          # major screens (Dashboard, Businesses, Alerts)
    ├── components/     # reusable UI parts (tables, charts, forms)
    ├── api/            # axios or fetch wrappers for backend REST
    └── styles/         # theming
```

Primary screens:
- **Dashboard** – summary of all businesses and anomalies
- **Business Detail** – schema, rules, latest events
- **Alerts** – active and historical
- **Suggestions** – rule recommendations

---

## ⚙️ Deployment Layout

```
anom-platform/
├── backend/
├── frontend/
└── docker-compose.yml
```

### Example compose snippet
```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["5173:5173"]
  db:
    image: postgres
  cache:
    image: redis
```

---

## 🧠 Workflow Summary

| Stage | Action | Example |
|-------|---------|---------|
| **1** | Define a Business | “Camel Route Monitoring” |
| **2** | Add Fields | `timestamp`, `routeId`, `durationMs`, `status` |
| **3** | Send Events | POST `/ingest/{businessId}` |
| **4** | Create Rules (API) | `durationMs > 5000`, “no event in 20m” |
| **5** | Engine Evaluates | generates alerts if condition met |
| **6** | UI Displays | business view, alerts, charts |
| **7** | Future | Engine learns baseline and suggests rules |

---

## 📦 Planned Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend Framework | **Python FastAPI** |
| DB / Event Store | **PostgreSQL + TimescaleDB** |
| Cache / Queue | **Redis** |
| Worker Scheduler | **Celery** / **APScheduler** |
| Frontend | **React (Vite + MUI)** |
| Messaging (optional) | **Kafka** or **Redis Streams** |
| Containerization | **Docker / Compose** |
| Observability | **Prometheus + Grafana** |
| Alerts | **Slack / Email / Webhooks** |

---

## 🛏️ Development Phases

1. **Phase 1 – Core API**
   - Business + Field CRUD
   - Event ingestion
   - Rule API
   - Basic alerting

2. **Phase 2 – UI & Dashboard**
   - Generic business views
   - Alert display & acknowledgement

3. **Phase 3 – Profiling Engine**
   - Learn normal behavior
   - Suggest rules automatically

4. **Phase 4 – Advanced Analytics**
   - Time-series visualizations
   - Correlation insights
   - Multi-tenant management

---

## 👨‍💻 Example Use Cases

- **Apache Camel**: track route latency and file arrivals.
- **Finance Tracker**: record expenses and detect overspending.
- **IoT Devices**: detect missing telemetry data.
- **Workflow Monitoring**: identify jobs that stop running.
- **Custom Apps**: plug any event source that can POST JSON.

---

## 📙 Philosophy

> “The schema is data. The rules are data.  
>  The platform just evaluates and visualizes.”

The engine shouldn’t know what Camel or expenses are —  
it just enforces logic that *you define dynamically.*

---

## 🏁 Quick Start (Local Dev)

### Backend (FastAPI)

```bash
cd backend

# (optional) create a virtual environment
python -m venv .venv            # use `python3` on macOS/Linux
.\.venv\Scripts\activate        # PowerShell on Windows
# source .venv/bin/activate      # macOS/Linux equivalent

# install runtime dependencies
python -m pip install -U pip
python -m pip install fastapi "uvicorn[standard]"

# launch the API with hot reload
uvicorn --app-dir src anom.api.main_app:app --reload --host 127.0.0.1 --port 8000
```

- API docs: http://127.0.0.1:8000/docs

### Frontend (React + Vite)

```bash
cd frontend

# install node modules
npm install

# point the UI at the local API (PowerShell example)
$env:VITE_API_URL = "http://127.0.0.1:8000"

# start the dev server
npm run dev -- --host 127.0.0.1
```

- UI: http://127.0.0.1:5173
- macOS/Linux: `export VITE_API_URL=http://127.0.0.1:8000`


---

## 📄 License

MIT License – free for personal or commercial use.

---

**Author:** *MindshiftCoder (Arockiaraj Rayappan)*  
**Created:** 2025  
**Purpose:** A modular, self-defining anomaly-detection platform for any kind of event data.

