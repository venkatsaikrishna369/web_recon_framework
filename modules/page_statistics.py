# modules/page_statistics.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from utils.logger import get_logger
import config

logger = get_logger()

def get_page_statistics(domain):
    """
    Page statistics like urlscan.
    Counts: Total Requests, HTTPS %, HTTP %, Redirects,
    JS Files, CSS Files, Images, Fonts, XHR, Transfer Size,
    Cookies, Domains, Subdomains, Countries, IPs.
    """
    url = f"https://{domain}"
    result = {}
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": config.USER_AGENT})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Basic stats
        result['status_code'] = response.status_code
        result['content_length'] = len(html)
        result['transfer_size'] = len(response.content)
        
        # Count elements
        result['js_files'] = len(soup.find_all('script', src=True))
        result['css_files'] = len(soup.find_all('link', rel='stylesheet'))
        result['images'] = len(soup.find_all('img'))
        result['fonts'] = len([link for link in soup.find_all('link') if 'font' in str(link).lower()])
        result['xhr'] = len([script for script in soup.find_all('script') if 'fetch' in str(script) or 'XMLHttpRequest' in str(script)])
        
        # Redirects
        result['redirects'] = len(response.history)
        
        # Links
        links = soup.find_all('a', href=True)
        domains = set()
        subdomains = set()
        
        for link in links:
            href = link['href']
            if href.startswith('http'):
                parsed = urlparse(href)
                if parsed.netloc:
                    domains.add(parsed.netloc)
                    parts = parsed.netloc.split('.')
                    if len(parts) >= 3:
                        subdomains.add('.'.join(parts[:-2]))
                        
        result['domains'] = len(domains)
        result['subdomains'] = len(subdomains)
        
        # HTTPS vs HTTP
        https_count = sum(1 for link in links if link.get('href', '').startswith('https'))
        http_count = sum(1 for link in links if link.get('href', '').startswith('http'))
        total = https_count + http_count
        result['https_percent'] = round((https_count / total * 100) if total > 0 else 0)
        result['http_percent'] = round((http_count / total * 100) if total > 0 else 0)
        
        # Cookies
        result['cookies'] = len(response.cookies)
        
        # Countries (from domains - simplified)
        result['countries'] = 'Multiple' if len(domains) > 1 else 'Unknown'
        
        # IPs (from DNS)
        try:
            import socket
            ips = set()
            for domain in list(domains)[:5]:  # Limit to 5 domains
                try:
                    ip = socket.gethostbyname(domain)
                    ips.add(ip)
                except:
                    pass
            result['ips'] = len(ips)
        except:
            result['ips'] = 0
            
    except Exception as e:
        logger.error(f"Page statistics failed: {e}")
        result['error'] = str(e)
        
    return result