from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import job_routes
from database import engine, Base
from services.scheduler_service import job_scheduler
import models.db_models
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Start scheduler (safe guard)
if not job_scheduler.scheduler.running:
    job_scheduler.start()

app = FastAPI(
    title="Job Recommendation System API",
    description="Backend API for matching resumes with job postings",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_routes.router, prefix="/api/jobs", tags=["Jobs"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Recommendation System API"}