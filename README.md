# 🎬 Netflix Recommender System

An end-to-end **Movie Recommendation System** built using **Machine Learning, FastAPI, and Streamlit**, designed to replicate real-world recommendation engines like Netflix.

---

## 🚀 Overview

This project delivers personalized movie recommendations by combining:

* **Content-Based Filtering** (movie similarity)
* **Collaborative Filtering** (user behavior)
* **Hybrid Ranking System** (improved accuracy)

It includes a complete pipeline from **data processing → model training → API serving → UI interaction**.

---

## ✨ Key Features

* 🔍 Search and select any movie
* 🎯 Hybrid recommendation system (Content + Collaborative)
* ⚡ FastAPI backend for real-time predictions
* 🎨 Streamlit frontend with horizontal scrolling UI
* 📊 “Because you watched this” recommendation section
* ⭐ Displays ratings and release year
* 🔄 Dynamic updates on user interaction

---

## 🧠 Recommendation System

### 1. Content-Based Filtering

* Uses movie metadata (tags, genres)
* TF-IDF vectorization
* FAISS for fast similarity search

### 2. Collaborative Filtering

* Based on user ratings
* User-item matrix
* Trained using Truncated SVD

### 3. Hybrid Model

Combines both approaches:

Final Score =

```
α × Content Score + (1 - α) × Collaborative Score
```

* Improves recommendation relevance
* Balances personalization and similarity

---

## 🏗️ Project Structure

```
netflix_recommendation_system/
│
├── backend/
│   ├── src/
│   │   ├── content_model.py
│   │   ├── collaborative_model.py
│   │   ├── hybrid_model.py
│   │   ├── recommend.py
│   │   ├── preprocess.py
│   │   ├── evaluation.py
│   │   ├── config.py
│   │   └── logger.py
│   │
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── raw/
│       ├── movies.csv
│       ├── ratings.csv
│       ├── tags.csv
│
├── models/
│   ├── user_item.pkl
│   ├── latent_matrix.pkl
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/netflix-recommender.git
cd netflix-recommender
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file:

```
API_HOST=127.0.0.1
API_PORT=8000
API_URL=http://127.0.0.1:8000

TMDB_KEY=your_tmdb_api_key

TOP_K=5
HYBRID_ALPHA=0.7

LOG_LEVEL=INFO
ENV=development
```

---

## ▶️ Running the Application

### Start Backend

```
uvicorn backend.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Start Frontend

```
streamlit run frontend/app.py
```

---

## 📡 API Endpoints

### Content-Based Recommendation

```
GET /recommend?movie=Inception&n=5
```

### Collaborative Recommendation

```
GET /collaborative?user_id=1&n=5
```

### Hybrid Recommendation

```
GET /hybrid?user_id=1&movie=Inception&n=10
```

---

## 📊 Sample Output

```json
[
  {
    "title": "The Dark Knight",
    "score": 0.92
  },
  {
    "title": "Interstellar",
    "score": 0.89
  }
]
```

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn (TF-IDF, SVD)
* FAISS (vector similarity search)
* FastAPI (backend)
* Streamlit (frontend)
* TMDB API (movie posters)

---

## 📈 Future Enhancements

* User history tracking & personalization
* Better recommendation explanations
* Similarity score display (e.g., 92% match)
* Genre-based filtering
* Deployment using Docker / Cloud

---

## 💼 Use Case

This project demonstrates:

* Recommender Systems (ML)
* Backend API development
* Frontend UI integration
* End-to-end system design