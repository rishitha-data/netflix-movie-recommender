import pickle
import pandas as pd

movies = pickle.load(open("models/movies.pkl", "rb"))

def load_similarity():
    return pickle.load(open("models/content_similarity.pkl", "rb"))

def content_recommend(movie: str, n: int = 5):

    similarity = load_similarity()

    movie = movie.lower()

    titles = movies["title"].str.lower()

    if movie not in titles.values:
        return fallback_movies(n)

    movie_index = movies[titles == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = [
        movies.iloc[i[0]].title for i in movie_list
    ]

    return recommendations


def fallback_movies(n: int = 5):
    return movies["title"].sample(n).tolist()


def search_movies(query: str, n: int = 10):

    results = movies[
        movies["title"].str.contains(query, case=False, na=False)
    ]

    return results["title"].head(n).tolist()


def trending_movies(n: int = 10):
    return movies["title"].sample(n).tolist()