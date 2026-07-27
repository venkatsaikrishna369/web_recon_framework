# modules/sitemap.py
import requests
import xml.etree.ElementTree as ET
from utils.logger import get_logger
import config

logger = get_logger()

def fetch_sitemap(domain):
    """Fetch sitemap.xml - accepts domain not URL"""
    url = f"https://{domain}/sitemap.xml"
    result = {
        'url_count': 0,
        'first_urls': [],
        'error': None
    }
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": config.USER_AGENT})
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                urls = root.findall('.//ns:loc', namespace)
                
                if not urls:
                    urls = root.findall('.//loc')
                    
                result['url_count'] = len(urls)
                result['first_urls'] = [u.text for u in urls[:10] if u.text]
                
            except ET.ParseError:
                result['error'] = 'Invalid XML'
        else:
            result['error'] = f'Status {response.status_code}'
            
    except Exception as e:
        logger.error(f"Sitemap fetch failed: {e}")
        result['error'] = str(e)
        
    return result