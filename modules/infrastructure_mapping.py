# modules/infrastructure_mapping.py - Full corrected version
import socket
import requests
from utils.logger import get_logger

logger = get_logger()

def get_infrastructure_mapping(domain):
    """Map infrastructure with proper geolocation"""
    result = {}
    
    try:
        # Get IP
        ip = socket.gethostbyname(domain)
        result['ip'] = ip
        
        # Get geolocation from ip-api.com
        geo_data = get_geolocation(ip)
        result.update(geo_data)
        
        # Get ASN info using ipwhois
        try:
            from ipwhois import IPWhois
            ip_obj = IPWhois(ip)
            ip_info = ip_obj.lookup_rdap()
            result['asn'] = ip_info.get('asn', 'N/A')
            result['asn_name'] = ip_info.get('asn_description', 'N/A')
            result['isp'] = ip_info.get('org', 'N/A')
            if result['isp'] == 'N/A':
                result['isp'] = geo_data.get('isp', 'N/A')
        except Exception as e:
            logger.warning(f"ASN lookup failed: {e}")
            result['asn'] = 'N/A'
            result['asn_name'] = 'N/A'
            result['isp'] = geo_data.get('isp', 'N/A')
        
        # Reverse DNS
        result['reverse_dns'] = get_reverse_dns(ip)
        
        # Cloud Provider Detection
        result['cloud_provider'] = detect_cloud_provider(ip, result.get('asn', ''))
        
        # CIDR Block
        try:
            from ipwhois import IPWhois
            ip_obj = IPWhois(ip)
            ip_info = ip_obj.lookup_rdap()
            network = ip_info.get('network', {})
            if isinstance(network, dict):
                result['cidr_block'] = network.get('cidr', 'N/A')
            else:
                result['cidr_block'] = 'N/A'
        except:
            result['cidr_block'] = 'N/A'
            
    except Exception as e:
        logger.error(f"Infrastructure mapping failed: {e}")
        result['error'] = str(e)
        
    return result

def get_geolocation(ip):
    """Get geolocation from IP using ip-api.com"""
    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,as",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'latitude': data.get('lat', 'N/A'),
                    'longitude': data.get('lon', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                }
    except Exception as e:
        logger.warning(f"Geolocation API error: {e}")
    
    return {
        'country': 'N/A',
        'region': 'N/A', 
        'city': 'N/A',
        'latitude': 'N/A',
        'longitude': 'N/A',
        'isp': 'N/A',
        'org': 'N/A',
    }

def get_reverse_dns(ip):
    """Get reverse DNS with fallback methods"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        try:
            return socket.getnameinfo((ip, 0), 0)[0]
        except:
            try:
                import dns.resolver
                resolver = dns.resolver.Resolver()
                resolver.nameservers = ['1.1.1.1', '8.8.8.8']
                ip_parts = ip.split('.')
                reverse_ip = f"{ip_parts[3]}.{ip_parts[2]}.{ip_parts[1]}.{ip_parts[0]}.in-addr.arpa"
                answers = resolver.resolve(reverse_ip, 'PTR')
                if answers:
                    return str(answers[0]).rstrip('.')
            except:
                pass
    return 'N/A'

def detect_cloud_provider(ip, asn):
    """Detect cloud provider from IP and ASN"""
    asn_str = str(asn)
    cloud_by_asn = {
        '13335': 'Cloudflare',
        '15169': 'Google Cloud Platform',
        '16509': 'Amazon Web Services',
        '8075': 'Microsoft Azure',
        '16276': 'OVH Cloud',
        '20473': 'Vultr',
        '14618': 'Amazon AWS',
        '54113': 'Fastly',
    }
    for code, name in cloud_by_asn.items():
        if code in asn_str:
            return name
    
    if ip.startswith(('104.16.', '104.17.', '104.18.', '104.19.', '104.20.', '104.21.', '104.22.', '104.23.', '104.24.', '104.25.', '104.26.', '104.27.', '172.64.', '173.245.')):
        return 'Cloudflare'
    elif ip.startswith(('52.', '54.', '34.', '35.', '3.', '13.', '18.', '75.')):
        return 'Amazon AWS'
    elif ip.startswith(('40.', '13.64.', '13.65.', '13.66.', '13.67.', '13.68.', '13.69.', '13.70.', '13.71.', '13.72.', '13.73.', '13.74.', '13.75.', '13.76.', '13.77.', '13.78.', '13.79.', '13.80.', '13.81.', '13.82.', '13.83.', '13.84.', '13.85.', '13.86.', '13.87.', '13.88.', '13.89.', '13.90.', '13.91.', '13.92.', '13.93.', '13.94.', '13.95.')):
        return 'Microsoft Azure'
    elif ip.startswith(('35.', '34.')):
        return 'Google Cloud Platform'
    elif ip.startswith(('8.')):
        return 'Google'
    
    return 'Unknown'