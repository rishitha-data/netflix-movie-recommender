import pickle
import os
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.src.preprocess import load_data


# =========================================================
# 🔥 PATH SETUP (FIXED)
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
models_dir = os.path.join(BASE_DIR, "models")   # ✅ FIXED

os.makedirs(models_dir, exist_ok=True)

index_path = os.path.join(models_dir, "faiss.index")
movies_path = os.path.join(models_dir, "movies.pkl")
tfidf_path = os.path.join(models_dir, "tfidf.pkl")
vectors_path = os.path.join(models_dir, "vectors.npy")


# =========================================================
# 🔥 TRAIN MODEL
# =========================================================
def train_model():

    print("🚀 Loading data...")
    df = load_data()

    # =========================================================
    # 🔥 SAFETY CHECK
    # =========================================================
    if df is None or df.empty:
        raise ValueError("❌ Dataset is empty or not loaded properly")

    # Clean tags
    df["tags"] = df["tags"].fillna("")
    df = df[df["tags"].str.strip() != ""]

    if df.empty:
        raise ValueError("❌ No valid data after preprocessing")

    print(f"✅ Total movies: {len(df)}")

    # =========================================================
    # 🔥 TF-IDF (OPTIMIZED FOR LOW RAM)
    # =========================================================
    print("🔠 Vectorizing text...")

    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=8000,     # ✅ reduced (LOW RAM)
        ngram_range=(1, 2),
        min_df=2,              # ✅ ignore rare words
        max_df=0.85
    )

    sparse_vectors = tfidf.fit_transform(df["tags"])

    # convert to float32 (lighter)
    vectors = sparse_vectors.astype("float32").toarray()

    print(f"✅ Vector shape: {vectors.shape}")

    if np.all(vectors == 0):
        raise ValueError("❌ All vectors are zero")

    # =========================================================
    # 🔥 NORMALIZATION
    # =========================================================
    print("📏 Normalizing vectors...")
    faiss.normalize_L2(vectors)

    # =========================================================
    # 🔥 FAISS INDEX
    # =========================================================
    print("⚡ Building FAISS index...")

    dim = vectors.shape[1]

    try:
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
    except Exception as e:
        raise RuntimeError(f"❌ FAISS failed: {e}")

    print(f"✅ Index trained with {index.ntotal} vectors")

    # =========================================================
    # 🔥 SAVE MODELS
    # =========================================================
    print("💾 Saving models...")

    try:
        faiss.write_index(index, index_path)

        with open(movies_path, "wb") as f:
            pickle.dump(df, f)

        with open(tfidf_path, "wb") as f:
            pickle.dump(tfidf, f)

        np.save(vectors_path, vectors)

    except Exception as e:
        raise RuntimeError(f"❌ Saving failed: {e}")

    print("🎉 Model training completed successfully!")


# =========================================================
# 🔥 MAIN ENTRY
# =========================================================
if __name__ == "__main__":
    train_model()