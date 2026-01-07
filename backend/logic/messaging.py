from database import SessionLocal, Lead

def generate_email_variant_a(lead):
    pain_point = lead.pain_points[0] if lead.pain_points else "challenges"
    return f"""Subject: Quick question about {lead.company_name}

Hi {lead.full_name.split()[0]},

I noticed you're leading efforts at {lead.company_name}. Many {lead.industry} leaders are struggling with {pain_point}.

We calculate that {lead.company_size} companies waste 20% of budget on this.

Open to a 15-min chat?
"""

def generate_email_variant_b(lead):
    trigger = lead.buying_triggers[0] if lead.buying_triggers else "growth"
    return f"""Subject: {lead.company_name} strategy

Hi {lead.full_name.split()[0]},

Saw your role as {lead.role}. With {trigger} coming up, are you prepared?

We help {lead.persona_tag}s streamline operations.

Worth a quick look?
"""

def generate_linkedin_variant_a(lead):
    return f"Hi {lead.full_name.split()[0]}, saw you're in {lead.industry}. Connecting to share insights on solving {lead.pain_points[0] if lead.pain_points else 'issues'}."

def generate_linkedin_variant_b(lead):
    return f"Hey {lead.full_name.split()[0]}, fellow {lead.industry} professional here. Would love to connect and discuss {lead.company_name}'s growth."

def generate_messages_logic(lead_id: int):
    db = SessionLocal()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        db.close()
        return {"status": "error", "message": "Lead not found"}
    
    try:
        lead.email_variant_a = generate_email_variant_a(lead)
        lead.email_variant_b = generate_email_variant_b(lead)
        lead.linkedin_variant_a = generate_linkedin_variant_a(lead)
        lead.linkedin_variant_b = generate_linkedin_variant_b(lead)
        
        lead.status = "MESSAGED"
        current_logs = list(lead.logs) if lead.logs else []
        current_logs.append({"action": "messages_generated", "timestamp": "now"})
        lead.logs = current_logs
        
        db.commit()
        return {"status": "success", "lead_id": lead_id}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
