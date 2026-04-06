import pandas as pd
import numpy as np
import os
import pickle
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

# =========================================================
# 🔥 PATHS (FIXED)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

data_path = os.path.join(ROOT_DIR, "data", "raw")
models_dir = os.path.join(ROOT_DIR, "models")

os.makedirs(models_dir, exist_ok=True)

user_item_path = os.path.join(models_dir, "user_item.pkl")
latent_path = os.path.join(models_dir, "latent_matrix.pkl")


# =========================================================
# 🔥 TRAIN MODEL
# =========================================================
def train_collaborative():

    print("📊 Training collaborative model...")

    movies_file = os.path.join(data_path, "movies.csv")
    ratings_file = os.path.join(data_path, "ratings.csv")

    # ✅ FILE CHECK
    if not os.path.exists(movies_file):
        raise FileNotFoundError(f"❌ Missing file: {movies_file}")

    if not os.path.exists(ratings_file):
        raise FileNotFoundError(f"❌ Missing file: {ratings_file}")

    # ✅ LOAD DATA
    movies = pd.read_csv(movies_file)
    ratings = pd.read_csv(ratings_file)

    if movies.empty or ratings.empty:
        raise ValueError("❌ Empty dataset")

    # =========================================================
    # 🔥 MERGE
    # =========================================================
    df = ratings.merge(movies, on="movieId")

    if df.empty:
        raise ValueError("❌ Merge failed")

    # =========================================================
    # 🔥 USER-ITEM MATRIX
    # =========================================================
    user_item = df.pivot_table(
        index='userId',
        columns='title',
        values='rating'
    ).fillna(0)

    # normalize
    user_item_norm = normalize(user_item)

    # =========================================================
    # 🔥 SAFE SVD (NO CRASH)
    # =========================================================
    n_components = min(50, user_item_norm.shape[1] - 1)

    svd = TruncatedSVD(n_components=n_components, random_state=42)
    latent_matrix = svd.fit_transform(user_item_norm)

    # =========================================================
    # 🔥 SAVE
    # =========================================================
    with open(user_item_path, "wb") as f:
        pickle.dump(user_item, f)

    with open(latent_path, "wb") as f:
        pickle.dump(latent_matrix, f)

    print("✅ Collaborative model trained & saved")


# =========================================================
# 🔥 LOAD MODEL
# =========================================================
def load_collaborative():

    if not os.path.exists(user_item_path) or not os.path.exists(latent_path):
        train_collaborative()

    user_item = pickle.load(open(user_item_path, "rb"))
    latent_matrix = pickle.load(open(latent_path, "rb"))

    return user_item, latent_matrix


# =========================================================
# 🔥 RECOMMEND
# =========================================================
def collaborative_recommend(user_id, n=5):

    user_item, latent_matrix = load_collaborative()

    if user_id not in user_item.index:
        return []

    user_idx = user_item.index.get_loc(user_id)
    user_vec = latent_matrix[user_idx]

    # similarity scores
    scores = np.dot(latent_matrix, user_vec)

    # similar users
    similar_users = np.argsort(scores)[::-1][1:20]

    movie_scores = {}

    for u in similar_users:
        user_ratings = user_item.iloc[u]

        liked_movies = user_ratings[user_ratings >= 4]

        for movie, rating in liked_movies.items():
            movie_scores[movie] = movie_scores.get(movie, 0) + rating

    # sort by score
    ranked = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)

    return [movie for movie, _ in ranked[:n]]