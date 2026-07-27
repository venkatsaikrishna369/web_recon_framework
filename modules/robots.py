# modules/robots.py
import requests
import config
from utils.logger import get_logger

logger = get_logger()

def fetch_robots(url, timeout=config.HTTP_TIMEOUT):
    """
    Fetch robots.txt.
    Returns dict with status, content, last_modified.
    """
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": config.USER_AGENT})
        if resp.status_code == 200:
            content = resp.text
            last_modified = resp.headers.get("Last-Modified", "N/A")
            return {
                "status": resp.status_code,
                "content": content,
                "last_modified": last_modified
            }
        else:
            return {
                "status": resp.status_code,
                "content": "Not Found",
                "last_modified": "N/A"
            }
    except requests.exceptions.RequestException as e:
        logger.error(f"robots.txt fetch failed: {e}")
        return {"error": str(e)}