
import re
from typing import List, Tuple

class SkillsExtractor:
    def __init__(self):
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

    def extract_all(self, text: str) -> Tuple[List[str], str]:
        """
        Lightweight replacement for spaCy extraction.
        Uses keyword matching for skills and simple heuristics for location.
        """
        if not text:
            return [], ""
            
        text_lower = text.lower()
        
        # 1. Extract Skills (Keyword Matching)
        extracted_skills = []
        for skill in self.skills_list:
            # Use word boundaries to avoid matching "Java" in "JavaScript"
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.append(skill)
                
        # 2. Extract Location (Simple Heuristic for demo)
        # In a lightweight version, we look for common city patterns 
        # or just return "Unknown" if not easily found without NER.
        # For simplicity in this refactor, we'll try to find common Indian cities as a placeholder.
        cities = ["Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad", "Chennai", "Gurgaon", "Noida", "Remote"]
        location = "Unknown"
        for city in cities:
            if city.lower() in text_lower:
                location = city
                break
        
        return sorted(list(set(extracted_skills))), location

    def extract_skills(self, text: str) -> List[str]:
        skills, _ = self.extract_all(text)
        return skills

# Global instance
skills_extractor = SkillsExtractor()
