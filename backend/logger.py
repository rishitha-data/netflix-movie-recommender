import logging
import os
from logging.handlers import RotatingFileHandler
from backend.config import LOG_LEVEL as CONFIG_LOG_LEVEL

# =========================================================
# 🔥 LOG DIRECTORY
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# =========================================================
# 🔥 LOG LEVEL
# =========================================================
LOG_LEVEL = getattr(logging, CONFIG_LOG_LEVEL.upper(), logging.INFO)

# =========================================================
# 🔥 FORMAT
# =========================================================
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# =========================================================
# 🔥 MAIN LOGGER
# =========================================================
logger = logging.getLogger("movie-recommender")

# 🔥 Prevent reconfiguration on reload
if not logger.hasHandlers():
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    # =====================================================
    # 🔥 CONSOLE HANDLER
    # =====================================================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # =====================================================
    # 🔥 FILE HANDLER (SAFE UTF-8)
    # =====================================================
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"   # 🔥 FIXED
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# =========================================================
# 🔥 GET CHILD LOGGER
# =========================================================
def get_logger(name: str):
    return logging.getLogger(f"movie-recommender.{name}")

# =========================================================
# 🔥 REQUEST LOGGING
# =========================================================
def log_request(endpoint: str, params: dict):
    logger.info("Request -> %s | Params: %s", endpoint, params)

def log_response(endpoint: str, result_count: int):
    logger.info("Response <- %s | Results: %d", endpoint, result_count)

# =========================================================
# 🔥 ERROR LOGGING (IMPORTANT)
# =========================================================
def log_error(message: str, exc: Exception = None):
    if exc:
        logger.exception(f"{message} | Exception: {exc}")
    else:
        logger.error(message)