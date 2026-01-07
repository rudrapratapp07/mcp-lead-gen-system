from database import SessionLocal, Lead
import random
import json

def determine_company_size(industry):
    if industry in ["Technology", "Finance"]:
        return random.choice(["Medium", "Enterprise", "Startup"])
    return random.choice(["Small", "Medium", "Enterprise"])

def determine_persona(role):
    role_lower = role.lower()
    if "vp" in role_lower or "chief" in role_lower or "director" in role_lower:
        return "Decision Maker"
    if "manager" in role_lower:
        return "Manager"
    return "Individual Contributor"

def get_pain_points(industry):
    pains = {
        "Technology": ["Legacy code maintenance", "Cloud costs spiraling", "Hiring talent"],
        "Healthcare": ["Patient data privacy", "Burnout", "Regulatory compliance"],
        "Finance": ["Fraud detection", "Market volatility", "Regulatory reporting"],
        "Retail": ["Supply chain disruptions", "Changing consumer habits", "Inventory management"],
        "Manufacturing": ["Equipment downtime", "Supply chain visibility", "Labor shortage"],
        "Education": ["Student engagement", "Funding cuts", "Remote learning tech"]
    }
    return random.sample(pains.get(industry, ["General inefficiency"]), k=min(2, len(pains.get(industry, []))))

def enrich_lead_logic(lead_id: int):
    db = SessionLocal()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        db.close()
        return {"status": "error", "message": "Lead not found"}
    
    try:
        # Heuristic / Rule-based Enrichment
        lead.company_size = determine_company_size(lead.industry)
        lead.persona_tag = determine_persona(lead.role)
        lead.pain_points = get_pain_points(lead.industry)
        lead.buying_triggers = ["Fiscal year end budget", "New compliance regulation"]
        lead.confidence_score = random.randint(60, 95)
        
        lead.status = "ENRICHED"
        current_logs = list(lead.logs) if lead.logs else []
        current_logs.append({"action": "enriched", "timestamp": "now"}) # Simplified timestamp
        lead.logs = current_logs
        
        db.commit()
        return {"status": "success", "lead_id": lead_id, "enrichment": "offline_rules"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
