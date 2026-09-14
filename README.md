# LearnWise AI

> **“Education that adapts to every learner.”**

LearnWise AI is an enterprise-ready Smart Education web application that transforms conventional one-pace classroom instruction into an adaptive intelligence loop. It diagnoses concept-level learning gaps, traces prerequisite root causes using Directed Acyclic Graphs (DAG), predicts explainable academic risk, powers a Socratic AI Tutor, and streams real-time telemetry to teachers with one-click interventions.

---

## 🌟 Core Innovations

1. **Root-Cause Prerequisite Gap Analysis (DAG):**
   Instead of vaguely telling a student *"You are weak in Calculus"*, LearnWise traces prerequisite dependencies (e.g. *Integration by Parts* $\rightarrow$ *Indefinite Integrals* $\rightarrow$ *Differentiation Basics* $\rightarrow$ *Algebraic Manipulation*). It accurately pinpoints the lowest unmastered prerequisite and warns the student and teacher before further confusion compounds.

2. **Explainable Multi-Factor Academic Risk Engine:**
   Implements an exact, transparent risk formula:
   $$\text{Risk} = 0.35 \times \text{Performance Risk} + 0.25 \times \text{Attendance Risk} + 0.20 \times \text{Assignment Risk} + 0.20 \times \text{Engagement Risk}$$
   Classifies learners into **LOW** (0-39), **MEDIUM** (40-69), and **HIGH** (70-100) and displays clear, bulleted reasons without stigmatizing learners.

3. **Socratic AI Tutor:**
   Context-aware AI tutor grounded in the student's actual curriculum, mastery score, and recent mistakes. Guides learners step-by-step using pedagogical questioning rather than just handing out raw solutions. Features a 100% reliable pedagogical fallback engine so the system works even offline or without API keys.

4. **Real-Time Teacher Live Telemetry:**
   WebSocket streaming enables teachers to observe practice submissions, assessment completions, and risk shifts in real time without refreshing the browser.

5. **Closed-Loop Remediation:**
   Teacher creates an intervention $\rightarrow$ Student receives targeted remediation $\rightarrow$ Reassessment triggered $\rightarrow$ Mastery score and risk dynamically recalculated.

---

## 👥 Role-Based Access & Demo Accounts

The database comes pre-seeded with realistic test accounts:

| Role | Email | Password | Description |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@learnwise.ai` | `LearnWise@2026` | Platform-wide analytics, curriculum hierarchy & RBAC |
| **Teacher** | `teacher@learnwise.ai` | `LearnWise@2026` | Dr. Eleanor Vance (Classes, student diagnostics, interventions) |
| **Student** | `arjun@learnwise.ai` | `LearnWise@2026` | Arjun Mehta (**High Risk**, Indefinite Integrals root gap) |
| **Student** | `priya@learnwise.ai` | `LearnWise@2026` | Priya Sharma (**Medium Risk**, steady progress) |
| **Student** | `rohit@learnwise.ai` | `LearnWise@2026` | Rohit Verma (**Low Risk**, high mastery) |

*A one-click demo filler is available on the `/login` screen for fast evaluation during hackathon presentations.*

---

## 🛠️ Technology Stack

- **Frontend:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons, Recharts
- **Backend:** Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn, WebSockets
- **Database:** PostgreSQL compatible (defaults out-of-the-box to SQLite for instant local zero-friction execution)
- **Security:** Bcrypt password hashing, JWT Access & Refresh tokens, strict RBAC
- **Deployment:** Docker & `docker-compose.yml`

---

## 🚀 Quick Start Guide

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt email-validator
python seed.py        # Seeds users, curriculum, questions & telemetry
python run.py         # Starts API on http://localhost:8000
```
Interactive API documentation: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev           # Starts Next.js on http://localhost:3000
```

Open `http://localhost:3000` in your browser.

---

## 🧪 Automated Testing

LearnWise AI includes automated backend pytest tests verifying:
- Teacher and Student authentication
- Duplicate registration & duplicate class enrollment prevention
- Invite token verification & invalid token rejection
- Strict role isolation (Students cannot access teacher endpoints)
- Multi-tenant data isolation (Teacher A cannot access Teacher B's students)
- Mathematical accuracy of composite risk formula ($0.35P + 0.25A + 0.20M + 0.20E$)
- Prerequisite DAG root-cause diagnostic engine

Run the test suite:
```bash
cd backend
python -m pytest -v
```

---

## 🐳 Docker Deployment

To launch the full production stack with PostgreSQL:
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
