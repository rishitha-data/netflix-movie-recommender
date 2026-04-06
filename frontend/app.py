# import streamlit as st
# import requests
# import os
# import sqlite3
# import re
# import urllib.parse
# from dotenv import load_dotenv

# # =========================================================
# # 🔥 ENV
# # =========================================================
# load_dotenv()
# API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
# TMDB_KEY = os.getenv("TMDB_KEY")

# # =========================================================
# # 🔥 PAGE CONFIG
# # =========================================================
# st.set_page_config(page_title="Netflix Recommender", layout="wide")

# # =========================================================
# # 🔥 STYLE
# # =========================================================
# st.markdown("""
# <style>
# body {background-color:#141414; color:white;}
# img {border-radius:10px; transition:0.3s;}
# img:hover {transform: scale(1.08);}
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # 🔥 SESSION
# # =========================================================
# if "selected_movie" not in st.session_state:
#     st.session_state.selected_movie = None

# # =========================================================
# # 🔥 HELPERS
# # =========================================================
# def clean_title(title):
#     return re.sub(r"\(\d{4}\)", "", str(title)).strip()

# def fetch_api(url):
#     try:
#         res = requests.get(url, timeout=5)
#         if res.status_code == 200:
#             return res.json()
#     except:
#         return None

# @st.cache_data
# def get_details(title):
#     if not TMDB_KEY:
#         return None
#     try:
#         res = requests.get(
#             "https://api.themoviedb.org/3/search/movie",
#             params={"api_key": TMDB_KEY, "query": clean_title(title)},
#             timeout=5
#         ).json()
#         if res.get("results"):
#             return res["results"][0]
#     except:
#         return None
#     return None

# # =========================================================
# # 🔥 MOVIE CARD (CLICKABLE)
# # =========================================================
# def movie_card(title, key):
#     details = get_details(title)

#     poster = "https://via.placeholder.com/300x450?text=No+Image"
#     rating = ""
#     year = ""

#     if details:
#         if details.get("poster_path"):
#             poster = f"https://image.tmdb.org/t/p/w500{details['poster_path']}"
#         rating = details.get("vote_average", "")
#         year = details.get("release_date", "")[:4]

#     st.image(poster, width=180)

#     # 🔥 CLICK BUTTON BELOW IMAGE
#     if st.button(f"🎬 {title}", key=key):
#         st.session_state.selected_movie = title
#         st.rerun()

#     if rating:
#         st.caption(f"⭐ {rating} | {year}")

# # =========================================================
# # 🔥 ROW
# # =========================================================
# def show_row(title, movies):
#     st.markdown(f"## {title}")

#     if not movies:
#         st.warning("No movies found")
#         return

#     cols = st.columns(6)

#     for i, m in enumerate(movies[:6]):
#         with cols[i]:
#             if isinstance(m, dict):
#                 movie_card(m["title"], f"{title}_{i}")
#             else:
#                 movie_card(m, f"{title}_{i}")

# # =========================================================
# # 🔥 HEADER
# # =========================================================
# st.title("🎬 Netflix Recommender")

# # =========================================================
# # 🔥 SEARCH
# # =========================================================
# query = st.text_input("🔍 Search movie")

# if query:
#     res = fetch_api(f"{API_URL}/search?query={query}&n=10")

#     if res and res.get("results"):
#         movie = st.selectbox("Select movie", res["results"])

#         if st.button("🎯 Recommend"):
#             st.session_state.selected_movie = movie
#             st.rerun()
#     else:
#         st.warning("No results found")

# # =========================================================
# # 🔥 TRENDING
# # =========================================================
# trend = fetch_api(f"{API_URL}/trending?n=12")
# if trend:
#     show_row("🔥 Trending Now", trend["movies"])

# # =========================================================
# # 🔥 POPULAR
# # =========================================================
# pop = fetch_api(f"{API_URL}/movies?n=12")
# if pop:
#     show_row("⭐ Popular Movies", pop["movies"])

# # =========================================================
# # 🔥 DETAIL VIEW
# # =========================================================
# if st.session_state.selected_movie:

#     movie = st.session_state.selected_movie
#     details = get_details(movie)

#     st.markdown("---")

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         if details and details.get("poster_path"):
#             st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
#         else:
#             st.image("https://via.placeholder.com/300x450")

#     with col2:
#         st.markdown(f"## 🎬 {movie}")

#         if details:
#             st.write(f"⭐ Rating: {details.get('vote_average', 'N/A')}")
#             st.write(f"📅 Year: {details.get('release_date', 'N/A')}")
#             st.write(details.get("overview", "No description available"))

#     # 🔥 FIX: URL ENCODE
#     encoded_movie = urllib.parse.quote(movie)

#     rec = fetch_api(
#         f"{API_URL}/hybrid?user_id=1&movie={encoded_movie}&n=12"
#     )

#     if rec and rec.get("recommendations"):
#         show_row("🎯 Because you watched this", rec["recommendations"])
#     else:
#         st.warning("No recommendations found")

#     if st.button("❌ Close"):
#         st.session_state.selected_movie = None
#         st.rerun()

