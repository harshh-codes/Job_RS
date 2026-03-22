from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from models.job import JobResponse, JobCreate, ResumeAnalysis
from services.job_service import job_service
from services.job_fetcher import job_fetcher
from database import get_db
from models.db_models import JobDB
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/fetch-remote")
async def fetch_remote_jobs(query: str = "data scientist jobs India", db: Session = Depends(get_db)):
    """
    Fetches real-time jobs from Google Jobs via SerpAPI and saves to DB.
    """
    new_jobs = job_fetcher.fetch_google_jobs(query)
    if new_jobs:
        saved_count = job_fetcher.save_to_db(db, new_jobs)
        return {"message": f"Fetched {len(new_jobs)} jobs, saved {saved_count} new unique jobs."}
    return {"message": "No new jobs found."}

@router.get("/", response_model=List[JobResponse])
async def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobDB).all()
    return [job.to_dict() for job in jobs]

@router.post("/recommend", response_model=List[JobResponse])
async def get_recommendations(resume_text: str, db: Session = Depends(get_db)):
    """
    Takes resume text and returns ranked jobs from the database.
    """
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is empty")
    
    jobs = db.query(JobDB).all()
    jobs_list = [job.to_dict() for job in jobs]
    
    # Process recommendations
    extracted_skills, recommended = job_service.recommend_jobs_for_resume(resume_text, jobs_list)
    return recommended


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Handles PDF resume uploads, extracts text, and returns recommendations.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    from utils.helpers import extract_text_from_pdf, clean_text
    
    content = await file.read()
    raw_text = extract_text_from_pdf(content)
    
    if not raw_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    
    cleaned_text = clean_text(raw_text)
    
    # Fetch all jobs from DB for recommendation
    jobs = db.query(JobDB).all()
    jobs_list = [job.to_dict() for job in jobs]
    
    extracted_skills, recommended = job_service.recommend_jobs_for_resume(cleaned_text, jobs_list)
    
    return {
        "filename": file.filename, 
        "extracted_text": cleaned_text[:500] + "...", 
        "extracted_skills": extracted_skills,
        "recommendations": recommended
    }



@router.post("/create", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobDB(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        source="Manual",
        skills=",".join(job.required_skills) if job.required_skills else ""
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job.to_dict()


@router.get("/recommend_jobs", response_model=List[JobResponse])
async def get_jobs_by_resume(resume_text: str, db: Session = Depends(get_db)):
    """
    Takes resume text as query param and returns top 10 ranked jobs from the database using TF-IDF.
    """
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is empty")
    
    # Fetch all jobs from DB
    jobs = db.query(JobDB).all()
    if not jobs:
        return []
        
    jobs_list = [job.to_dict() for job in jobs]
    
    # Process recommendations using the service
    extracted_skills, recommended = job_service.recommend_jobs_for_resume(resume_text, jobs_list)
    
    # Return top 10
    return recommended[:10]


@router.post("/interaction")
async def record_interaction(job_id: int, type: str, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Records a user interaction (click or apply) for a specific job.
    """
    if type not in ['click', 'apply']:
        raise HTTPException(status_code=400, detail="Invalid interaction type")
        
    from models.db_models import InteractionDB
    
    new_interaction = InteractionDB(
        job_id=job_id,
        interaction_type=type,
        user_id=user_id
    )
    db.add(new_interaction)
    db.commit()
    return {"status": "success", "message": f"Interaction {type} recorded for job {job_id}"}

