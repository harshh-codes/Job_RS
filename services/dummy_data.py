
from typing import List, Dict, Any

# Enhanced Realistic Dummy Job Dataset covering AI, Web, Data Science, Backend, and Cloud.
DUMMY_JOBS: List[Dict[str, Any]] = [
    # --- AI & MACHINE LEARNING ---
    {
        "id": 1001,
        "title": "AI Research Scientist",
        "company": "DeepMind Innovations",
        "location": "Remote / London",
        "description": "Develop and pioneer next-generation Large Language Models (LLMs). Experience with PyTorch, Transformer architectures, and fine-tuning strategies is essential.",
        "required_skills": ["Python", "PyTorch", "NLP", "Deep Learning", "Transformers", "LLM"],
        "salary_range": "₹40,00,000 - ₹65,00,000",
        "job_type": "Full-time",
        "source": "AI Labs"
    },
    {
        "id": 1002,
        "title": "Machine Learning Engineer (NLP)",
        "company": "NeuralText AI",
        "location": "Bangalore, India",
        "description": "Build high-performance NLP pipelines for text classification and sentiment analysis. You will work extensively with Scikit-learn, Pandas, and Hugging Face.",
        "required_skills": ["Python", "Machine Learning", "NLP", "Pandas", "Scikit-learn", "NLTK"],
        "salary_range": "₹18,00,000 - ₹32,00,000",
        "job_type": "Full-time",
        "source": "LinkedIn"
    },
    # --- WEB DEVELOPMENT (Frontend & Fullstack) ---
    {
        "id": 1003,
        "title": "Senior React Developer",
        "company": "Frontend Studio",
        "location": "Pune, India",
        "description": "Lead the development of our modern enterprise dashboard. Expert knowledge of React 18, Tailwind CSS, and State Management (Redux/Zustand) is required.",
        "required_skills": ["React", "JavaScript", "TypeScript", "Tailwind CSS", "Redux", "Vite", "HTML", "CSS"],
        "salary_range": "₹22,0,000 - ₹35,00,000",
        "job_type": "Full-time",
        "source": "Direct"
    },
    {
        "id": 1004,
        "title": "Full Stack Engineer (Next.js & Node)",
        "company": "WebFlow Tech",
        "location": "Hyderabad, India",
        "description": "End-to-end development of scalable SaaS products. Use Next.js for SSR/ISR and Node.js for high-throughput API endpoints.",
        "required_skills": ["React", "Next.js", "Node.js", "TypeScript", "PostgreSQL", "Prisma", "AWS"],
        "salary_range": "₹15,00,000 - ₹28,00,000",
        "job_type": "Full-time",
        "source": "Glassdoor"
    },
    # --- BACKEND & DISTRIBUTED SYSTEMS ---
    {
        "id": 1005,
        "title": "Backend Systems Architect (Go/Python)",
        "company": "Scalable Systems",
        "location": "Remote",
        "description": "Design and implement high-performance microservices. Experience with Redis, Kafka, and distributed consistency is a must.",
        "required_skills": ["Go", "Python", "FastAPI", "Redis", "Kafka", "PostgreSQL", "Microservices"],
        "salary_range": "₹35,00,000 - ₹55,00,000",
        "job_type": "Full-time",
        "source": "LinkedIn"
    },
    # --- DATA SCIENCE & ANALYTICS ---
    {
        "id": 1006,
        "title": "Lead Data Scientist",
        "company": "Insight Analytics",
        "location": "Mumbai, India",
        "description": "Transform raw financial data into actionable business intelligence. High proficiency in SQL, R, and statistical modeling is expected.",
        "required_skills": ["Python", "R", "SQL", "Statistics", "Data Analysis", "Tableau", "Matplotlib"],
        "salary_range": "₹25,00,000 - ₹45,00,000",
        "job_type": "Full-time",
        "source": "AngelList"
    },
    # --- CLOUD, DEVOPS & SRE ---
    {
        "id": 1007,
        "title": "Cloud Infrastructure Engineer (AWS)",
        "company": "CloudReady Inc.",
        "location": "Gurgaon, India",
        "description": "Automate cloud infrastructure using Terraform and Ansible. Ensure 99.9% uptime for our global Kubernetes clusters.",
        "required_skills": ["AWS", "Kubernetes", "Docker", "Terraform", "Ansible", "Linux", "CI/CD"],
        "salary_range": "₹28,00,000 - ₹42,00,000",
        "job_type": "Full-time",
        "source": "Indeed"
    },
    {
        "id": 1008,
        "title": "Site Reliability Engineer (SRE)",
        "company": "SafeStack Ops",
        "location": "Bangalore, India",
        "description": "Optimize our build and release pipelines. Focus on observability, performance monitoring, and incident response management.",
        "required_skills": ["Linux", "Python", "Prometheus", "Grafana", "Jenkins", "Kubernetes", "Bash"],
        "salary_range": "₹20,0,000 - ₹35,00,000",
        "job_type": "Full-time",
        "source": "Direct"
    }
]

def get_demo_jobs() -> List[Dict[str, Any]]:
    """Returns the enhanced dummy dataset for platform demonstration."""
    return DUMMY_JOBS