# import streamlit as st
# import requests
# import os
# import re
# import urllib.parse
# from dotenv import load_dotenv

# # =========================================================
# # 🔥 ENV
# # =========================================================
# load_dotenv()
# API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
# TMDB_KEY = os.getenv("TMDB_KEY")

# # =========================================================
# # 🔥 PAGE CONFIG
# # =========================================================
# st.set_page_config(page_title="Netflix Recommender", layout="wide")

# # =========================================================
# # 🔥 STYLE
# # =========================================================
# st.markdown("""
# <style>
# body {background-color:#141414; color:white;}
# img {border-radius:10px; transition:0.3s; cursor:pointer;}
# img:hover {transform: scale(1.08);}
# .scroll-container {
#     display: flex;
#     overflow-x: auto;
#     gap: 20px;
# }
# .scroll-item {
#     min-width: 180px;
# }
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # 🔥 SESSION
# # =========================================================
# if "selected_movie" not in st.session_state:
#     st.session_state.selected_movie = None

# if "user_id" not in st.session_state:
#     st.session_state.user_id = 1

# # =========================================================
# # 🔥 HELPERS
# # =========================================================
# def clean_title(title):
#     return re.sub(r"\(\d{4}\)", "", str(title)).strip()

# def fetch_api(url):
#     try:
#         res = requests.get(url, timeout=5)
#         if res.status_code == 200:
#             return res.json()
#     except:
#         return None

# @st.cache_data
# def get_details(title):
#     if not TMDB_KEY:
#         return None
#     try:
#         res = requests.get(
#             "https://api.themoviedb.org/3/search/movie",
#             params={"api_key": TMDB_KEY, "query": clean_title(title)},
#             timeout=5
#         ).json()
#         if res.get("results"):
#             return res["results"][0]
#     except:
#         return None
#     return None

# # =========================================================
# # 🔥 MOVIE CARD (PURE CLICK)
# # =========================================================
# def movie_card(title, key):
#     details = get_details(title)

#     poster = "https://via.placeholder.com/300x450?text=No+Image"
#     rating = ""
#     year = ""

#     if details:
#         if details.get("poster_path"):
#             poster = f"https://image.tmdb.org/t/p/w500{details['poster_path']}"
#         rating = details.get("vote_average", "")
#         year = details.get("release_date", "")[:4]

#     st.markdown('<div class="scroll-item">', unsafe_allow_html=True)

#     st.image(poster, width=180)

#     # 🔥 INVISIBLE CLICK BUTTON
#     if st.button("", key=key):
#         st.session_state.selected_movie = title
#         st.rerun()

#     st.caption(title)

#     if rating:
#         st.caption(f"⭐ {rating} | {year}")
#         st.caption("Because you watched similar content")

#     st.markdown('</div>', unsafe_allow_html=True)

# # =========================================================
# # 🔥 ROW (HORIZONTAL SCROLL)
# # =========================================================
# def show_row(title, movies):
#     st.markdown(f"## {title}")

#     if not movies:
#         st.warning("No movies found")
#         return

#     st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

#     cols = st.columns(len(movies[:10]))

#     for i, m in enumerate(movies[:10]):
#         with cols[i]:
#             if isinstance(m, dict):
#                 movie_card(m["title"], f"{title}_{i}")
#             else:
#                 movie_card(m, f"{title}_{i}")

#     st.markdown('</div>', unsafe_allow_html=True)

# # =========================================================
# # 🔥 HEADER
# # =========================================================
# st.title("🎬 Netflix Recommender")

# # =========================================================
# # 🔥 SEARCH
# # =========================================================
# query = st.text_input("🔍 Search movie")

# if query:
#     res = fetch_api(f"{API_URL}/search?query={query}&n=10")

#     if res and res.get("results"):
#         movie = st.selectbox("Select movie", res["results"])

#         if st.button("🎯 Recommend"):
#             st.session_state.selected_movie = movie
#             st.rerun()
#     else:
#         st.warning("No results found")

# # =========================================================
# # 🔥 TRENDING
# # =========================================================
# trend = fetch_api(f"{API_URL}/trending?n=12")
# if trend:
#     show_row("🔥 Trending Now", trend["movies"])

# # =========================================================
# # 🔥 POPULAR
# # =========================================================
# pop = fetch_api(f"{API_URL}/movies?n=12")
# if pop:
#     show_row("⭐ Popular Movies", pop["movies"])

# # =========================================================
# # 🔥 DETAIL VIEW
# # =========================================================
# if st.session_state.selected_movie:

#     placeholder = st.empty()

#     with placeholder.container():
#         st.write("🎬 Loading recommendations...")

#     movie = st.session_state.selected_movie
#     details = get_details(movie)

#     st.markdown("---")

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         if details and details.get("poster_path"):
#             st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
#         else:
#             st.image("https://via.placeholder.com/300x450")

#     with col2:
#         st.markdown(f"## 🎬 {movie}")

#         if details:
#             st.write(f"⭐ Rating: {details.get('vote_average', 'N/A')}")
#             st.write(f"📅 Year: {details.get('release_date', 'N/A')}")
#             st.write(details.get("overview", "No description available"))

