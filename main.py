from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import job_routes
from database import engine, Base
from services.scheduler_service import job_scheduler
import models.db_models # Critical: must be imported to register tables with Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Start background job scheduler
# Note: In production with uvicorn --reload, this will start twice unless guarded.
if not job_scheduler.scheduler.running:
    job_scheduler.start()

app = FastAPI(
    title="Job Recommendation System API",
    description="Backend API for matching resumes with job postings",
    version="1.0.0"
)

# Configure CORS for React Frontend
origins = [
    "http://localhost:3000", # Default React dev server
    "http://localhost:5173", # Default Vite dev server 
    "*" # Allow all while developing - restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(job_routes.router, prefix="/api/jobs", tags=["Jobs"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Recommendation System API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
