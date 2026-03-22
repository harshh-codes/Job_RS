To check the working visit :https://job-rs.vercel.app/


# 🚀 AI-Powered Job Recommendation System (Lightweight)

An efficient, full-stack recruitment platform designed for high-performance job matching. This version is optimized for **cloud free-tier deployment** (e.g., Render, Railway) by using efficient algorithms that run with a minimal memory footprint.

---

## ✨ Key Features

- **📄 Smart Resume Parsing**: Upload PDF resumes to automatically extract technical skills and locations using a high-performance keyword mapping engine.
- **🔍 Relevance-Based Matching**: Uses **TF-IDF Vectorization** to understand the context of your experience and match it with job descriptions.
- **⚡ Fast Similarity Search**: Leverages optimized **Scikit-Learn** cosine similarity for rapid querying across thousands of job listings on shared cloud hardware.
- **📈 Heuristic Re-ranking**: A two-stage pipeline that calculates match scores based on skill overlap, location preference, and semantic relevance.
- **🤖 Autonomous Job Scraper**: A background scheduler that fetches the latest listings from sources like Google Jobs.
- **📊 Interaction Tracking**: Learns from user behavior by tracking clicks and applications to improve future results.
- **💡 Match Explanations**: Personalized reasoning for every recommendation (e.g., *"Matches your Python and React skills"*).

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Math/ML**: Scikit-Learn, NumPy, pandas
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
- **Hosting**: Vercel (Frontend), Render (Backend)

---

## 🏗️ System Architecture

```text
[ Frontend (React) ] <---> [ API (FastAPI) ] <---> [ Database (PostgreSQL) ]
           |                    |                         ^
           |                    |                         |
    (PDF Upload)         (AI Processing)          (Job Scraper)
           |             /      |      \                  |
           v            v       v       v                 |
  [ Keyword Map ] -> [ TF-IDF ] -> [ Cosine Sim ] -> [ Heuristic Ranker ]
```

---

## ⚙️ Installation

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables (.env)
SERPAPI_KEY=your_key_here

# Start the server
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
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

---

## 🧠 How the Recommendation Works

1. **Extraction**: The system parses the resume to find technical entities and preferred location using an internal keyword mapping system.
2. **Retrieval (Stage 1)**: Job descriptions and resumes are vectorized using **TF-IDF**. A cosine similarity search finds the top 50 candidates.
3. **Re-ranking (Stage 2)**: A heuristic engine takes those 50 candidates and calculates a score based on Similarity, Skill Overlap, and Location Match.
4. **Explanation**: A rule-based engine generates a human-friendly sentence explaining the fit.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

*Give this project a ⭐ if you found it helpful!*
