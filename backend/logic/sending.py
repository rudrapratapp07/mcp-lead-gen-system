from database import SessionLocal, Lead
import random
import time

def send_messages_logic(lead_id: int, mode: str = "dry_run"):
    """
    mode: 'dry_run' or 'live'
    """
    db = SessionLocal()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        db.close()
        return {"status": "error", "message": "Lead not found"}
    
    try:
        # Simulate Network Delay
        if mode == "live":
            time.sleep(1) # Simulate SMTP latency
        
        # Simulate Success/Fail
        # 90% success rate in live mode, 100% in dry_run
        if mode == "live" and random.random() < 0.1:
            raise Exception("SMTP Connection Timeout (Simulated)")

        lead.status = "SENT"
        current_logs = list(lead.logs) if lead.logs else []
        current_logs.append({
            "action": "sent", 
            "mode": mode,
            "channel": "email_variant_a", # Defaulting to sending Variant A
            "timestamp": "now"
        })
        lead.logs = current_logs
        
        db.commit()
        return {"status": "success", "lead_id": lead_id, "mode": mode}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
