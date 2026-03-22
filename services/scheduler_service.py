
from apscheduler.schedulers.background import BackgroundScheduler
from services.job_fetcher import job_fetcher
from database import SessionLocal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs_task():
    """
    Background task to scrape jobs and update the database.
    """
    logger.info("Starting background job scraping task...")
    db = SessionLocal()
    try:
        # Define search queries for different roles
        queries = [
            "Software Engineer jobs Bangalore",
            "Data Scientist jobs India",
            "React Developer jobs remote",
            "Python Backend Developer jobs",
            "DevOps Engineer jobs"
        ]
        
        total_saved = 0
        for query in queries:
            logger.info(f"Scraping for: {query}")
            jobs = job_fetcher.fetch_google_jobs(query)
            saved = job_fetcher.save_to_db(db, jobs)
            total_saved += saved
            
        logger.info(f"Scraping task completed. Saved {total_saved} new jobs.")
    except Exception as e:
        logger.error(f"Error in background scraping task: {e}")
    finally:
        db.close()

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        """
        Starts the scheduler and adds the scraping job.
        Default interval: every 6 hours.
        """
        # Run once immediately on start
        self.scheduler.add_job(scrape_jobs_task, 'date')
        
        # Schedule to run every 6 hours
        self.scheduler.add_job(scrape_jobs_task, 'interval', hours=6)
        
        self.scheduler.start()
        logger.info("Job scheduler started (Interval: 6 hours).")

    def shutdown(self):
        self.scheduler.shutdown()

# Global instance
job_scheduler = JobScheduler()
