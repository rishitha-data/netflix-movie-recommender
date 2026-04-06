import numpy as np


# --------------------------------------------------
# 🔹 Precision@K
# --------------------------------------------------
def precision_at_k(recommended, relevant, k=5):
    recommended = list(dict.fromkeys(recommended))[:k]  # remove duplicates

    if k == 0:
        return 0.0

    hits = sum(1 for item in recommended if item in relevant)

    return hits / k


# --------------------------------------------------
# 🔹 Recall@K
# --------------------------------------------------
def recall_at_k(recommended, relevant, k=5):
    recommended = list(dict.fromkeys(recommended))[:k]

    if len(relevant) == 0:
        return 0.0

    hits = sum(1 for item in recommended if item in relevant)

    return hits / len(relevant)


# --------------------------------------------------
# 🔹 Average Precision@K (AP@K)
# --------------------------------------------------
def average_precision_at_k(recommended, relevant, k=5):
    recommended = list(dict.fromkeys(recommended))[:k]

    score = 0.0
    hits = 0

    for i, item in enumerate(recommended):
        if item in relevant:
            hits += 1
            score += hits / (i + 1)

    if hits == 0:
        return 0.0

    return score / min(len(relevant), k)


# --------------------------------------------------
# 🔹 Mean Average Precision@K (MAP@K)
# --------------------------------------------------
def mean_average_precision_at_k(all_recommended, all_relevant, k=5):
    scores = [
        average_precision_at_k(rec, rel, k)
        for rec, rel in zip(all_recommended, all_relevant)
    ]

    return float(np.mean(scores)) if scores else 0.0


# --------------------------------------------------
# 🔹 Evaluate Wrapper (Fixed Naming)
# --------------------------------------------------
def evaluate_model(recommended, relevant, k=5):
    return {
        "precision@k": round(precision_at_k(recommended, relevant, k), 3),
        "recall@k": round(recall_at_k(recommended, relevant, k), 3),
        "ap@k": round(average_precision_at_k(recommended, relevant, k), 3)
    }