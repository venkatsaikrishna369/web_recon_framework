# modules/geo_lookup.py
import requests
import socket
from utils.logger import get_logger
import config

logger = get_logger()

def get_geolocation(domain):
    """
    Use ip-api.com (free, no API key) to get geolocation for the resolved IP.
    If unavailable, fallback to 'Geolocation unavailable'.
    """
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,as,isp",
                                timeout=config.HTTP_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "N/A"),
                    "region": data.get("regionName", "N/A"),
                    "city": data.get("city", "N/A"),
                    "asn": data.get("as", "N/A"),
                    "isp": data.get("isp", "N/A")
                }
            else:
                logger.warning(f"Geolocation API error: {data.get('message', 'Unknown')}")
        else:
            logger.warning(f"Geolocation API returned status {response.status_code}")
    except Exception as e:
        logger.warning(f"Geolocation unavailable: {e}")
    return {"error": "Geolocation unavailable"}