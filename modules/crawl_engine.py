# modules/crawl_engine.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from utils.logger import get_logger
import config
from collections import deque

logger = get_logger()

def get_crawl_data(domain, max_urls=50):
    """
    Web crawling like Katana.
    Collects: URLs, Parameters, Endpoints, Images, JS Files,
    CSS, Forms, Links, External Links, Internal Links,
    PDFs, Downloads, Emails, and more.
    """
    start_url = f"https://{domain}"
    result = {
        'urls': set(),
        'parameters': set(),
        'endpoints': set(),
        'images': set(),
        'js_files': set(),
        'css_files': set(),
        'forms': [],
        'links': {'internal': set(), 'external': set()},
        'pdfs': set(),
        'downloads': set(),
        'emails': set(),
        'phone_numbers': set(),
        'social_links': set(),
        'api_endpoints': set(),
        'internal_jsons': set(),
        'crawled_pages': set(),
    }
    
    try:
        # Start with initial page
        visited = set()
        queue = deque([start_url])
        max_pages = min(max_urls, 30)  # Limit to 30 pages to avoid too many requests
        
        while queue and len(visited) < max_pages:
            current_url = queue.popleft()
            if current_url in visited:
                continue
                
            try:
                response = requests.get(current_url, timeout=10, 
                                      headers={"User-Agent": config.USER_AGENT})
                if response.status_code != 200:
                    continue
                    
                visited.add(current_url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    
                    # Skip mailto, tel, javascript, etc.
                    if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                        continue
                        
                    # Clean URL (remove fragments)
                    clean_url = full_url.split('#')[0]
                    
                    # Add to URLs
                    result['urls'].add(clean_url)
                    
                    # Check if internal or external
                    if domain in clean_url or clean_url.startswith('/') or clean_url.startswith('./') or clean_url.startswith('../'):
                        result['links']['internal'].add(clean_url)
                        # Add to queue for crawling
                        if len(visited) < max_pages and clean_url not in visited:
                            queue.append(clean_url)
                    else:
                        result['links']['external'].add(clean_url)
                    
                    # Extract parameters from URLs
                    parsed = urlparse(clean_url)
                    if parsed.query:
                        params = parse_qs(parsed.query)
                        for key in params.keys():
                            result['parameters'].add(key)
                            
                    # Check for PDFs and downloads
                    if clean_url.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx')):
                        result['pdfs'].add(clean_url)
                    elif clean_url.lower().endswith(('.zip', '.rar', '.tar', '.gz', '.7z')):
                        result['downloads'].add(clean_url)
                        
                    # Extract API endpoints
                    if '/api/' in clean_url or '/v1/' in clean_url or '/v2/' in clean_url or '/rest/' in clean_url:
                        result['api_endpoints'].add(clean_url)
                        
                # Extract images
                for img in soup.find_all('img', src=True):
                    img_url = urljoin(current_url, img['src'])
                    result['images'].add(img_url)
                    
                # Extract JS files
                for script in soup.find_all('script', src=True):
                    js_url = urljoin(current_url, script['src'])
                    result['js_files'].add(js_url)
                    
                # Extract CSS files
                for link in soup.find_all('link', rel='stylesheet', href=True):
                    css_url = urljoin(current_url, link['href'])
                    result['css_files'].add(css_url)
                    
                # Extract forms
                for form in soup.find_all('form'):
                    form_data = {
                        'action': urljoin(current_url, form.get('action', '')),
                        'method': form.get('method', 'GET').upper(),
                        'inputs': []
                    }
                    for inp in form.find_all('input'):
                        input_data = {
                            'name': inp.get('name', ''),
                            'type': inp.get('type', 'text'),
                            'value': inp.get('value', '')
                        }
                        if inp.get('placeholder'):
                            input_data['placeholder'] = inp.get('placeholder')
                        form_data['inputs'].append(input_data)
                    
                    # Add select options
                    for select in form.find_all('select'):
                        options = []
                        for option in select.find_all('option'):
                            options.append({
                                'value': option.get('value', ''),
                                'text': option.text.strip()
                            })
                        if options:
                            form_data['selects'] = options
                            
                    result['forms'].append(form_data)
                    
                # Extract emails (regex)
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails_found = re.findall(email_pattern, html)
                for email in emails_found:
                    result['emails'].add(email)
                    
                # Extract phone numbers
                phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{6,15}'
                phones_found = re.findall(phone_pattern, html)
                for phone in phones_found:
                    if len(phone) >= 7:
                        result['phone_numbers'].add(phone)
                        
                # Extract social media links
                social_patterns = [
                    r'facebook\.com/[a-zA-Z0-9\.]+',
                    r'twitter\.com/[a-zA-Z0-9_]+',
                    r'instagram\.com/[a-zA-Z0-9_]+',
                    r'linkedin\.com/in/[a-zA-Z0-9-]+',
                    r'youtube\.com/[a-zA-Z0-9_-]+',
                    r'github\.com/[a-zA-Z0-9-]+',
                ]
                for pattern in social_patterns:
                    social_matches = re.findall(pattern, html)
                    for match in social_matches:
                        result['social_links'].add('https://' + match)
                        
                # Extract endpoints (paths)
                path_pattern = r'/[a-zA-Z0-9\-_/]{3,}'
                endpoints = re.findall(path_pattern, html)
                for endpoint in endpoints:
                    if len(endpoint) > 1 and endpoint not in ['/', '//']:
                        result['endpoints'].add(endpoint)
                        
                # Find JSON data in scripts
                json_pattern = r'\{\s*"[^"]+"\s*:\s*[^{}]+\s*\}'
                json_matches = re.findall(json_pattern, html)
                for json_match in json_matches[:5]:  # Limit to 5
                    result['internal_jsons'].add(json_match[:100] + '...')
                    
            except Exception as e:
                logger.warning(f"Error crawling {current_url}: {e}")
                continue
                
        # Convert sets to lists for JSON serialization
        for key in result:
            if isinstance(result[key], set):
                result[key] = list(result[key])
                
        # Add summary
        result['summary'] = {
            'total_pages_crawled': len(visited),
            'total_links': len(result['links']['internal']) + len(result['links']['external']),
            'total_images': len(result['images']),
            'total_js': len(result['js_files']),
            'total_css': len(result['css_files']),
            'total_forms': len(result['forms']),
            'total_emails': len(result['emails']),
            'total_apis': len(result['api_endpoints']),
        }
        
    except Exception as e:
        logger.error(f"Crawl engine failed: {e}")
        result['error'] = str(e)
        
    return result