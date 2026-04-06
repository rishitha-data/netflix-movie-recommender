import os
from dotenv import load_dotenv

# =========================================================
# 🔥 LOAD ENV
# =========================================================
load_dotenv()


# =========================================================
# 🔥 HELPERS (SAFE PARSING)
# =========================================================
def get_env(key, default=None, cast=str, required=False):
    try:
        value = os.getenv(key, default)

        if required and value is None:
            raise ValueError(f"Missing env variable: {key}")

        return cast(value) if value is not None else default

    except Exception:
        return default   # ✅ SAFE fallback


# =========================================================
# 🔥 BASE PATHS (FIXED)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


# =========================================================
# 🔥 DATA PATHS
# =========================================================
DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")

TMDB_DATA_PATH = os.path.join(DATA_DIR, "tmdb_5000_movies.csv")
MOVIELENS_MOVIES_PATH = os.path.join(RAW_DATA_DIR, "movies.csv")
MOVIELENS_RATINGS_PATH = os.path.join(RAW_DATA_DIR, "ratings.csv")


# =========================================================
# 🔥 MODEL PATHS (FIXED GLOBAL LOCATION)
# =========================================================
MODEL_DIR = os.path.join(ROOT_DIR, "models")   # ✅ FIXED
os.makedirs(MODEL_DIR, exist_ok=True)

FAISS_INDEX_PATH = os.path.join(MODEL_DIR, "faiss.index")
MOVIES_PKL_PATH = os.path.join(MODEL_DIR, "movies.pkl")
TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf.pkl")
VECTORS_PATH = os.path.join(MODEL_DIR, "vectors.npy")

# collaborative
COLLAB_USER_ITEM_PATH = os.path.join(MODEL_DIR, "user_item.pkl")
COLLAB_LATENT_PATH = os.path.join(MODEL_DIR, "latent_matrix.pkl")


# =========================================================
# 🔥 API CONFIG
# =========================================================
API_HOST = get_env("API_HOST", "127.0.0.1")
API_PORT = get_env("API_PORT", 8000, int)


# =========================================================
# 🔥 RECOMMENDATION CONFIG
# =========================================================
TOP_K = get_env("TOP_K", 5, int)

HYBRID_ALPHA = get_env("HYBRID_ALPHA", 0.8, float)
SEARCH_MULTIPLIER = get_env("SEARCH_MULTIPLIER", 10, int)


# =========================================================
# 🔥 TRAINING CONFIG
# =========================================================
TFIDF_MAX_FEATURES = get_env("TFIDF_MAX_FEATURES", 8000, int)   # ✅ reduced
TFIDF_MIN_DF = get_env("TFIDF_MIN_DF", 2, int)
TFIDF_MAX_DF = get_env("TFIDF_MAX_DF", 0.85, float)
TFIDF_NGRAM_RANGE = (1, 2)


# =========================================================
# 🔥 EVALUATION CONFIG
# =========================================================
EVAL_NUM_USERS = get_env("EVAL_NUM_USERS", 200, int)
EVAL_TOP_K = get_env("EVAL_TOP_K", 5, int)


# =========================================================
# 🔥 ENVIRONMENT
# =========================================================
ENV = get_env("ENV", "dev")
DEBUG = ENV == "dev"


# =========================================================
# 🔥 LOGGING
# =========================================================
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")


# =========================================================
# 🔥 VALIDATION (SAFE VERSION - NO CRASH)
# =========================================================
def validate_paths(strict=False):   # ✅ default SAFE

    required_files = [
        MOVIES_PKL_PATH,
        FAISS_INDEX_PATH,
        VECTORS_PATH,
    ]

    missing = [f for f in required_files if not os.path.exists(f)]

    if missing:
        msg = "\n⚠️ Missing model files:\n" + "\n".join(f"   - {f}" for f in missing)
        msg += "\n\n👉 Run training first:\npython -m backend.src.content_model\n"

        print(msg)

        if strict:
            raise FileNotFoundError(msg)


# =========================================================
# 🔥 DEBUG PRINT
# =========================================================
def print_config():
    print("\n🔧 CONFIGURATION")
    print(f"ENV: {ENV}")
    print(f"API: {API_HOST}:{API_PORT}")
    print(f"TOP_K: {TOP_K}")
    print(f"HYBRID_ALPHA: {HYBRID_ALPHA}")
    print(f"MODEL_DIR: {MODEL_DIR}")