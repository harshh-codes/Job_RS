
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.helpers import clean_text
from services.skills_service import skills_extractor
from services.ranker_service import job_ranker
from services.dummy_data import DUMMY_JOBS

class JobRecommendationService:
    def __init__(self):
        """
        Lightweight replacement for the previous heavy ML backend.
        Uses TF-IDF Vectorization for semantic-like matching on free-tier deployments.
        """
        # Vectorizer instance - much smaller memory footprint than pre-trained models
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.job_mapping = {}

    def _build_index(self, jobs_list: List[Dict[str, Any]]):
        """
        Fits the TF-IDF vectorizer on the job corpus.
        """
        if not jobs_list:
            return

        job_corpus = []
        for job in jobs_list:
            title = job.get('title', '')
            company = job.get('company', '')
            description = job.get('description', '')
            job_skills = ", ".join(job.get('required_skills', []))
            
            # Combine fields to create a rich context for TF-IDF
            combined_text = clean_text(f"{title} {company} {job_skills} {description}")
            job_corpus.append(combined_text)
            
        # Compute TF-IDF Matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(job_corpus)
        
        # Save mapping for result extraction
        self.job_mapping = {i: job for i, job in enumerate(jobs_list)}

    def recommend_jobs_for_resume(self, resume_text: str, jobs_list: List[Dict[str, Any]], top_k: int = 10) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Recommends jobs using TF-IDF and heuristic re-ranking.
        """
        # FALLBACK: If database is empty, use the high-quality demo dataset
        if not jobs_list:
            print("System Check: Database empty, using demo jobs for demonstration.")
            jobs_list = DUMMY_JOBS
            
        if not jobs_list:
            return [], []
            
        # 1. Extract Resume Info (Keyword Matching)
        resume_skills, resume_location = skills_extractor.extract_all(resume_text)
        
        # 2. Build/Update TF-IDF Index
        self._build_index(jobs_list)
        
        try:
            # 3. Vectorize Resume
            resume_vector = self.vectorizer.transform([clean_text(resume_text)])
            
            # 4. Compute Similarities (Cosine Similarity)
            # This replaces the vector search logic
            similarities = cosine_similarity(resume_vector, self.tfidf_matrix).flatten()
            
            # 5. Extract Candidates
            candidate_jobs = []
            # Sort by TF-IDF similarity score descending
            indices = np.argsort(similarities)[::-1]
            
            # We take up to 50 candidates for re-ranking
            for idx in indices[:50]:
                if idx in self.job_mapping:
                    job = self.job_mapping[idx].copy()
                    # Assign the raw TF-IDF score
                    job['recommendation_score'] = round(float(similarities[idx]), 3)
                    candidate_jobs.append(job)
            
            # 6. Re-rank using Rule-Based Logic
            reranked_jobs = job_ranker.rerank_jobs(resume_skills, resume_location, candidate_jobs)
            
            # 7. Generate Explanations
            for job in reranked_jobs:
                job['explanation'] = self._generate_explanation(resume_skills, resume_location, job)
            
            return resume_skills, reranked_jobs[:top_k]
            
        except Exception as e:
            print(f"Error in TF-IDF matching: {e}")
            return resume_skills, jobs_list[:top_k]

    def _generate_explanation(self, resume_skills: List[str], user_location: str, job: Dict[str, Any]) -> str:
        """
        Generates a human-readable explanation for why a job was recommended.
        """
        job_skills = set(job.get('required_skills', []))
        resume_skills_set = set(resume_skills)
        matched_skills = sorted(list(job_skills.intersection(resume_skills_set)))
        
        reasons = []
        
        if matched_skills:
            if len(matched_skills) > 2:
                reasons.append(f"matches your {', '.join(matched_skills[:2])} and {len(matched_skills)-2} other skills")
            else:
                reasons.append(f"matches your {' and '.join(matched_skills)} skills")
        
        job_loc = (job.get('location', '') or '').lower()
        if user_location and user_location.lower() != "unknown" and user_location.lower() in job_loc:
            reasons.append(f"is in your preferred location ({job.get('location')})")
            
        if not reasons:
            reasons.append("aligns with your professional profile")
            
        explanation = "This job " + ", ".join(reasons) + "."
        return explanation.strip()

# Global instance
job_service = JobRecommendationService()
