from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    company_name = Column(String)
    role = Column(String)
    industry = Column(String)
    website = Column(String)
    email = Column(String)
    linkedin_url = Column(String)
    country = Column(String)
    
    # Enrichment fields
    company_size = Column(String, nullable=True)
    persona_tag = Column(String, nullable=True)
    pain_points = Column(JSON, nullable=True)
    buying_triggers = Column(JSON, nullable=True)
    confidence_score = Column(Integer, nullable=True)
    
    # Message content
    email_variant_a = Column(Text, nullable=True)
    email_variant_b = Column(Text, nullable=True)
    linkedin_variant_a = Column(Text, nullable=True)
    linkedin_variant_b = Column(Text, nullable=True)
    
    # Status tracking
    status = Column(String, default="NEW") # NEW, ENRICHED, MESSAGED, SENT, FAILED
    
    # Logs/Metadata
    created_at = Column(String, default=datetime.datetime.utcnow().isoformat)
    logs = Column(JSON, default=list)

# Database setup
DATABASE_URL = "sqlite:///./leads.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
