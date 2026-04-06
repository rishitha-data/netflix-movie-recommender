# 🎬 Netflix Recommender System

An end-to-end **Movie Recommendation System** built using **Machine Learning, FastAPI, and Streamlit**, designed to simulate real-world recommendation engines like Netflix.

---

## 🚀 Overview

This project delivers personalized movie recommendations by combining:

* **Content-Based Filtering** (movie similarity)
* **Collaborative Filtering** (user behavior)
* **Hybrid Ranking System** (improved accuracy)

It implements a complete pipeline from **data preprocessing → model training → API serving → interactive UI**.

---

## ✨ Key Features

* 🔍 Search and select movies
* 🎯 Hybrid recommendation system (Content + Collaborative)
* ⚡ FastAPI backend for real-time predictions
* 🎨 Streamlit frontend with Netflix-style UI
* 📊 “Because you watched this” recommendations
* ⭐ Displays ratings, posters, and release year
* 🔄 Dynamic updates on user interaction

---

## 🧠 Recommendation System

### 1️⃣ Content-Based Filtering

* Uses movie metadata (genres, keywords, cast, overview)
* Text converted into vectors using **TF-IDF**
* Similarity search powered by **FAISS (Facebook AI Similarity Search)**

---

### 2️⃣ Collaborative Filtering

* Based on user-item interactions (ratings)
* Builds user-item matrix
* Learns latent features using **Truncated SVD**

---

### 3️⃣ Hybrid Model

Combines both approaches:

```
Final Score = α × Content Score + (1 - α) × Collaborative Score
```

* Improves recommendation quality
* Balances personalization and similarity

---

## 📂 Dataset

### 📌 Source

* **TMDB 5000 Dataset**
* **MovieLens Dataset (100K / Latest small)**

---

### 📊 Dataset Size

| Dataset           | Approx Size      |
| ----------------- | ---------------- |
| TMDB Movies       | ~5,000 movies    |
| MovieLens Ratings | ~100,000 ratings |
| Tags              | ~3,000+ entries  |

---

### 🧹 Preprocessing Steps

The following steps are applied before training:

* Removed null values and duplicates
* Parsed JSON fields (genres, keywords, cast, crew)
* Extracted:

  * Top cast members
  * Director information
* Combined features into a single **"tags" column**
* Applied text cleaning:

  * Lowercasing
  * Removing special characters
  * Removing spaces between words
* Weighted important features:

  * Genres (higher weight)
  * Keywords
  * Cast & Director
* Generated final feature vector for each movie

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
│   ├── raw/
│   │   ├── movies.csv
│   │   ├── ratings.csv
│   │   ├── tags.csv
│   │   ├── tmdb_5000_movies.csv
│   │   └── tmdb_5000_credits.csv
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

### 1. Clone Repository

```
git clone https://github.com/your-username/netflix-recommender.git
cd netflix-recommender
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate      (Windows)
source venv/bin/activate   (Mac/Linux)
```

---

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

---

### Start Frontend

```
streamlit run frontend/app.py
```

---

## 📡 API Endpoints

### 🔹 Content-Based Recommendation

```
GET /recommend?movie=Inception&n=5
```

### 🔹 Collaborative Recommendation

```
GET /collaborative?user_id=1&n=5
```

### 🔹 Hybrid Recommendation

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

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn (TF-IDF, SVD)
* FAISS (Vector Search)
* FastAPI (Backend)
* Streamlit (Frontend)
* TMDB API (Posters & Metadata)

## 📈 Future Improvements

* Personalized recommendations based on user history
* Explainable recommendations ("Because you watched X")
* Similarity score display (e.g., 92% match)
* Genre-based filtering
* Deployment using Docker / AWS

## 💼 Use Case

This project demonstrates:

* Recommender Systems (Machine Learning)
* Backend API development
* Frontend UI integration
* End-to-end ML system design