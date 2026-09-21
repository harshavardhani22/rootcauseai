# RootCause AI — Full-Stack Data Pipeline Root-Cause Intelligence

A dark, premium AI/data-observability dashboard with a Python Flask backend, SQLite authentication, dashboard APIs, incident analysis and remediation workflow.

## Run locally

### 1. Create environment

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start
```bash
python run.py
```

Open `http://127.0.0.1:5055`.

## Included
- Premium dark RootCause AI landing page
- Signup/login backed by SQLite and password hashing
- Dashboard KPI cards
- Pipeline health monitoring
- 96% schema-drift root-cause analysis
- Root-cause distribution
- Failure timeline
- Data-quality monitoring
- Dependency / blast-radius visualization
- Incident queue
- Evidence correlation
- AI scan API
- Remediation API
- Responsive layout

## API
- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/me`
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/analyze`
- `POST /api/remediate`

The current dataset is a demo/simulation. Replace the `DEMO` object in `backend/app.py` with your real pipeline/log/database integrations when connecting production data.
