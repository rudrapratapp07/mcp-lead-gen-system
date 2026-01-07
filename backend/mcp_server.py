import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from database import init_db, SessionLocal, Lead
from logic.lead_gen import generate_leads_logic
from logic.enrichment import enrich_lead_logic
from logic.messaging import generate_messages_logic
from logic.sending import send_messages_logic

app = FastAPI(title="MCP Lead Gen Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# --- Pydantic Models for Inputs ---
class GenerateLeadsRequest(BaseModel):
    count: int = 10
    seed: Optional[int] = None

class ProcessLeadRequest(BaseModel):
    lead_id: int

class SendMessageRequest(BaseModel):
    lead_id: int
    mode: str = "dry_run"

# --- API Endpoints (Acting as MCP Tools) ---

@app.post("/tools/generate_leads")
def generate_leads(req: GenerateLeadsRequest):
    """MCP Tool: Generate valid leads."""
    return generate_leads_logic(req.count, req.seed)

@app.post("/tools/enrich_lead")
def enrich_lead_endpoint(req: ProcessLeadRequest):
    """MCP Tool: Enrich a specific lead."""
    return enrich_lead_logic(req.lead_id)

@app.post("/tools/generate_messages")
def generate_messages_endpoint(req: ProcessLeadRequest):
    """MCP Tool: Generate messages for a lead."""
    return generate_messages_logic(req.lead_id)

@app.post("/tools/send_message")
def send_message_endpoint(req: SendMessageRequest):
    """MCP Tool: Send the generated message."""
    return send_messages_logic(req.lead_id, req.mode)

@app.get("/tools/get_stats")
def get_stats():
    """MCP Tool: Get pipeline statistics."""
    db = SessionLocal()
    try:
        total = db.query(Lead).count()
        enriched = db.query(Lead).filter(Lead.status == "ENRICHED").count()
        messaged = db.query(Lead).filter(Lead.status == "MESSAGED").count()
        sent = db.query(Lead).filter(Lead.status == "SENT").count()
        failed = db.query(Lead).filter(Lead.status == "FAILED").count()
        
        return {
            "total_leads": total,
            "enriched": enriched,
            "messaged": messaged,
            "sent": sent,
            "failed": failed
        }
    finally:
        db.close()

@app.get("/api/leads")
def get_leads():
    """Frontend API: Get all leads for the table."""
    db = SessionLocal()
    try:
        leads = db.query(Lead).all()
        return leads
    finally:
        db.close()
        
@app.post("/api/reset")
def reset_db():
    db = SessionLocal()
    try:
        db.query(Lead).delete()
        db.commit()
        return {"status": "cleared"}
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)
