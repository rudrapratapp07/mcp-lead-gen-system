from faker import Faker
import random
from database import SessionLocal, Lead

fake = Faker()

INDUSTRIES = ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Education"]
ROLES = {
    "Technology": ["CTO", "DevOps Engineer", "Frontend Developer", "Product Manager"],
    "Healthcare": ["Medical Director", "Chief Surgeon", "Nurse Practitioner", "Hospital Administrator"],
    "Finance": ["CFO", "Investment Banker", "Financial Analyst", "Risk Manager"],
    "Retail": ["Store Manager", "Supply Chain Analyst", "Buyer", "Merchandiser"],
    "Manufacturing": ["Plant Manager", "Operations Director", "Quality Control", "Safety Officer"],
    "Education": ["Principal", "Superintendent", "Professor", "Admissions Officer"]
}

def generate_leads_logic(count: int, seed: int = None):
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)
    
    db = SessionLocal()
    generated_ids = []
    
    try:
        for _ in range(count):
            industry = random.choice(INDUSTRIES)
            role = random.choice(ROLES[industry])
            
            lead = Lead(
                full_name=fake.name(),
                company_name=fake.company(),
                role=role,
                industry=industry,
                website=fake.url(),
                email=fake.email(),
                linkedin_url=f"https://linkedin.com/in/{fake.user_name()}",
                country=fake.country(),
                status="NEW",
                logs=[{"action": "created", "timestamp": fake.iso8601()}]
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)
            generated_ids.append(lead.id)
            
        return {"status": "success", "count": count, "ids": generated_ids}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
