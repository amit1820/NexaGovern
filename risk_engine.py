"""
NexaGovern — EU AI Act Risk Classification Engine
Maps AI agent characteristics to EU AI Act risk tiers and generates compliance gap analysis.
"""

# EU AI Act Annex III high-risk use cases
HIGH_RISK_USE_CASES = {
    "credit_scoring": {"label": "Credit scoring / lending decisions", "article": "Annex III, 5(b)", "sector": "Financial Services"},
    "insurance_pricing": {"label": "Insurance pricing / risk assessment", "article": "Annex III, 5(a)", "sector": "Financial Services"},
    "fraud_detection": {"label": "Fraud detection in financial transactions", "article": "Annex III, 5(b)", "sector": "Financial Services"},
    "recruitment_screening": {"label": "CV screening / candidate ranking", "article": "Annex III, 4(a)", "sector": "HR / Employment"},
    "employee_monitoring": {"label": "Employee performance monitoring", "article": "Annex III, 4(b)", "sector": "HR / Employment"},
    "student_assessment": {"label": "Student assessment / grading", "article": "Annex III, 3(a)", "sector": "Education"},
    "biometric_id": {"label": "Biometric identification / facial recognition", "article": "Annex III, 1(a)", "sector": "Security"},
    "medical_diagnosis": {"label": "Medical diagnosis / triage", "article": "Annex III, 5(c)", "sector": "Healthcare"},
    "predictive_policing": {"label": "Predictive policing / risk profiling", "article": "Annex III, 6(a)", "sector": "Law Enforcement"},
    "critical_infrastructure": {"label": "Critical infrastructure management", "article": "Annex III, 2(a)", "sector": "Infrastructure"},
}

# EU AI Act Article requirements for high-risk systems
HIGH_RISK_REQUIREMENTS = [
    {"id": "art9", "article": "Article 9", "title": "Risk Management System", "desc": "Establish and maintain a risk management system throughout the AI system's lifecycle"},
    {"id": "art10", "article": "Article 10", "title": "Data Governance", "desc": "Training, validation, and testing datasets must meet quality criteria — relevance, representativeness, free of errors, completeness"},
    {"id": "art11", "article": "Article 11", "title": "Technical Documentation", "desc": "Detailed technical documentation enabling assessment of compliance before the system is placed on the market"},
    {"id": "art12", "article": "Article 12", "title": "Record-Keeping / Logging", "desc": "Automatic recording of events (logs) throughout the system's lifecycle for traceability"},
    {"id": "art13", "article": "Article 13", "title": "Transparency & Information", "desc": "Designed to be sufficiently transparent to enable users to interpret and use the system's output appropriately"},
    {"id": "art14", "article": "Article 14", "title": "Human Oversight", "desc": "Designed to allow effective human oversight during the period the system is in use"},
    {"id": "art15", "article": "Article 15", "title": "Accuracy, Robustness, Cybersecurity", "desc": "Achieve appropriate levels of accuracy, robustness, and cybersecurity throughout lifecycle"},
    {"id": "art17", "article": "Article 17", "title": "Quality Management System", "desc": "Providers must put in place a quality management system ensuring compliance"},
    {"id": "art26", "article": "Article 26", "title": "Deployer Obligations", "desc": "Deployers must use AI systems according to instructions, monitor operations, and inform the provider of risks"},
    {"id": "art27", "article": "Article 27", "title": "Fundamental Rights Impact Assessment", "desc": "Before deploying a high-risk system, deployers must perform an assessment of its impact on fundamental rights"},
]

# Data sensitivity levels
DATA_SENSITIVITY = {
    "pii": {"label": "Personal Identifiable Information (PII)", "risk_weight": 3},
    "financial": {"label": "Financial / credit data", "risk_weight": 3},
    "health": {"label": "Health / medical data", "risk_weight": 4},
    "biometric": {"label": "Biometric data", "risk_weight": 4},
    "employee": {"label": "Employee / HR data", "risk_weight": 2},
    "public": {"label": "Public / non-sensitive data", "risk_weight": 0},
    "proprietary": {"label": "Proprietary business data", "risk_weight": 1},
}


def classify_risk_tier(use_case: str, data_types: list, has_human_oversight: bool, decision_impact: str) -> dict:
    """Classify an AI agent under EU AI Act risk tiers."""

    score = 0
    reasons = []

    # Use case classification
    if use_case in HIGH_RISK_USE_CASES:
        score += 40
        info = HIGH_RISK_USE_CASES[use_case]
        reasons.append(f"Use case classified as HIGH-RISK under {info['article']}: {info['label']}")

    # Data sensitivity
    for dt in data_types:
        if dt in DATA_SENSITIVITY:
            weight = DATA_SENSITIVITY[dt]["risk_weight"]
            score += weight * 5
            if weight >= 3:
                reasons.append(f"Handles sensitive data: {DATA_SENSITIVITY[dt]['label']}")

    # Decision impact
    impact_scores = {"automated_decision": 20, "recommendation": 10, "informational": 3}
    score += impact_scores.get(decision_impact, 0)
    if decision_impact == "automated_decision":
        reasons.append("Makes automated decisions affecting individuals")

    # Human oversight
    if not has_human_oversight:
        score += 15
        reasons.append("No human oversight mechanism in place")

    # Determine tier
    if score >= 50:
        tier = "HIGH"
        tier_color = "#C53030"
        tier_desc = "High-risk system under EU AI Act. Must comply with Articles 9-15, 17, 26-27 before August 2026."
    elif score >= 25:
        tier = "LIMITED"
        tier_color = "#DD6B20"
        tier_desc = "Limited-risk system. Transparency obligations apply (Article 52)."
    else:
        tier = "MINIMAL"
        tier_color = "#2F855A"
        tier_desc = "Minimal-risk system. No specific EU AI Act obligations, but best practices recommended."

    return {
        "tier": tier,
        "tier_color": tier_color,
        "tier_desc": tier_desc,
        "score": min(score, 100),
        "reasons": reasons,
        "applicable_requirements": HIGH_RISK_REQUIREMENTS if tier == "HIGH" else [],
    }


def generate_gap_analysis(agent_name: str, classification: dict, existing_measures: list) -> list:
    """Generate a gap analysis for a high-risk AI agent."""
    gaps = []
    for req in classification["applicable_requirements"]:
        status = "met" if req["id"] in existing_measures else "not_met"
        gaps.append({
            "article": req["article"],
            "title": req["title"],
            "description": req["desc"],
            "status": status,
            "status_label": "✅ Met" if status == "met" else "❌ Not Met",
            "action": "" if status == "met" else f"Implement {req['title'].lower()} for {agent_name}",
        })
    return gaps
