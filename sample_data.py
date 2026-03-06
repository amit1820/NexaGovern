"""
NexaGovern — Sample Agent Data
Pre-loaded AI agents for demo purposes.
"""

COMMON_AGENTS = [
    {
        "name": "ChatGPT Enterprise",
        "platform": "OpenAI",
        "department": "Multiple",
        "use_case": "general",
        "description": "General-purpose LLM used across departments for content generation, summarization, and Q&A",
        "data_types": ["proprietary"],
        "decision_impact": "informational",
        "has_human_oversight": True,
    },
    {
        "name": "Microsoft Copilot",
        "platform": "Microsoft",
        "department": "Multiple",
        "use_case": "general",
        "description": "AI assistant integrated into Office 365 for email drafting, document summarization, and data analysis",
        "data_types": ["pii", "proprietary"],
        "decision_impact": "informational",
        "has_human_oversight": True,
    },
    {
        "name": "Credit Risk Scorer v3",
        "platform": "Custom (Python/sklearn)",
        "department": "Risk / Lending",
        "use_case": "credit_scoring",
        "description": "ML model scoring loan applications for creditworthiness. Trained on 5 years of historical lending data.",
        "data_types": ["pii", "financial"],
        "decision_impact": "automated_decision",
        "has_human_oversight": False,
    },
    {
        "name": "TalentMatch AI",
        "platform": "HuggingFace (fine-tuned BERT)",
        "department": "HR",
        "use_case": "recruitment_screening",
        "description": "NLP model ranking CVs against job descriptions. Deployed via internal API, used by recruiters.",
        "data_types": ["pii", "employee"],
        "decision_impact": "recommendation",
        "has_human_oversight": True,
    },
    {
        "name": "Customer Service Bot",
        "platform": "OpenAI + Slack",
        "department": "Customer Support",
        "use_case": "general",
        "description": "Slack bot answering customer queries using RAG over product documentation. Escalates to human for complex issues.",
        "data_types": ["pii", "proprietary"],
        "decision_impact": "informational",
        "has_human_oversight": True,
    },
    {
        "name": "Fraud Detection Engine",
        "platform": "Custom (XGBoost)",
        "department": "Compliance",
        "use_case": "fraud_detection",
        "description": "Real-time transaction monitoring flagging suspicious patterns. Auto-blocks transactions above risk threshold.",
        "data_types": ["pii", "financial"],
        "decision_impact": "automated_decision",
        "has_human_oversight": False,
    },
    {
        "name": "Claims Triage Assistant",
        "platform": "Azure OpenAI",
        "department": "Insurance Operations",
        "use_case": "insurance_pricing",
        "description": "Classifies incoming insurance claims by severity and routes to appropriate handler. Uses customer health and financial data.",
        "data_types": ["pii", "health", "financial"],
        "decision_impact": "recommendation",
        "has_human_oversight": True,
    },
]

SAMPLE_POLICIES = [
    {"id": "pol_pii", "name": "No PII in LLM Prompts", "description": "Block or redact personally identifiable information before sending to external LLMs", "severity": "Critical", "active": True},
    {"id": "pol_approval", "name": "High-Risk AI Requires Approval", "description": "Any AI system classified as high-risk must receive CISO approval before deployment", "severity": "Critical", "active": True},
    {"id": "pol_human", "name": "Human Oversight for Automated Decisions", "description": "AI systems making automated decisions affecting individuals must have human review capability", "severity": "High", "active": True},
    {"id": "pol_logging", "name": "All AI Actions Must Be Logged", "description": "Every AI agent interaction must be logged for audit trail purposes", "severity": "Medium", "active": True},
    {"id": "pol_model_registry", "name": "Model Registry Required", "description": "All deployed ML models must be registered with version, training data, and performance metrics", "severity": "Medium", "active": False},
]

SAMPLE_VIOLATIONS = [
    {"agent": "Credit Risk Scorer v3", "policy": "Human Oversight for Automated Decisions", "timestamp": "2026-03-01 14:23", "severity": "Critical", "status": "Open", "detail": "Model auto-rejected 3 loan applications with no human review"},
    {"agent": "Customer Service Bot", "policy": "No PII in LLM Prompts", "timestamp": "2026-03-03 09:15", "severity": "Critical", "status": "Open", "detail": "Customer credit card number detected in prompt sent to OpenAI API"},
    {"agent": "TalentMatch AI", "policy": "Model Registry Required", "timestamp": "2026-02-28 11:00", "severity": "Medium", "status": "Resolved", "detail": "Model deployed without registry entry — now registered"},
    {"agent": "Fraud Detection Engine", "policy": "Human Oversight for Automated Decisions", "timestamp": "2026-03-04 16:45", "severity": "High", "status": "Open", "detail": "Auto-blocked 12 transactions without human review queue"},
    {"agent": "ChatGPT Enterprise", "policy": "No PII in LLM Prompts", "timestamp": "2026-03-05 08:30", "severity": "High", "status": "Open", "detail": "Employee pasted customer email with personal data into ChatGPT"},
]
