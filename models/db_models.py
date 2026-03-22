from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class JobDB(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_key = Column(String(255), unique=True, index=True) # Used for deduplication
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    source = Column(String(100), default="Google Jobs")
    
    # Skills extracted (as comma separated for simple DB storage)
    skills = Column(String(500), nullable=True)

    __table_args__ = (
        # Combination to find duplicates if job_key not provided
        UniqueConstraint('title', 'company', 'location', name='_uix_job_unique'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "job_type": "Full-time", # Default or detect
            "required_skills": self.skills.split(",") if self.skills else [],
            "source": self.source
        }

class InteractionDB(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    interaction_type = Column(String(50)) # e.g., 'click', 'apply'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Placeholder for user_id once authentication is added
    user_id = Column(String(255), nullable=True)
