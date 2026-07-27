# modules/headers.py
import requests
import config
from utils.logger import get_logger

logger = get_logger()

def fetch_headers(url, timeout=config.HTTP_TIMEOUT):
    """
    Fetch HTTP response headers.
    Returns dict of all headers.
    """
    try:
        # Use HEAD to get headers only
        resp = requests.head(url, timeout=timeout, headers={"User-Agent": config.USER_AGENT}, allow_redirects=True)
        # Some servers may not respond to HEAD; fallback to GET if no content-length
        if resp.status_code >= 400:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": config.USER_AGENT}, stream=True)
            # We only need headers, close connection
            resp.close()
        # Convert headers to dict
        headers = dict(resp.headers)
        logger.info(f"Headers fetched from {url}")
        return headers
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch headers: {e}")
        return {"error": str(e)}