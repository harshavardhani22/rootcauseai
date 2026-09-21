# RootCause AI — Full-Stack Data Pipeline Root-Cause Intelligence

A dark, premium AI/data-observability dashboard for monitoring data pipelines, analyzing incidents, identifying root causes, and supporting remediation workflows.

Built with a Python Flask backend, SQLite authentication, dashboard APIs, incident analysis, and remediation workflows.

## 🚀 Run Locally

### 1. Create Environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Start the Application
python run.py

Open:

http://127.0.0.1:5055
✨ Included Features
Premium dark RootCause AI landing page
Signup and login backed by SQLite
Password hashing
Dashboard KPI cards
Pipeline health monitoring
Schema-drift root-cause analysis
96% confidence root-cause analysis demo
Root-cause distribution
Failure timeline
Data-quality monitoring
Dependency / blast-radius visualization
Incident queue
Evidence correlation
AI scan API
Remediation API
Responsive dashboard layout
🏗️ Project Structure
RootCause-AI/
│
├── ai_engine/
├── backend/
├── frontend/
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
🔌 API Endpoints
Health & Dashboard
GET /api/health
GET /api/dashboard
GET /api/me
Authentication
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout
Root-Cause Analysis
POST /api/analyze
POST /api/remediate
🔍 Root-Cause Analysis

The system analyzes pipeline incidents using signals such as:

Schema changes
Data-quality issues
Pipeline failures
Evidence correlation
Dependency relationships

The current demonstration includes a schema-drift scenario with a 96% root-cause confidence score.

📊 Dashboard

The dashboard provides visibility into:

Pipeline health
Incident status
Root-cause distribution
Failure timelines
Data-quality metrics
Dependency impact
Blast radius
Evidence correlation
Recommended remediation
🧪 Demo Data

The current dataset is a demo/simulation intended for demonstration and development.

For production usage, replace the DEMO object in:

backend/app.py

with integrations for real pipeline, log, database, and monitoring data.

🛠️ Tech Stack
Backend: Python, Flask
Database: SQLite
Frontend: HTML, CSS, JavaScript
AI/Data Analysis: Python
Authentication: SQLite + password hashing
Version Control: Git, GitHub
🔮 Future Enhancements
Real-time pipeline monitoring
Apache Airflow integration
PySpark integration
Kafka event streaming
AWS CloudWatch integration
Automated incident remediation
Slack/Email notifications
Advanced anomaly detection
LLM-powered incident explanations
Pipeline dependency graphs
👩‍💻 Author

Harsha Vardhani Balusu

B.Tech — Computer Science & Engineering

GitHub: https://github.com/harshavardhani22

📄 License

This project is developed for educational, research, and demonstration purposes.


