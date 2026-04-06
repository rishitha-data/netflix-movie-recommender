import pandas as pd
import os
import re
import random
from collections import defaultdict
from backend.src.evaluation import evaluate_model
from backend.src.hybrid_model import hybrid_recommend

# =========================================================
# 🔥 FIX RANDOMNESS (IMPORTANT)
# =========================================================
random.seed(42)

# =========================================================
# 🔥 CLEAN TITLE
# =========================================================
def clean_title(t):
    t = str(t).lower()
    t = re.sub(r"\(\d{4}\)", "", t)
    return t.strip()

# =========================================================
# 🔥 LOAD DATA
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ratings_path = os.path.join(BASE_DIR, "..", "data", "raw", "ratings.csv")
movies_path = os.path.join(BASE_DIR, "..", "data", "raw", "movies.csv")

ratings = pd.read_csv(ratings_path)
movies = pd.read_csv(movies_path)

# =========================================================
# 🔥 MERGE
# =========================================================
data = ratings.merge(movies, on="movieId")

# =========================================================
# 🔥 PARAMETERS
# =========================================================
NUM_USERS = 200
TOP_K = 5

users = data["userId"].unique()
random.shuffle(users)

results = []

# =========================================================
# 🔥 EVALUATION LOOP (FINAL)
# =========================================================
for user in users[:NUM_USERS]:

    try:
        user_data = data[data["userId"] == user]

        # -------- LIKED MOVIES --------
        liked = user_data[user_data["rating"] >= 4]["title"].tolist()

        if len(liked) < 6:
            continue

        random.shuffle(liked)

        split = int(len(liked) * 0.6)
        train = liked[:split]
        test = liked[split:]

        if not train or not test:
            continue

        # =====================================================
        # 🔥 MULTIPLE SEEDS
        # =====================================================
        seed_movies = random.sample(train, min(2, len(train)))

        score_dict = defaultdict(float)

        for seed in seed_movies:
            recs = hybrid_recommend(user, seed, n=10)

            if not recs:
                continue

            for rank, r in enumerate(recs):
                title = clean_title(r["title"])

                # ❌ REMOVE TRAIN MOVIES (CRITICAL FIX)
                if title in [clean_title(t) for t in train]:
                    continue

                # 🔥 RANK WEIGHTING
                score_dict[title] += 1 / (rank + 1)

        if not score_dict:
            continue

        # =====================================================
        # 🔥 FINAL RANKING
        # =====================================================
        ranked = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

        recommended = [t for t, _ in ranked[:TOP_K]]

        relevant = [clean_title(t) for t in test]

        # =====================================================
        # 🔥 EVALUATE
        # =====================================================
        metrics = evaluate_model(recommended, relevant, k=TOP_K)

        results.append(metrics)

    except Exception as e:
        print(f"⚠️ Skipping user {user}: {e}")
        continue

# =========================================================
# 🔥 FINAL RESULTS
# =========================================================
if results:
    df = pd.DataFrame(results)

    print("\n📊 Evaluation Results:")
    print(df.describe())

    print("\n📈 Average Metrics:")
    print(df.mean())

else:
    print("❌ No valid evaluation results")