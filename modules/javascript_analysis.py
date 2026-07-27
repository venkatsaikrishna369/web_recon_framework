# modules/javascript_analysis.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.logger import get_logger
import config

logger = get_logger()

def get_javascript_analysis(domain):
    """
    JavaScript analysis.
    Extracts: Endpoints, API URLs, Secrets, Tokens, JWT,
    Firebase URLs, S3 Buckets, GitHub Links, Comments, Hidden URLs.
    """
    url = f"https://{domain}"
    result = {
        'endpoints': [],
        'api_urls': [],
        'secrets': [],
        'tokens': [],
        'jwt': [],
        'firebase_urls': [],
        's3_buckets': [],
        'github_links': [],
        'comments': [],
        'hidden_urls': [],
    }
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": config.USER_AGENT})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all script tags
        scripts = soup.find_all('script')
        js_content = ''
        for script in scripts:
            if script.string:
                js_content += script.string
                
        # Load external JS files
        for script in scripts:
            if script.get('src'):
                try:
                    js_url = urljoin(url, script['src'])
                    js_response = requests.get(js_url, timeout=5)
                    if js_response.status_code == 200:
                        js_content += js_response.text
                except:
                    pass
                    
        # Extract API endpoints
        api_patterns = [
            r'/api/[a-zA-Z0-9\-_/]+',
            r'/v[0-9]/[a-zA-Z0-9\-_/]+',
            r'/rest/[a-zA-Z0-9\-_/]+',
            r'/graphql',
        ]
        for pattern in api_patterns:
            matches = re.findall(pattern, js_content)
            result['api_urls'].extend(matches)
            
        # Extract JWT tokens
        jwt_pattern = r'eyJ[a-zA-Z0-9\-_=]+\.[a-zA-Z0-9\-_=]+\.?[a-zA-Z0-9\-_=]*'
        result['jwt'] = re.findall(jwt_pattern, js_content)
        
        # Extract secrets (high entropy strings)
        secret_pattern = r'[a-zA-Z0-9]{32,}'
        secrets = re.findall(secret_pattern, js_content)
        result['secrets'] = [s for s in secrets if len(s) >= 32][:10]
        
        # Extract Firebase URLs
        firebase_pattern = r'[a-zA-Z0-9\-]+\.firebaseio\.com'
        result['firebase_urls'] = re.findall(firebase_pattern, js_content)
        
        # Extract S3 buckets
        s3_pattern = r'[a-zA-Z0-9\-]+\.s3\.amazonaws\.com'
        result['s3_buckets'] = re.findall(s3_pattern, js_content)
        
        # Extract GitHub links
        github_pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+'
        result['github_links'] = re.findall(github_pattern, js_content)
        
        # Extract comments
        comment_pattern = r'//.*$|/\*.*?\*/'
        comments = re.findall(comment_pattern, js_content, re.DOTALL | re.MULTILINE)
        result['comments'] = comments[:20]  # Limit to 20
        
        # Extract hidden URLs
        url_pattern = r'https?://[a-zA-Z0-9\-_.]+/[a-zA-Z0-9\-_/]+'
        all_urls = re.findall(url_pattern, js_content)
        result['hidden_urls'] = list(set(all_urls))[:20]
        
        # Extract endpoints from comments
        if result['comments']:
            for comment in result['comments']:
                endpoints = re.findall(r'/[a-zA-Z0-9\-_/]+', comment)
                result['endpoints'].extend(endpoints)
                
        # Deduplicate
        for key in result:
            result[key] = list(set(result[key]))[:20]  # Limit to 20 each
            
    except Exception as e:
        logger.error(f"JavaScript analysis failed: {e}")
        result['error'] = str(e)
        
    return result