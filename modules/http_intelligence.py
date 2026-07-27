# modules/http_intelligence.py
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from utils.logger import get_logger
import config

logger = get_logger()

def get_http_intelligence(domain):
    """
    Comprehensive HTTP intelligence.
    Collects: HTTP Version, Response Code, Redirect Chain,
    Compression, Cookies, Headers, Security Headers,
    Server Banner, Powered By, Cache, Encoding, Technologies,
    Frameworks, CDN, HTTP Methods.
    """
    result = {}
    url = f"https://{domain}"
    
    try:
        # Initial request to get complete data
        response = requests.get(url, timeout=10, allow_redirects=True, 
                              headers={"User-Agent": config.USER_AGENT})
        
        result['http_version'] = response.raw.version
        result['status_code'] = response.status_code
        result['redirect_chain'] = [r.url for r in response.history]
        result['final_url'] = response.url
        
        # Headers
        result['headers'] = dict(response.headers)
        
        # Security Headers Analysis
        result['security_headers'] = analyze_security_headers(response.headers)
        
        # Server Banner
        result['server_banner'] = response.headers.get('Server', 'Unknown')
        
        # Powered By
        result['powered_by'] = response.headers.get('X-Powered-By', 'Unknown')
        
        # Compression
        result['compression'] = response.headers.get('Content-Encoding', 'None')
        
        # Cache
        result['cache'] = {
            'cache_control': response.headers.get('Cache-Control', 'None'),
            'expires': response.headers.get('Expires', 'None'),
            'age': response.headers.get('Age', 'None'),
        }
        
        # Cookies
        result['cookies'] = {cookie.name: cookie.value for cookie in response.cookies}
        result['cookie_flags'] = [cookie.has_nonstandard_attr('secure') for cookie in response.cookies]
        
        # Content Type
        result['content_type'] = response.headers.get('Content-Type', 'Unknown')
        result['content_length'] = response.headers.get('Content-Length', len(response.text))
        
        # Detect Technologies
        result['technologies'] = detect_technologies(response.text, response.headers)
        
        # Detect Framework
        result['frameworks'] = detect_frameworks(response.text, response.headers)
        
        # Detect CDN
        result['cdn'] = detect_cdn(response.headers)
        
        # HTTP Methods (OPTIONS request)
        try:
            options_response = requests.options(url, timeout=5)
            result['http_methods'] = options_response.headers.get('Allow', 'Not specified')
        except:
            result['http_methods'] = 'Unknown'
            
    except Exception as e:
        logger.error(f"HTTP intelligence failed: {e}")
        result['error'] = str(e)
        
    return result

def analyze_security_headers(headers):
    """Analyze security headers"""
    security_headers = [
        'Content-Security-Policy', 'Strict-Transport-Security',
        'X-Frame-Options', 'X-Content-Type-Options',
        'Referrer-Policy', 'Permissions-Policy',
        'Cross-Origin-Opener-Policy', 'Cross-Origin-Embedder-Policy',
        'Cross-Origin-Resource-Policy'
    ]
    result = {}
    for header in security_headers:
        result[header] = headers.get(header, None)
    return result

def detect_technologies(html, headers):
    """Detect technologies from HTML and headers"""
    technologies = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for common technologies
    if 'cloudflare' in headers.get('Server', '').lower():
        technologies.append('Cloudflare')
        
    if 'react' in str(soup).lower() and 'react' in html:
        technologies.append('React')
        
    if 'angular' in str(soup).lower():
        technologies.append('Angular')
        
    if 'vue' in str(soup).lower():
        technologies.append('Vue.js')
        
    if 'bootstrap' in str(soup).lower():
        technologies.append('Bootstrap')
        
    if 'jquery' in str(soup).lower():
        technologies.append('jQuery')
        
    if 'wordpress' in str(soup).lower():
        technologies.append('WordPress')
        
    if 'drupal' in str(soup).lower():
        technologies.append('Drupal')
        
    if 'laravel' in str(soup).lower():
        technologies.append('Laravel')
        
    if 'django' in str(soup).lower():
        technologies.append('Django')
        
    if 'node' in str(soup).lower():
        technologies.append('Node.js')
        
    if 'php' in str(soup).lower() or '.php' in str(soup):
        technologies.append('PHP')
        
    if 'aspx' in str(soup).lower() or '.aspx' in str(soup):
        technologies.append('ASP.NET')
        
    return technologies

def detect_frameworks(html, headers):
    """Detect web frameworks"""
    frameworks = []
    soup = BeautifulSoup(html, 'html.parser')
    
    if 'wp-content' in str(soup).lower() or 'wp-includes' in str(soup).lower():
        frameworks.append('WordPress')
        
    if 'drupal' in str(soup).lower():
        frameworks.append('Drupal')
        
    if 'laravel' in str(soup).lower():
        frameworks.append('Laravel')
        
    if 'django' in str(soup).lower():
        frameworks.append('Django')
        
    if 'rails' in str(soup).lower():
        frameworks.append('Ruby on Rails')
        
    if 'spring' in str(soup).lower():
        frameworks.append('Spring')
        
    return frameworks

def detect_cdn(headers):
    """Detect CDN from headers"""
    if 'cloudflare' in headers.get('Server', '').lower():
        return 'Cloudflare'
    if 'Fastly' in headers.get('Server', ''):
        return 'Fastly'
    if 'Akamai' in headers.get('Server', ''):
        return 'Akamai'
    if 'CloudFront' in headers.get('Server', '') or 'cloudfront' in headers.get('X-Cache', '').lower():
        return 'AWS CloudFront'
    return 'None'