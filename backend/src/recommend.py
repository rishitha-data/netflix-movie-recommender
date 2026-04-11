import pickle
import os
import faiss
import pandas as pd
import numpy as np
from functools import lru_cache
import re

# =========================================================
# PATH (FIXED)
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(BASE_DIR, "models")

movies_path = os.path.join(models_dir, "movies.pkl")
index_path = os.path.join(models_dir, "faiss.index")
vectors_path = os.path.join(models_dir, "vectors.npy")


# =========================================================
# LOAD MODELS
# =========================================================
@lru_cache(maxsize=1)
def load_models():
    movies = pickle.load(open(movies_path, "rb"))
    index = faiss.read_index(index_path)
    vectors = np.load(vectors_path, mmap_mode='r')

    movies = pd.DataFrame(movies)
    movies["title"] = movies["title"].astype(str)
    movies = movies.drop_duplicates(subset="title").reset_index(drop=True)

    return movies, index, vectors


# =========================================================
# CLEAN QUERY
# =========================================================
def clean_query(query):
    return re.sub(r'[^a-zA-Z0-9 ]', '', str(query).lower().strip())


# =========================================================
# FIND MOVIE (IMPROVED - STRONG MATCHING)
# =========================================================
def find_movie(query, movies):
    query = clean_query(query)

    titles = movies["title"].str.lower()

    # ✅ exact match
    exact = titles[titles == query]
    if not exact.empty:
        return exact.index[0]

    # ✅ smart word matching (better than contains)
    scores = titles.apply(lambda x: len(set(query.split()) & set(x.split())))
    best_idx = scores.idxmax()

    if scores[best_idx] > 0:
        return best_idx

    return None


# =========================================================
# NORMALIZE
# =========================================================
def normalize(vec):
    norm = np.linalg.norm(vec)
    return vec if norm == 0 else vec / norm


# =========================================================
# 🔥 CONTENT RECOMMEND
# =========================================================
def content_recommend(movie: str, n: int = 5):

    movies, index, vectors = load_models()

    idx = find_movie(movie, movies)

    if idx is None:
        return []

    query_vector = normalize(vectors[idx]).reshape(1, -1)

    distances, indices = index.search(query_vector, n * 10)

    results = []
    seen = set()

    for i, score in zip(indices[0], distances[0]):
        if i == idx or i >= len(movies):
            continue

        title = str(movies.iloc[i].title)

        if title in seen:
            continue

        seen.add(title)

        results.append({
            "title": title,
            "score": round(float(score), 3)
        })

        if len(results) == n:
            break

    return results


# =========================================================
# 🔍 SEARCH MOVIES
# =========================================================
def search_movies(query: str, n: int = 10):
    movies, _, _ = load_models()

    query = clean_query(query)

    if not query:
        return movies.head(n)["title"].tolist()

    titles = movies["title"].str.lower()

    # better search ranking
    scores = titles.apply(lambda x: len(set(query.split()) & set(x.split())))
    ranked = scores.sort_values(ascending=False)

    return movies.loc[ranked.index].head(n)["title"].tolist()


# =========================================================
# 🔥 TRENDING MOVIES
# =========================================================
def trending_movies(n: int = 10):
    movies, _, _ = load_models()

    return movies.sample(n=min(n, len(movies)))["title"].tolist()