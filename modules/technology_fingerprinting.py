# modules/technology_fingerprinting.py
import re
from bs4 import BeautifulSoup
import requests
from utils.logger import get_logger

logger = get_logger()

def get_technology_fingerprint(domain):
    """
    Technology fingerprinting like Wappalyzer.
    Detects: servers, frameworks, libraries, CDNs, languages.
    """
    url = f"https://{domain}"
    result = {
        'servers': [],
        'languages': [],
        'frameworks': [],
        'libraries': [],
        'cdn': [],
        'cms': [],
    }
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text
        headers = response.headers
        soup = BeautifulSoup(html, 'html.parser')
        
        # Server detection
        server = headers.get('Server', '')
        if 'nginx' in server.lower():
            result['servers'].append('Nginx')
        elif 'apache' in server.lower():
            result['servers'].append('Apache')
        elif 'iis' in server.lower():
            result['servers'].append('IIS')
        elif 'cloudflare' in server.lower():
            result['servers'].append('Cloudflare')
        elif 'openresty' in server.lower():
            result['servers'].append('OpenResty')
        elif 'litespeed' in server.lower():
            result['servers'].append('LiteSpeed')
        elif 'tomcat' in server.lower():
            result['servers'].append('Tomcat')
            
        # Language detection
        if '.php' in html or 'php' in headers.get('X-Powered-By', '').lower():
            result['languages'].append('PHP')
        if '.aspx' in html or 'asp.net' in headers.get('X-Powered-By', '').lower():
            result['languages'].append('ASP.NET')
        if '.jsp' in html:
            result['languages'].append('JSP')
        if 'node' in html.lower() or 'node.js' in headers.get('X-Powered-By', '').lower():
            result['languages'].append('Node.js')
        if 'django' in html.lower():
            result['languages'].append('Python')
        if 'rails' in html.lower() or '.rb' in html.lower():
            result['languages'].append('Ruby')
            
        # Framework detection
        frameworks = {
            'react': 'React',
            'angular': 'Angular',
            'vue': 'Vue.js',
            'bootstrap': 'Bootstrap',
            'jquery': 'jQuery',
            'tailwind': 'Tailwind CSS',
            'django': 'Django',
            'rails': 'Ruby on Rails',
            'laravel': 'Laravel',
            'spring': 'Spring',
            'flask': 'Flask',
        }
        for pattern, framework in frameworks.items():
            if pattern in html.lower():
                result['frameworks'].append(framework)
                
        # Libraries
        libraries = {
            'moment.js': 'moment',
            'lodash': 'lodash',
            'axios': 'axios',
            'underscore': 'underscore',
            'd3': 'D3.js',
            'three.js': 'Three.js',
        }
        for lib, lib_name in libraries.items():
            if lib.lower() in html.lower():
                result['libraries'].append(lib_name)
                
        # CDN detection
        cdn_indicators = {
            'cloudflare': 'Cloudflare',
            'fastly': 'Fastly',
            'akamai': 'Akamai',
            'cloudfront': 'AWS CloudFront',
        }
        for indicator, cdn in cdn_indicators.items():
            if indicator in html.lower() or indicator in str(headers).lower():
                result['cdn'].append(cdn)
                
        # CMS detection
        cms = {
            'wp-content': 'WordPress',
            'drupal': 'Drupal',
            'joomla': 'Joomla',
            'shopify': 'Shopify',
            'magento': 'Magento',
            'wix': 'Wix',
        }
        for pattern, cms_name in cms.items():
            if pattern in html.lower():
                result['cms'].append(cms_name)
                
    except Exception as e:
        logger.error(f"Technology fingerprinting failed: {e}")
        result['error'] = str(e)
        
    # Deduplicate
    for key in result:
        result[key] = list(set(result[key]))
        
    return result