#     encoded_movie = urllib.parse.quote(movie)

#     rec = fetch_api(
#         f"{API_URL}/hybrid?user_id={st.session_state.user_id}&movie={encoded_movie}&n=12"
#     )

#     placeholder.empty()

#     if rec and rec.get("recommendations"):
#         show_row("🎯 Because you watched this", rec["recommendations"])
#     else:
#         st.warning("No recommendations found")

#     if st.button("❌ Close"):
#         st.session_state.selected_movie = None
#         st.rerun()
import streamlit as st
import requests
import os
import re
import urllib.parse
from dotenv import load_dotenv

# =========================================================
# 🔥 ENV
# =========================================================
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
TMDB_KEY = os.getenv("TMDB_KEY")

# =========================================================
# 🔥 PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Netflix Recommender", layout="wide")

# =========================================================
# 🔥 STYLE
# =========================================================
st.markdown("""
<style>
body {background-color:#141414; color:white;}
img {border-radius:10px; transition:0.3s;}
img:hover {transform: scale(1.08);}

.scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 20px;
}
.scroll-item {
    min-width: 180px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🔥 SESSION
# =========================================================
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "user_id" not in st.session_state:
    st.session_state.user_id = 1

# =========================================================
# 🔥 HELPERS
# =========================================================
def clean_title(title):
    return re.sub(r"\(\d{4}\)", "", str(title)).strip()

def fetch_api(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json()
    except:
        return None

@st.cache_data
def get_details(title):
    if not TMDB_KEY:
        return None
    try:
        res = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_KEY, "query": clean_title(title)},
            timeout=5
        ).json()
        if res.get("results"):
            return res["results"][0]
    except:
        return None
    return None

# =========================================================
# 🔥 MOVIE CARD (VISIBLE BUTTON FINAL)
# =========================================================
def movie_card(title, key):
    details = get_details(title)

    poster = "https://via.placeholder.com/300x450?text=No+Image"
    rating = ""
    year = ""

    if details:
        if details.get("poster_path"):
            poster = f"https://image.tmdb.org/t/p/w500{details['poster_path']}"
        rating = details.get("vote_average", "")
        year = details.get("release_date", "")[:4]

    st.markdown('<div class="scroll-item">', unsafe_allow_html=True)

    # 🎬 Poster
    st.image(poster, width=180)

    # ✅ VISIBLE BUTTON (FINAL FIX)
    if st.button(f"🎬 {title}", key=key):
        st.session_state.selected_movie = title
        st.rerun()

    # 🎯 Info
    if rating:
        st.caption(f"⭐ {rating} | {year}")
        st.caption("Because you watched similar content")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 🔥 ROW
# =========================================================
def show_row(title, movies):
    st.markdown(f"## {title}")

    if not movies:
        st.warning("No movies found")
        return

    cols = st.columns(len(movies[:10]))

    for i, m in enumerate(movies[:10]):
        with cols[i]:
            if isinstance(m, dict):
                movie_card(m["title"], f"{title}_{i}")
            else:
                movie_card(m, f"{title}_{i}")

# =========================================================
# 🔥 HEADER
# =========================================================
st.title("🎬 Netflix Recommender")

# =========================================================
# 🔥 SEARCH
# =========================================================
query = st.text_input("🔍 Search movie")

if query:
    res = fetch_api(f"{API_URL}/search?query={query}&n=10")

    if res and res.get("results"):
        movie = st.selectbox("Select movie", res["results"])

        if st.button("🎯 Recommend"):
            st.session_state.selected_movie = movie
            st.rerun()
    else:
        st.warning("No results found")

# =========================================================
# 🔥 TRENDING
# =========================================================
trend = fetch_api(f"{API_URL}/trending?n=12")
if trend:
    show_row("🔥 Trending Now", trend["movies"])

# =========================================================
# 🔥 POPULAR
# =========================================================
pop = fetch_api(f"{API_URL}/movies?n=12")
if pop:
    show_row("⭐ Popular Movies", pop["movies"])

# =========================================================
# 🔥 DETAIL VIEW
# =========================================================
if st.session_state.selected_movie:

    placeholder = st.empty()

    with placeholder.container():
        st.write("🎬 Loading recommendations...")

    movie = st.session_state.selected_movie
    details = get_details(movie)

    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        if details and details.get("poster_path"):
            st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
        else:
            st.image("https://via.placeholder.com/300x450")

    with col2:
        st.markdown(f"## 🎬 {movie}")

        if details:
            st.write(f"⭐ Rating: {details.get('vote_average', 'N/A')}")
            st.write(f"📅 Year: {details.get('release_date', 'N/A')}")
            st.write(details.get("overview", "No description available"))

    encoded_movie = urllib.parse.quote(movie)

    rec = fetch_api(
        f"{API_URL}/hybrid?user_id={st.session_state.user_id}&movie={encoded_movie}&n=12"
    )

    placeholder.empty()

    if rec and rec.get("recommendations"):
        show_row("🎯 Because you watched this", rec["recommendations"])
    else:
        st.warning("No recommendations found")

    if st.button("❌ Close"):
        st.session_state.selected_movie = None
        st.rerun()