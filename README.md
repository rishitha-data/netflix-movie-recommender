# 🎬 Netflix Movie Recommender System

An end-to-end **Movie Recommendation System** built using **Machine Learning, FastAPI, and Streamlit**, designed to simulate real-world recommendation engines like Netflix.

---

## 🚀 Overview

This project delivers personalized movie recommendations by combining:

* **Content-Based Filtering** (movie similarity)
* **Collaborative Filtering** (user behavior)
* **Hybrid Recommendation System** (improved accuracy)

Pipeline:

```
Data Preprocessing → Model Training → API Development → Interactive UI
```

---

## ✨ Key Features

* 🔍 Search and select any movie
* 🎯 Hybrid recommendation system (Content + Collaborative)
* ⚡ FastAPI backend for real-time predictions
* 🎨 Streamlit frontend with Netflix-style UI
* 📊 “Because you watched this” recommendations
* ⭐ Displays movie ratings, posters, and year
* 🔄 Dynamic updates on user interaction

---

## 🧠 Recommendation System

### 1️⃣ Content-Based Filtering

* Uses metadata: genres, keywords, cast, overview
* TF-IDF vectorization
* FAISS for fast similarity search

---

### 2️⃣ Collaborative Filtering

* Based on MovieLens ratings
* User-item matrix
* Truncated SVD

---

### 3️⃣ Hybrid Model

```
Final Score = α × Content Score + (1 - α) × Collaborative Score
```

* Balances similarity + personalization
* Improves recommendation accuracy

---

## 📂 Dataset

### 📌 Sources

* TMDB 5000 Dataset
* MovieLens Dataset

---

### 📊 Size

* ~5,000 movies
* ~100,000 ratings
* ~3,000+ tags

---

### 🧹 Preprocessing

* Removed nulls & duplicates
* Parsed JSON fields
* Extracted cast & director
* Created weighted **tags**
* Cleaned text (lowercase, remove symbols)
* Generated feature vectors

---

## 🏗️ Project Structure

```
netflix_recommendation_system/
├── backend/
├── frontend/
├── data/
├── models/
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
git clone https://github.com/rishitha-data/netflix-movie-recommender.git
cd netflix-movie-recommender
```

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run

### Backend

```bash
uvicorn backend.main:app --reload
```

### Frontend

```bash
streamlit run frontend/app.py
```

---

## 🔗 API Documentation

👉 Swagger UI
https://netflix-movie-recommender-bxv3.onrender.com/docs

👉 ReDoc
https://netflix-movie-recommender-bxv3.onrender.com/redoc

> ⚠️ May take ~30–60 seconds to wake up (Render free tier)


## 📡 API Endpoints

### Content-Based

```
GET /recommend?movie=Inception&n=5
```

### Hybrid

```
GET /hybrid?user_id=1&movie=Inception&n=10
```

### Search

```
GET /search?query=Inception&n=10
```

### Trending

```
GET /trending?n=10
```

### Movies Catalog

```
GET /movies?n=50
```

> 📌 Uses query parameters for scalability (industry standard)

---

## 📊 Example Output

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


## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* FAISS
* FastAPI
* Streamlit


## 📈 Future Improvements

* Personalized user history
* Recommendation explanation
* Similarity % score
* Cloud deployment

## 💼 What This Project Demonstrates

* Recommender Systems
* Backend API design
* Frontend integration
* End-to-end ML system
