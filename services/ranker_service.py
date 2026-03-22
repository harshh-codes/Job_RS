
import numpy as np
from typing import List, Dict, Any, Optional

class JobRanker:
    """
    Lightweight replacement for XGBoost ranker.
    Uses a weighted rule-based scoring system suitable for free-tier cloud deployment.
    """
    def __init__(self):
        # Placeholder for compatibility
        self.is_trained = False

    def extract_features(self, resume_skills: List[str], resume_location: str, job: Dict[str, Any]) -> np.ndarray:
        """
        Calculates simple numerical scores for different matching criteria.
        """
        # Feature 1: Semantic similarity (now comes from TF-IDF)
        sim_score = job.get('recommendation_score', 0.0)
        
        # Feature 2: Skill overlap (Ratio of matched job skills)
        job_skills = set(job.get('required_skills', []))
        resume_skills_set = set(resume_skills)
        matched = job_skills.intersection(resume_skills_set)
        skill_score = len(matched) / len(job_skills) if len(job_skills) > 0 else 0.0
        
        # Feature 3: Location Match
        job_loc = (job.get('location', '') or '').lower()
        # Simple boolean match or partial match
        loc_match = 1.0 if resume_location.lower() != "unknown" and resume_location.lower() in job_loc else 0.0
        
        return np.array([sim_score, skill_score, loc_match], dtype=np.float32)

    def rerank_jobs(self, resume_skills: List[str], resume_location: str, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Re-ranks top K job results using a weighted heuristic (Linear Combination).
        Matches the intended ranking logic but without heavy dependencies.
        """
        if not jobs:
            return []

        # Heuristic Weights (Total = 1.0)
        # 40% based on TF-IDF relevance, 40% on skill overlap, 20% on location
        W = np.array([0.4, 0.4, 0.2])
        
        for job in jobs:
            features = self.extract_features(resume_skills, resume_location, job)
            # Dot product for rule-based scoring
            rerank_score = float(features @ W)
            
            job['rerank_score'] = round(rerank_score, 3)
            # The UI expects 'recommendation_score' for the match percentage display
            job['recommendation_score'] = job['rerank_score']

        # Sort based on the new ranker score
        return sorted(jobs, key=lambda x: x.get('rerank_score', 0), reverse=True)

# Global instance
job_ranker = JobRanker()
