
import xgboost as xgb
import numpy as np
from typing import List, Dict, Any, Optional

class JobRanker:
    def __init__(self):
        """
        Initializes the XGBoost model for re-ranking.
        In a production app, the model would be loaded from a pre-trained file.
        """
        # For this demonstration, we'll initialize a placeholder XGBRegressor
        # and use it to demonstrate the ranking flow.
        self.model = xgb.XGBRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5, 
            random_state=42
        )
        # Mock-trained flag for our demo
        self.is_trained = False
        
        # We can pre-train on dummy data to avoid runtime errors if we want,
        # but usually we just load it. Let's provide a 'heuristic_rerank' fallback.

    def extract_features(self, resume_skills: List[str], resume_location: str, job: Dict[str, Any]) -> np.ndarray:
        """
        Extract features based on requirements:
        1. similarity score (pre-calculated from FAISS)
        2. skill overlap (count or ratio)
        3. location match (boolean)
        """
        # Feature 1: Semantic similarity from FAISS
        sim_score = job.get('recommendation_score', 0.0)
        
        # Feature 2: Skill overlap (Ratio of matched job skills)
        job_skills = set(job.get('required_skills', []))
        resume_skills_set = set(resume_skills)
        matched = job_skills.intersection(resume_skills_set)
        skill_score = len(matched) / len(job_skills) if len(job_skills) > 0 else 0.0
        
        # Feature 3: Location Match
        # Check if user location is in job location/description
        job_loc = (job.get('location', '') or '').lower()
        loc_match = 1.0 if resume_location.lower() in job_loc else 0.0
        
        # Return as numerical feature vector
        return np.array([sim_score, skill_score, loc_match], dtype=np.float32)

    def rerank_jobs(self, resume_skills: List[str], resume_location: str, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Re-ranks top K job results using XGBoost-like logic.
        """
        if not jobs:
            return []

        features_list = []
        for job in jobs:
            features = self.extract_features(resume_skills, resume_location, job)
            features_list.append(features)
            
        X = np.array(features_list)
        
        # If model is loaded/trained, we use it. 
        # For the demo, we compute a weighted score to simulate the XGBoost's output logic
        if self.is_trained:
            rerank_scores = self.model.predict(X)
        else:
            # Simulated weights (Learned-like heuristic)
            # Weights could represent importance of similarity vs skills vs location
            W = np.array([0.4, 0.4, 0.2]) # Similarity 40%, skills 40%, location 20%
            rerank_scores = X @ W
            
        for i, job in enumerate(jobs):
            job['rerank_score'] = round(float(rerank_scores[i]), 3)
            # We overwrite recommendation_score for the UI to show the final ranking
            job['recommendation_score'] = job['rerank_score']

        # Sort based on the new ranker score
        return sorted(jobs, key=lambda x: x.get('rerank_score', 0), reverse=True)

# Global instance
job_ranker = JobRanker()
