import os
import serpapi
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class JobFetcherService:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        
    def fetch_google_jobs(self, query: str = "data scientist jobs India") -> List[Dict[str, Any]]:
        if not self.api_key:
            print("Warning: SERPAPI_KEY not found in environment.")
            return []
            
        params = {
            "engine": "google_jobs",
            "q": query,
            "hl": "en",
            "gl": "in" # India
        }

        try:
            client = serpapi.Client(api_key=self.api_key)
            results = client.search(params)
            
            jobs = results.get("jobs_results", [])
            structured_jobs = []
            
            for idx, job in enumerate(jobs):
                structured_jobs.append({
                    "id": idx + 100, # Offset for local IDs
                    "title": job.get("title", "N/A"),
                    "company": job.get("company_name", "N/A"),
                    "location": job.get("location", "N/A"),
                    "description": job.get("description", "N/A"),
                    "required_skills": self._infer_skills(job.get("description", "")),
                    "job_type": job.get("detected_extensions", {}).get("schedule_type", "Full-time"),
                    "salary_range": job.get("detected_extensions", {}).get("salary", "Competitive"),
                    "apply_link": job.get("related_links", [{}])[0].get("link", "#")
                })
            
            return structured_jobs
        except Exception as e:
            print(f"Error fetching jobs from SerpAPI: {e}")
            return []

    def save_to_db(self, db_session, jobs_list: List[Dict[str, Any]]):
        """
        Saves a list of jobs to the database, skipping duplicates.
        """
        from models.db_models import JobDB
        from sqlalchemy.exc import IntegrityError

        saved_count = 0
        for job in jobs_list:
            # Create a unique key for deduplication based on title + company + location
            # Or use a source-specific key if available
            
            db_job = JobDB(
                title=job['title'],
                company=job['company'],
                location=job['location'],
                description=job['description'],
                source="Google Jobs",
                skills=",".join(job['required_skills']) if job['required_skills'] else ""
            )
            
            try:
                # Check for existing before adding to avoid common integrity errors if possible
                existing = db_session.query(JobDB).filter_by(
                    title=job['title'], 
                    company=job['company'], 
                    location=job['location']
                ).first()
                
                if not existing:
                    db_session.add(db_job)
                    db_session.commit()
                    saved_count += 1
            except IntegrityError:
                db_session.rollback()
                continue
            except Exception as e:
                print(f"DB Error: {e}")
                db_session.rollback()
        
        return saved_count

    def _infer_skills(self, description: str) -> List[str]:
        """
        Uses the advanced SkillsExtractor service (spaCy-based) to find skills in descriptions.
        """
        from services.skills_service import skills_extractor
        return skills_extractor.extract_skills(description)

job_fetcher = JobFetcherService()
