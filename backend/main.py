# from fastapi import FastAPI, HTTPException
# import pandas as pd
# import os
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# app = FastAPI()

# movies = None
# similarity = None

# # -------- BASE DIRECTORY --------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# # -------- LOAD DATA --------
# @app.on_event("startup")
# def load_models():
#     global movies, similarity

#     movies_path = os.path.join(BASE_DIR, "data", "movies.csv")

#     movies = pd.read_csv(movies_path)

#     movies["cast"] = movies.get("cast", "")
#     movies["crew"] = movies.get("crew", "")

#     movies["tags"] = (
#         movies["cast"].fillna("").astype(str) +
#         " " +
#         movies["crew"].fillna("").astype(str)
#     )

#     cv = CountVectorizer(max_features=5000, stop_words="english")

#     vectors = cv.fit_transform(movies["tags"])

#     similarity = cosine_similarity(vectors)


# # -------- HOME --------
# @app.get("/")
# def home():
#     return {"message": "Movie Recommendation API running"}


# # -------- RECOMMEND --------
# @app.get("/recommend/{movie}")
# def recommend(movie: str, n: int = 5):

#     titles = movies["title"].str.lower()

#     if movie.lower() not in titles.values:
#         raise HTTPException(status_code=404, detail="Movie not found")

#     movie_index = movies[titles == movie.lower()].index[0]

#     distances = similarity[movie_index]

#     movie_list = sorted(
#         list(enumerate(distances)),
#         key=lambda x: x[1],
#         reverse=True
#     )[1:n+1]

#     rec_movies = [movies.iloc[i[0]].title for i in movie_list]

#     return {"recommendations": rec_movies}


# # -------- SEARCH --------
# @app.get("/search/{query}")
# def search(query: str):

#     results = movies[
#         movies["title"].str.contains(query, case=False, na=False)
#     ]

#     return {"results": results["title"].head(10).tolist()}


# # -------- TRENDING --------
# @app.get("/trending")
# def trending():
#     return {"movies": movies["title"].sample(10).tolist()}
from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import os

app = FastAPI()

# -------- BASE DIRECTORY --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------- LOAD MODELS --------
movies_path = os.path.join(BASE_DIR, "models", "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "models", "content_similarity.pkl")

movies = pickle.load(open(movies_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))


# -------- HOME --------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API running"}


# -------- RECOMMEND --------
@app.get("/recommend/{movie}")
def recommend(movie: str, n: int = 5):

    titles = movies["title"].str.lower()

    if movie.lower() not in titles.values:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = movies[titles == movie.lower()].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    rec_movies = [movies.iloc[i[0]].title for i in movie_list]

    return {"recommendations": rec_movies}


# -------- SEARCH --------
@app.get("/search/{query}")
def search(query: str):

    results = movies[
        movies["title"].str.contains(query, case=False, na=False)
    ]

    return {"results": results["title"].head(10).tolist()}


# -------- TRENDING --------
@app.get("/trending")
def trending():
    return {"movies": movies["title"].sample(10).tolist()}