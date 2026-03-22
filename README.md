# 🚀 AI-Powered Job Recommendation System

An intelligent, full-stack recruitment platform that bridges the gap between candidates and their ideal careers. Using state-of-the-art NLP and machine learning, this system extracts technical skills from resumes and matches them with high-relevance job opportunities in real-time.

---

## ✨ Key Features

- **📄 Smart Resume Parsing**: Upload PDF resumes to automatically extract technical skills and locations using spaCy NLP.
- **🔍 Semantic Job Search**: Beyond keyword matching—uses **Sentence Transformers** to understand the context of your experience.
- **⚡ High-Performance Retrieval**: Integrated **FAISS** (Facebook AI Similarity Search) for sub-millisecond querying across thousands of job listings.
- **📈 XGBoost Re-ranking**: A two-stage recommendation pipeline that uses a gradient boosting model to rank matches based on skill overlap, location, and semantic score.
- **🤖 Autonomous Job Scraper**: A background scheduler that fetches the latest listings from sources like Google Jobs, Indeed, and LinkedIn simulation.
- **📊 Interaction Tracking**: Learns from user behavior by tracking clicks and applications to improve future ranking accuracy.
- **💡 Match Explanations**: Personalized reasoning for every recommendation (e.g., *"Matches your Python and React skills"*).

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI/ML**: Sentence-Transformers, spaCy, XGBoost, FAISS
- **Database**: PostgreSQL (Production) / SQLite (Local)
- **ORM**: SQLAlchemy
- **Task Scheduling**: APScheduler

### Frontend
- **Library**: React 18 (Vite)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker & Docker Compose
- **Hosting**: Vercel (Frontend), Docker (Backend)

---

## 🏗️ System Architecture

```text
[ Frontend (React) ] <---> [ API (FastAPI) ] <---> [ Database (PostgreSQL) ]
           |                    |                         ^
           |                    |                         |
    (PDF Upload)         (AI Processing)          (Job Scraper)
           |             /      |      \                  |
           v            v       v       v                 |
      [ spaCy ] -> [ FAISS ] -> [ Transformers ] -> [ XGBoost Ranker ]
```

---

## 🖼️ Screenshots

*(Add your high-resolution screenshots here once deployed)*

| Dashboard | Job Recommendations |
| :---: | :---: |
| ![Dashboard Placehoder](https://via.placeholder.com/400x250) | ![Results Placeholder](https://via.placeholder.com/400x250) |

---

## ⚙️ Installation

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/job-rs_system.git
cd job-rs_system

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm

# Configure environment variables (.env)
SERPAPI_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Start the server
python main.py
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/jobs/upload-resume` | Upload PDF and get ranked recommendations |
| `POST` | `/api/jobs/recommend` | Get recommendations from raw text |
| `GET` | `/api/jobs/` | List all available jobs |
| `POST` | `/api/jobs/interaction` | Track clicks and applications |
| `GET` | `/api/jobs/fetch-remote` | Trigger manual job scraping cycle |

---

## 🧠 How the Recommendation Works

1. **Extraction**: spaCy parses the resume to find technical entities (skills) and geopolitical entities (preferred location).
2. **Retrieval (Stage 1)**: The system converts the resume into a high-dimensional vector. **FAISS** then performs a vector similarity search to find the top 50 matches based on semantic meaning.
3. **Re-ranking (Stage 2)**: The **XGBoost** model takes those 50 candidates and calculates a "Super-Score" based on:
   - Vector Similarity (Cos-Sim)
   - Strict Skill Overlap Ratio
   - Location Match Boolean
4. **Explanation**: A rule-based engine generates a human-friendly sentence explaining why the job is a good fit.

---

## 🚀 Future Improvements

- [ ] **Multi-User Authentication**: Individual profiles and saved job lists.
- [ ] **Graph-Based Matching**: Incorporate Knowledge Graphs for better skill relationship understanding (e.g., knowing Python is related to Django).
- [ ] **Resume Rewriting API**: Suggestions to improve the resume based on target job gaps.
- [ ] **Automated Apply**: One-click application submission to external platforms.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

*Give this project a ⭐ if you found it helpful!*
