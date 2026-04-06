# 🎬 Netflix Movie Recommender System

An end-to-end **Movie Recommendation System** built using **Machine Learning, FastAPI, and Streamlit**, designed to simulate real-world recommendation engines like Netflix.

---

## 🚀 Overview

This project delivers personalized movie recommendations by combining:

* **Content-Based Filtering** (movie similarity)
* **Collaborative Filtering** (user behavior)
* **Hybrid Recommendation System** (improved accuracy)

It implements a complete pipeline from:

```
Data Preprocessing → Model Training → API Development → Interactive UI
```

---

## ✨ Key Features

* 🔍 Search and select any movie
* 🎯 Hybrid recommendation system (Content + Collaborative)
* ⚡ FastAPI backend for real-time predictions
* 🎨 Streamlit frontend with Netflix-style UI
* 📊 “Because you watched this” recommendation section
* ⭐ Displays movie ratings, posters, and release year
* 🔄 Dynamic updates on user interaction

---

## 🧠 Recommendation System

### 1️⃣ Content-Based Filtering

* Uses movie metadata:

  * Genres
  * Keywords
  * Cast
  * Overview
* Text converted into vectors using **TF-IDF**
* Fast similarity search using **FAISS**

---

### 2️⃣ Collaborative Filtering

* Based on user ratings (MovieLens dataset)
* User-item interaction matrix
* Latent feature extraction using **Truncated SVD**

---

### 3️⃣ Hybrid Model

Combines both approaches:

```
Final Score = α × Content Score + (1 - α) × Collaborative Score
```

* Improves recommendation quality
* Balances similarity and personalization

---

## 📂 Dataset

### 📌 Sources

* **TMDB 5000 Dataset** (movies metadata)
* **MovieLens Dataset** (user ratings & interactions)

These datasets are widely used in building recommendation systems in both academia and industry ([GitHub][1])

---

### 📊 Dataset Size

| Dataset           | Size             |
| ----------------- | ---------------- |
| TMDB Movies       | ~5,000 movies    |
| MovieLens Ratings | ~100,000 ratings |
| Tags              | ~3,000+          |

---

### 🧹 Data Preprocessing

The following steps were applied:

#### 🔹 Cleaning

* Removed null values
* Removed duplicate entries

#### 🔹 Feature Extraction

* Parsed JSON columns (genres, keywords, cast, crew)
* Extracted:

  * Top cast members
  * Director

#### 🔹 Feature Engineering

* Combined features into a single **"tags" column**
* Applied weighting:

  * Genres → high importance
  * Keywords → medium
  * Cast/Director → contextual

#### 🔹 Text Processing

* Lowercasing
* Removing special characters
* Removing spaces in names
* Tokenization

#### 🔹 Final Output

* Cleaned dataset with meaningful feature vectors for similarity search

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
git clone https://github.com/rishitha-data/netflix-movie-recommender.git
cd netflix-movie-recommender
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

## 🔑 Environment Variables

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

### Backend

```
uvicorn backend.main:app --reload
```

---

### Frontend

```
streamlit run frontend/app.py
```

---

## 📡 API Endpoints

### Content-Based

```
GET /recommend?movie=Inception&n=5
```

### Collaborative

```
GET /collaborative?user_id=1&n=5
```

### Hybrid

```
GET /hybrid?user_id=1&movie=Inception&n=10
```

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
* Scikit-learn (TF-IDF, SVD)
* FAISS (Vector Search)
* FastAPI
* Streamlit
* TMDB API

## 📈 Future Improvements

* Personalized recommendations based on user history
* Explainable AI ("Because you watched X")
* Similarity score display (e.g., 92% match)
* Deployment using Docker / AWS

## 💼 What This Project Demonstrates

* Recommender Systems (ML)
* Backend API Development
* Frontend UI Design
* End-to-End ML System Architecture

