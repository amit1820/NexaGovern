# 🛡️ NexaGovern — AI Agent Visibility & Governance Platform (MVP)

A working prototype demonstrating AI agent discovery, risk classification, policy enforcement, and EU AI Act compliance gap analysis.

## What It Does

| Tab | Function |
|-----|----------|
| **Agent Discovery** | Inventory of all AI agents across the org. Pre-loaded with 7 sample agents. Add your own and get instant EU AI Act risk classification. |
| **Policy Engine** | Pre-built governance policies (PII detection, human oversight, model registry). Live PII detection demo — paste a prompt and watch it get flagged. |
| **Risk Dashboard** | Real-time compliance score, risk tier distribution (donut chart), department risk heatmap, individual agent risk scores. |
| **Gap Report** | For each high-risk agent, detailed EU AI Act compliance gap analysis showing which Articles apply and what's missing. |

## Quick Start

```bash
# Clone or download this folder
cd nexagovern-mvp

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deploy to Streamlit Cloud (Free)

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Deploy — it's free for public apps

## Demo Walkthrough (for class presentation)

1. **Open the app** → Show the dashboard with 7 pre-loaded agents
2. **Agent Discovery** → Point out the 3 HIGH-RISK agents (Credit Risk Scorer, Fraud Detection, Claims Triage)
3. **Add a new agent** → Register a "Salary Prediction Model" used by HR, selecting "recruitment_screening" as use case → Watch it get classified as HIGH RISK
4. **Policy Engine** → Show the 5 governance policies, then scroll to violations
5. **PII Detection Demo** → Type a prompt with a customer name and credit card number → Watch it get blocked in real time
6. **Risk Dashboard** → Show the donut chart, department heatmap, and individual risk scores
7. **Gap Report** → Select "Credit Risk Scorer v3" → Show the 10 EU AI Act requirements → Most will show ❌ Not Met → This is the compliance gap the company needs to close before August 2026

## Project Structure

```
nexagovern-mvp/
├── app.py              # Main Streamlit application
├── risk_engine.py      # EU AI Act risk classification logic
├── sample_data.py      # Pre-loaded agents, policies, violations
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Dark theme configuration
└── README.md           # This file
```

## Team

- **Amit Kumar** — Lead Developer (Power BI, Python, SQL)
- **Kailash Selvan** — Business Analysis
- **Chanyung Hur** — Regulatory Mapping
- **Preeth Chilvery** — UX & Presentation

Frankfurt School of Finance & Management | MIM Entrepreneurship 2026
