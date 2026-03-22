import spacy
from spacy.matcher import PhraseMatcher
from typing import List, Tuple
import os

class SkillsExtractor:
    def __init__(self):
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model is not downloaded (though we are downloading it)
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
            
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        # Comprehensive list of software engineering skills
        self.skills_list = [
            # Programming Languages
            "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Scala", "Dart", "R", "SQL",
            # Web Frameworks
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", "Express", "Laravel", "Ruby on Rails", "Svelte", "Next.js", "Nuxt.js",
            # Databases
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Cassandra", "Elasticsearch", "Oracle", "DynamoDB", "MariaDB",
            # Cloud & DevOps
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "CI/CD", "GitHub Actions", "Git", "GitLab", "Linux", "Unix",
            # Data Science & AI
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Keras", "Data Analysis", "Statistics",
            # Tools & Other
            "Jira", "Slack", "Confluence", "Postman", "Swagger", "GraphQL", "REST API", "Microservices", "System Design", "Unit Testing", "TDD", "Agile", "Scrum",
            "HTML", "CSS", "Tailwind", "Bootstrap", "Redux", "Webpack", "Vite"
        ]
        
        # Add patterns to matcher
        patterns = [self.nlp.make_doc(text) for text in self.skills_list]
        self.matcher.add("SKILLS", patterns)

    def extract_all(self, text: str) -> Tuple[List[str], str]:
        """
        Extracts both skills and the likely location (GPE entities) from the resume.
        Returns (skills, location).
        """
        if not text:
            return [], ""
            
        doc = self.nlp(text)
        
        # 1. Extract Skills
        matches = self.matcher(doc)
        extracted_skills = []
        for match_id, start, end in matches:
            span = doc[start:end]
            extracted_skills.append(span.text)
            
        # 2. Extract Location (GPE - Geopolitical Entities)
        # Using the last GPE mentioned as the likely location
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        location = "Unknown" if not locations else locations[-1]
        
        # Remove duplicates and sort skills
        return sorted(list(set(extracted_skills))), location

    def extract_skills(self, text: str) -> List[str]:
        skills, _ = self.extract_all(text)
        return skills

# Global instance
skills_extractor = SkillsExtractor()
