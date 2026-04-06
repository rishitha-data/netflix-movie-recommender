from backend.src.recommend import content_recommend, load_models
from backend.src.collaborative_model import collaborative_recommend


def hybrid_recommend(user_id, movie, n=5):

    movies, _, _ = load_models()

    # =========================================================
    # 🔥 FEATURES
    # =========================================================
    def extract_features(text):
        return set(str(text).lower().split())

    # ✅ normalize titles (IMPORTANT FIX)
    movie_features = {
        row["title"].lower(): extract_features(row.get("tags", ""))
        for _, row in movies.iterrows()
    }

    # normalize input movie
    movie = str(movie).strip().lower()

    input_features = movie_features.get(movie, set())

    # ✅ fallback instead of empty
    if not input_features:
        return content_recommend(movie, n)

    # =========================================================
    # 🔥 RECOMMENDATIONS
    # =========================================================
    content = content_recommend(movie, n * 10) or []
    collab = collaborative_recommend(user_id, n * 5) or []

    # =========================================================
    # 🔥 FILTER CONTENT
    # =========================================================
    filtered_content = []

    for item in content:
        title = item.get("title")
        score = item.get("score", 0)

        if not title:
            continue

        features = movie_features.get(title.lower(), set())
        overlap = len(input_features & features)

        if overlap >= 1 and score > 0.15:
            filtered_content.append({
                "title": title,
                "score": score,
                "overlap": overlap
            })

    # fallback if nothing passes filter
    if not filtered_content:
        return content[:n]

    # =========================================================
    # 🔥 SCORING
    # =========================================================
    scores = {}

    for rank, item in enumerate(filtered_content):
        title = item["title"]

        base = item["score"]
        overlap = item["overlap"]
        rank_score = 1 / (rank + 1)

        final = (0.6 * base) + (0.2 * rank_score) + (0.2 * overlap)

        scores[title] = final

    # =========================================================
    # 🔥 COLLAB BOOST
    # =========================================================
    for rank, title in enumerate(collab):

        if title in scores:
            scores[title] += 0.1 * (1 / (rank + 1))

    # =========================================================
    # 🔥 SORT
    # =========================================================
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # =========================================================
    # 🔥 DIVERSITY
    # =========================================================
    selected = []
    used = set()

    for title, score in ranked:
        features = movie_features.get(title.lower(), set())

        if len(features & used) < 3:
            selected.append({
                "title": title,
                "score": round(float(score), 3)
            })
            used.update(features)

        if len(selected) == n:
            break

    # =========================================================
    # 🔥 FALLBACK (ENSURE N RESULTS)
    # =========================================================
    if len(selected) < n:
        existing = {m["title"] for m in selected}

        for title, score in ranked:
            if title not in existing:
                selected.append({
                    "title": title,
                    "score": round(float(score), 3)
                })

            if len(selected) == n:
                break

    return selected