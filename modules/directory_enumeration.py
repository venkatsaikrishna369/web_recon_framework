# modules/directory_enumeration.py
import requests
from concurrent.futures import ThreadPoolExecutor
from utils.logger import get_logger
import config

logger = get_logger()

def get_directory_enumeration(domain):
    """
    Directory enumeration like Gobuster.
    Checks common directories for existence.
    """
    url = f"https://{domain}"
    directories = [
        'admin', 'backup', 'old', 'test', 'login', 'api', 'uploads',
        'private', 'config', 'dashboard', 'wp-admin', 'wp-content',
        'cgi-bin', 'images', 'css', 'js', 'assets', 'media',
        'download', 'files', 'tmp', 'temp', 'logs', 'cache',
        'vendor', 'node_modules', 'dist', 'build', 'src',
        'app', 'system', 'includes', 'lib', 'model', 'controller'
    ]
    
    result = {
        'found': [],
        'response_codes': {},
    }
    
    def check_directory(dir_name):
        try:
            full_url = f"{url}/{dir_name}"
            response = requests.get(full_url, timeout=5, headers={"User-Agent": config.USER_AGENT})
            if response.status_code < 400:
                return {'url': full_url, 'status': response.status_code, 'size': len(response.text)}
        except:
            pass
        return None
        
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_directory, dir_name) for dir_name in directories]
        for future in futures:
            result_item = future.result()
            if result_item:
                result['found'].append(result_item['url'])
                result['response_codes'][result_item['url']] = result_item['status']
                
    return result