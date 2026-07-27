# modules/security_observations.py
import requests
from urllib.parse import urljoin
from utils.logger import get_logger
import config

logger = get_logger()

def get_security_observations(domain):
    """
    Comprehensive security observations with proper risk scoring.
    Returns findings categorized by severity and a risk score.
    """
    url = f"https://{domain}"
    result = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': [],
        'info': [],
        'risk_score': 0,
        'risk_level': 'Low'
    }
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": config.USER_AGENT})
        headers = response.headers
        
        # Check critical security headers
        if 'Content-Security-Policy' not in headers:
            result['high'].append('Missing Content-Security-Policy (CSP) - XSS protection missing')
        else:
            result['info'].append('✅ CSP header present')
            
        if 'Strict-Transport-Security' not in headers:
            result['high'].append('Missing Strict-Transport-Security (HSTS) - No HTTPS enforcement')
        else:
            result['info'].append('✅ HSTS header present')
            
        if 'X-Frame-Options' not in headers:
            result['medium'].append('Missing X-Frame-Options - Clickjacking vulnerability')
        else:
            result['info'].append('✅ X-Frame-Options header present')
            
        if 'X-Content-Type-Options' not in headers:
            result['medium'].append('Missing X-Content-Type-Options - MIME sniffing vulnerability')
        else:
            result['info'].append('✅ X-Content-Type-Options header present')
            
        if 'Referrer-Policy' not in headers:
            result['low'].append('Missing Referrer-Policy - Information leakage possible')
        else:
            result['info'].append('✅ Referrer-Policy header present')
            
        if 'Permissions-Policy' not in headers:
            result['low'].append('Missing Permissions-Policy - Browser feature misuse possible')
        else:
            result['info'].append('✅ Permissions-Policy header present')
            
        # Cookie security
        if 'Set-Cookie' in headers:
            cookies = headers.get('Set-Cookie', '')
            if 'Secure' not in cookies:
                result['medium'].append('Cookies missing Secure flag - Cookies sent over HTTP')
            if 'HttpOnly' not in cookies:
                result['medium'].append('Cookies missing HttpOnly flag - JavaScript access possible')
            if 'SameSite' not in cookies:
                result['low'].append('Cookies missing SameSite attribute - CSRF vulnerability')
        else:
            result['info'].append('No cookies set')
            
        # Server disclosure
        if 'Server' in headers:
            result['low'].append(f'Server header exposed: {headers["Server"]}')
        if 'X-Powered-By' in headers:
            result['low'].append(f'X-Powered-By header exposed: {headers["X-Powered-By"]}')
            
        # Check for robots.txt exposure
        try:
            robots_url = urljoin(url, '/robots.txt')
            robots_response = requests.get(robots_url, timeout=5)
            if robots_response.status_code == 200:
                if 'Disallow: /' in robots_response.text:
                    result['medium'].append('robots.txt contains sensitive paths')
                result['info'].append('robots.txt found')
        except:
            pass
            
        # Check for sitemap.xml
        try:
            sitemap_url = urljoin(url, '/sitemap.xml')
            sitemap_response = requests.get(sitemap_url, timeout=5)
            if sitemap_response.status_code == 200:
                result['info'].append('sitemap.xml found')
        except:
            pass
            
        # Check for exposed sensitive files
        sensitive_files = ['.env', '.git/config', '.htaccess', 'wp-config.php', 'composer.json']
        for file in sensitive_files:
            try:
                file_url = urljoin(url, file)
                file_response = requests.get(file_url, timeout=3)
                if file_response.status_code == 200:
                    result['critical'].append(f'Sensitive file exposed: {file}')
            except:
                pass
                
        # Check for directory listing
        try:
            dir_response = requests.get(urljoin(url, '/uploads/'), timeout=3)
            if '<title>Index of /uploads' in dir_response.text:
                result['high'].append('Directory listing enabled on /uploads/')
        except:
            pass
            
        # Calculate risk score
        risk_weights = {
            'critical': 10,
            'high': 5,
            'medium': 3,
            'low': 1
        }
        
        total_score = 0
        for severity in ['critical', 'high', 'medium', 'low']:
            total_score += len(result[severity]) * risk_weights[severity]
            
        result['risk_score'] = min(100, total_score * 2)  # Max 100
        
        # Set risk level
        if result['risk_score'] >= 80:
            result['risk_level'] = 'Critical'
        elif result['risk_score'] >= 60:
            result['risk_level'] = 'High'
        elif result['risk_score'] >= 40:
            result['risk_level'] = 'Medium'
        elif result['risk_score'] >= 20:
            result['risk_level'] = 'Low'
        else:
            result['risk_level'] = 'Secure'
            
    except Exception as e:
        logger.error(f"Security observations failed: {e}")
        result['error'] = str(e)
        
    return result