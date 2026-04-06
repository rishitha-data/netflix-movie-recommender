import pandas as pd
import os
import ast
import re


# =========================================================
# 🔥 CLEAN TEXT
# =========================================================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# =========================================================
# 🔥 SAFE PARSE
# =========================================================
def safe_eval(text):
    if isinstance(text, list):
        return text
    if pd.isna(text):
        return []
    try:
        return ast.literal_eval(text)
    except:
        return []


# =========================================================
# 🔥 EXTRACTORS
# =========================================================
def extract_names(lst, key="name", limit=None):
    if not isinstance(lst, list):
        return []
    if limit:
        lst = lst[:limit]
    return [i.get(key, "") for i in lst if isinstance(i, dict)]


def extract_director(lst):
    if not isinstance(lst, list):
        return []
    for i in lst:
        if isinstance(i, dict) and i.get("job") == "Director":
            return [i.get("name", "")]
    return []


def clean_list(lst):
    return [i.replace(" ", "").lower() for i in lst if isinstance(i, str)]


# =========================================================
# 🔥 WEIGHTING HELPER
# =========================================================
def repeat(lst, times):
    return (" ".join(lst) + " ") * times if lst else ""


# =========================================================
# 🔥 LOAD DATA (SAFE VERSION)
# =========================================================
def load_data():

    print("🚀 Loading data...")

    # safer root path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

    movies_path = os.path.join(ROOT_DIR, "data", "tmdb_5000_movies.csv")
    credits_path = os.path.join(ROOT_DIR, "data", "tmdb_5000_credits.csv")

    print("Movies path:", movies_path)
    print("Credits path:", credits_path)

    # =========================================================
    # 🔥 FILE CHECK
    # =========================================================
    if not os.path.exists(movies_path):
        raise FileNotFoundError(f"❌ Movies file not found: {movies_path}")

    if not os.path.exists(credits_path):
        raise FileNotFoundError(f"❌ Credits file not found: {credits_path}")

    # =========================================================
    # 🔥 LOAD DATA
    # =========================================================
    try:
        movies = pd.read_csv(movies_path)
        credits = pd.read_csv(credits_path)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load CSV files: {e}")

    # =========================================================
    # 🔥 VALIDATE COLUMNS
    # =========================================================
    required_cols_movies = {'title', 'overview', 'genres', 'keywords'}
    required_cols_credits = {'title', 'cast', 'crew'}

    if not required_cols_movies.issubset(movies.columns):
        raise ValueError("❌ Movies dataset missing required columns")

    if not required_cols_credits.issubset(credits.columns):
        raise ValueError("❌ Credits dataset missing required columns")

    # =========================================================
    # 🔥 MERGE DATA
    # =========================================================
    df = movies.merge(credits, on="title")

    if df.empty:
        raise ValueError("❌ Merge failed — dataset is empty")

    # =========================================================
    # 🔥 KEEP REQUIRED COLUMNS
    # =========================================================
    df = df[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    df = df.rename(columns={"id": "movie_id"})

    df = df.dropna(subset=['title'])

    # =========================================================
    # 🔥 PARSE JSON
    # =========================================================
    df['genres'] = df['genres'].apply(lambda x: extract_names(safe_eval(x)))
    df['keywords'] = df['keywords'].apply(lambda x: extract_names(safe_eval(x)))
    df['cast'] = df['cast'].apply(lambda x: extract_names(safe_eval(x), limit=5))
    df['crew'] = df['crew'].apply(lambda x: extract_director(safe_eval(x)))

    for col in ['genres', 'keywords', 'cast', 'crew']:
        df[col] = df[col].apply(clean_list)

    # =========================================================
    # 🔥 FEATURE ENGINEERING
    # =========================================================
    df['tags'] = ""

    df['tags'] += df['genres'].apply(lambda x: repeat(x, 5))
    df['tags'] += df['keywords'].apply(lambda x: repeat(x, 3))
    df['tags'] += df['cast'].apply(lambda x: " ".join(x) + " ")
    df['tags'] += df['crew'].apply(lambda x: repeat(x, 3))
    df['tags'] += df['overview'].fillna("") + " "
    df['tags'] += df['title'] + " "

    # clean text
    df['tags'] = df['tags'].apply(clean_text)

    # convert genres list → string
    df['genres'] = df['genres'].apply(lambda x: " ".join(x))

    # remove duplicates
    df = df.drop_duplicates(subset="title").reset_index(drop=True)

    if df.empty:
        raise ValueError("❌ No data after preprocessing")

    print(f"✅ Data loaded successfully: {len(df)} movies")

    return df[['movie_id', 'title', 'genres', 'tags']]