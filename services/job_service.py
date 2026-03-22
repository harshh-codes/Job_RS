from typing import List, Dict, Any, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import spacy
from spacy.matcher import PhraseMatcher
from utils.helpers import clean_text
from services.skills_service import skills_extractor
from services.ranker_service import job_ranker

class JobRecommendationService:
    def __init__(self):
        # Initialize the embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384 # Dimension of MiniLM-L6-v2 embeddings
        self.index = faiss.IndexFlatIP(self.dimension) # Inner Product (equivalent to Cosine Similarity for normalized vectors)
        self.job_mapping = {} # To map FAISS indices back to job data

    def _build_index(self, jobs_list: List[Dict[str, Any]]):
        """
        Builds or rebuilds the FAISS index from a list of jobs.
        In a production scenario, this should be done incrementally or during background synchronization.
        """
        if not jobs_list:
            return
            
        # Prepare job corpus: combine title, company, description, and skills
        job_corpus = []
        for job in jobs_list:
            title = job.get('title', '')
            company = job.get('company', '')
            description = job.get('description', '')
            job_skills = ", ".join(job.get('required_skills', []))
            
            combined_text = f"Job Title: {title} at {company}. Skills required: {job_skills}. Description: {description}"
            job_corpus.append(combined_text)
            
        # 1. Compute Embeddings
        embeddings = self.model.encode(job_corpus)
        
        # 2. Normalize for Cosine Similarity
        faiss.normalize_L2(embeddings)
        
        # 3. Reset and Rebuild the index
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # 4. Save mapping for results extraction
        self.job_mapping = {i: job for i, job in enumerate(jobs_list)}

    def recommend_jobs_for_resume(self, resume_text: str, jobs_list: List[Dict[str, Any]], top_k: int = 10) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Extracts skills using spaCy and queries the FAISS index for the top K semantic matches.
        Returns (extracted_skills, recommended_jobs).
        """
        if not jobs_list:
            return [], []
            
        # 1. Extract Resume Skills and Location
        resume_skills, resume_location = skills_extractor.extract_all(resume_text)
        resume_skills_text = ", ".join(resume_skills)
        
        # 2. Prepare rich resume text
        rich_resume = f"Skills: {resume_skills_text}. Content: {clean_text(resume_text)}"
        
        # 3. (Re)build FAISS index
        self._build_index(jobs_list)
        
        try:
            # 4. Embed Query
            query_embedding = self.model.encode([rich_resume])
            faiss.normalize_L2(query_embedding)
            
            # 5. Search FAISS Index (Get top K candidate)
            # We fetch more candidates than top_k to allow the ranker to re-order them
            candidate_k = min(len(jobs_list), top_k * 5)
            scores, indices = self.index.search(np.array(query_embedding).astype('float32'), candidate_k)
            
            # 6. Extract Candidate Results
            candidate_jobs = []
            for score, idx in zip(scores[0], indices[0]):
                if idx in self.job_mapping:
                    job = self.job_mapping[idx].copy()
                    job['recommendation_score'] = round(float(score), 3)
                    candidate_jobs.append(job)
            
            # 7. Re-rank using XGBoost Model
            reranked_jobs = job_ranker.rerank_jobs(resume_skills, resume_location, candidate_jobs)
            
            # 8. Generate Explanations for each job
            for job in reranked_jobs:
                job['explanation'] = self._generate_explanation(resume_skills, resume_location, job)
            
            return resume_skills, reranked_jobs[:top_k]
            
        except Exception as e:
            print(f"Error querying FAISS index: {e}")
            return resume_skills, jobs_list[:top_k]

    def _generate_explanation(self, resume_skills: List[str], user_location: str, job: Dict[str, Any]) -> str:
        """
        Generates a human-readable explanation for why a job was recommended.
        Highlights: Overlapping skills, location match, and semantic relevance.
        """
        job_skills = set(job.get('required_skills', []))
        resume_skills_set = set(resume_skills)
        matched_skills = sorted(list(job_skills.intersection(resume_skills_set)))
        
        reasons = []
        
        # 1. Skill Match Reason
        if matched_skills:
            if len(matched_skills) > 2:
                reasons.append(f"matches your {', '.join(matched_skills[:2])} and {len(matched_skills)-2} other skills")
            else:
                reasons.append(f"matches your {' and '.join(matched_skills)} skills")
        
        # 2. Location Reason
        job_loc = (job.get('location', '') or '').lower()
        if user_location and user_location.lower() != "unknown" and user_location.lower() in job_loc:
            reasons.append(f"is in your preferred location ({job.get('location')})")
            
        # 3. Strength of Match Reason
        score = job.get('recommendation_score', 0)
        if score > 0.8:
            reasons.append("has a very high contextual fit for your background")
        elif not reasons:
            reasons.append("aligns semantically with your professional experience")
            
        if not reasons:
            return "A solid match for your overall professional profile."
            
        # Combine into a sentence
        explanation = "This job " + ", ".join(reasons) + "."
        # Capitalize and fix spacing
        return explanation.replace(" ,", ",").strip()

# Global instance
job_service = JobRecommendationService()

# Instantiate globally or as needed
job_service = JobRecommendationService()
