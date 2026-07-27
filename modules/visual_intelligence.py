# modules/visual_intelligence.py
import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger
import config
import base64
from urllib.parse import urljoin

logger = get_logger()

def get_visual_intelligence(domain):
    """
    Visual intelligence gathering.
    Collects: Page Title, Logo, Favicon, Viewport, Meta tags.
    (Screenshot functionality uses a simple approach without Selenium)
    """
    url = f"https://{domain}"
    result = {
        'page_title': 'No title',
        'viewport': 'Not specified',
        'favicon': '/favicon.ico',
        'logo': 'Not found',
        'screenshot': 'Screenshot requires Selenium setup',
        'mobile_screenshot': 'Screenshot requires Selenium setup',
        'meta_tags': {},
        'og_tags': {},
        'twitter_tags': {}
    }
    
    try:
        # Basic page info
        response = requests.get(url, timeout=10, headers={"User-Agent": config.USER_AGENT})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Page Title
        title_tag = soup.find('title')
        result['page_title'] = title_tag.text.strip() if title_tag else 'No title'
        
        # Viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        result['viewport'] = viewport.get('content') if viewport else 'Not specified'
        
        # Favicon - try multiple ways
        favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon and favicon.get('href'):
            result['favicon'] = urljoin(url, favicon['href'])
        else:
            # Try default favicon location
            result['favicon'] = urljoin(url, '/favicon.ico')
            
        # Logo detection - look for common logo patterns
        logo_selectors = [
            'img[alt*="logo"]',
            'img[class*="logo"]',
            'img[id*="logo"]',
            'div[class*="logo"] img',
            'header img',
            'nav img',
            '.brand img',
            '.site-logo img'
        ]
        
        for selector in logo_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    if element.name == 'img' and element.get('src'):
                        result['logo'] = urljoin(url, element['src'])
                        break
                    elif element.name == 'div' and element.find('img'):
                        img = element.find('img')
                        if img and img.get('src'):
                            result['logo'] = urljoin(url, img['src'])
                            break
                if result['logo'] != 'Not found':
                    break
                    
        # If no logo found, try to find the largest image that might be a logo
        if result['logo'] == 'Not found':
            images = soup.find_all('img')
            for img in images:
                if img.get('src') and img.get('alt'):
                    if 'logo' in img.get('alt', '').lower():
                        result['logo'] = urljoin(url, img['src'])
                        break
                        
        # Collect Open Graph tags
        og_tags = {}
        for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            property_name = meta.get('property', '')
            content = meta.get('content', '')
            if property_name and content:
                og_tags[property_name] = content
        result['og_tags'] = og_tags
        
        # Collect Twitter Cards
        twitter_tags = {}
        for meta in soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')}):
            name = meta.get('name', '')
            content = meta.get('content', '')
            if name and content:
                twitter_tags[name] = content
        result['twitter_tags'] = twitter_tags
        
        # Collect all meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        result['meta_tags'] = meta_tags
        
        # Description
        description = soup.find('meta', attrs={'name': 'description'})
        if description and description.get('content'):
            result['description'] = description['content']
        else:
            result['description'] = 'No description'
            
        # Keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords and keywords.get('content'):
            result['keywords'] = keywords['content']
        else:
            result['keywords'] = 'No keywords'
            
        # Try to take a screenshot using a simple method (base64 of rendered HTML)
        # This is a placeholder - for real screenshots, need selenium
        try:
            # Just encode the first part of HTML as a simple representation
            html_preview = html[:5000] if len(html) > 5000 else html
            result['html_preview'] = base64.b64encode(html_preview.encode()).decode()
        except:
            pass
            
    except Exception as e:
        logger.error(f"Visual intelligence failed: {e}")
        result['error'] = str(e)
        
    return result

# Optional: If you want to use Selenium for screenshots, uncomment this function
# and install selenium and chromedriver
"""
def capture_screenshot_with_selenium(url, mobile=False):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        if mobile:
            options.add_argument('--window-size=375,812')
        else:
            options.add_argument('--window-size=1920,1080')
            
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # Wait for page to load
        driver.implicitly_wait(3)
        screenshot = driver.get_screenshot_as_base64()
        driver.quit()
        return f"data:image/png;base64,{screenshot}"
    except Exception as e:
        logger.warning(f"Screenshot failed: {e}")
        return 'Screenshot unavailable'
"""