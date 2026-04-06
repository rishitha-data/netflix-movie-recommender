from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
import time
import sys

from backend.src.recommend import (
    content_recommend,
    search_movies,
    trending_movies,
    load_models
)
from backend.src.hybrid_model import hybrid_recommend

from backend.logger import get_logger, log_request, log_response, log_error
from backend.config import TOP_K

# =========================================================
# 🔥 LOGGER
# =========================================================
logger = get_logger(__name__)

# =========================================================
# 🔥 FIX WINDOWS ENCODING
# =========================================================
try:
    sys.stdout.reconfigure(encoding="utf-8")
except:
    pass

# =========================================================
# 🔥 INIT APP
# =========================================================
app = FastAPI(
    title="Movie Recommendation API",
    version="3.0",
    description="Industry-Level Hybrid Movie Recommendation System"
)

# =========================================================
# 🔥 GLOBAL ERROR HANDLER
# =========================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error("Unhandled exception", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# =========================================================
# 🔥 STARTUP (SAFE VERSION)
# =========================================================
@app.on_event("startup")
def startup_event():
    try:
        load_models()
        logger.info("✅ Models loaded successfully")
    except Exception as e:
        log_error("⚠️ Models not loaded", e)
        print("\n⚠️ Models not found. Run this first:\n")
        print("python -m backend.src.content_model\n")

# =========================================================
# 🔥 HEALTH CHECK
# =========================================================
@app.get("/", tags=["Health"])
def home():
    try:
        load_models()
        return {"status": "ok", "models": "loaded"}
    except:
        return {"status": "error", "models": "not loaded"}

# =========================================================
# 🔥 CONTENT-BASED
# =========================================================
@app.get("/recommend", tags=["Content-Based"])
def recommend(
    movie: str = Query(..., min_length=1),
    n: int = Query(TOP_K, ge=1, le=50)
):
    start = time.time()
    movie = movie.strip()

    log_request("/recommend", {"movie": movie, "n": n})

    results = content_recommend(movie, n)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found")

    log_response("/recommend", len(results))

    return {
        "type": "content",
        "input_movie": movie,
        "count": len(results),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "recommendations": results
    }

# =========================================================
# 🔥 HYBRID
# =========================================================
@app.get("/hybrid", tags=["Hybrid"])
def hybrid(
    user_id: int = Query(..., ge=1),
    movie: str = Query(..., min_length=1),
    n: int = Query(TOP_K, ge=1, le=50)
):
    start = time.time()
    movie = movie.strip()

    log_request("/hybrid", {"user_id": user_id, "movie": movie, "n": n})

    results = hybrid_recommend(user_id, movie, n)

    if not results:
        raise HTTPException(status_code=404, detail="No recommendations found")

    log_response("/hybrid", len(results))

    return {
        "type": "hybrid",
        "user_id": user_id,
        "input_movie": movie,
        "count": len(results),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "recommendations": results
    }

# =========================================================
# 🔥 SEARCH
# =========================================================
@app.get("/search", tags=["Search"])
def search(
    query: str = Query("", min_length=0),
    n: int = Query(10, ge=1, le=50)
):
    start = time.time()
    query = query.strip()

    log_request("/search", {"query": query, "n": n})

    results = search_movies(query, n)

    log_response("/search", len(results))

    return {
        "query": query,
        "count": len(results),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "results": results
    }

# =========================================================
# 🔥 TRENDING
# =========================================================
@app.get("/trending", tags=["Discovery"])
def trending(n: int = Query(10, ge=1, le=50)):
    start = time.time()

    log_request("/trending", {"n": n})

    results = trending_movies(n)

    log_response("/trending", len(results))

    return {
        "count": len(results),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "movies": results
    }

# =========================================================
# 🔥 MOVIES LIST
# =========================================================
@app.get("/movies", tags=["Catalog"])
def get_movies(n: int = Query(100, ge=1, le=500)):
    start = time.time()

    log_request("/movies", {"n": n})

    movies, _, _ = load_models()
    results = movies["title"].head(n).tolist()

    log_response("/movies", len(results))

    return {
        "count": len(results),
        "latency_ms": round((time.time() - start) * 1000, 2),
        "movies": results
    }