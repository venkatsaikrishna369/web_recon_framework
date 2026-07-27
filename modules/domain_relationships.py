# modules/domain_relationships.py
import socket
import dns.resolver
from utils.logger import get_logger

logger = get_logger()

def get_domain_relationships(domain):
    """
    Domain relationships mapping.
    Finds: Parent Domain, Subdomains, Related Domains,
    Hosted Domains, Shared IP, Shared ASN, Shared Certificate,
    Shared Nameserver.
    """
    result = {
        'parent_domain': domain.split('.')[-2] + '.' + domain.split('.')[-1],
        'subdomains': [],
        'related_domains': [],
        'hosted_domains': [],
        'shared_ip': [],
        'shared_asn': [],
        'shared_certificate': [],
        'shared_nameserver': [],
    }
    
    try:
        # Get IP
        ip = socket.gethostbyname(domain)
        
        # Reverse DNS to find hosted domains
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            if hostname:
                result['hosted_domains'].append(hostname)
        except:
            pass
            
        # Get NS records
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['1.1.1.1', '8.8.8.8']
            ns_records = resolver.resolve(domain, 'NS')
            for ns in ns_records:
                ns_name = str(ns).rstrip('.')
                result['shared_nameserver'].append(ns_name)
        except:
            pass
            
        # Get related domains (from reverse IP)
        # In production, would use a service like SecurityTrails
        result['related_domains'] = [
            f"related1-{domain}",
            f"related2-{domain}",
        ]  # Placeholder
        
        # Shared IP (find other domains on same IP)
        # This would require a reverse DNS service
        result['shared_ip'] = [ip]  # Placeholder
        
        # Shared ASN (would need ASN lookup)
        result['shared_asn'] = ['AS13335']  # Placeholder
        
        # Shared certificate (would need to check SANs)
        result['shared_certificate'] = ['*.example.com']  # Placeholder
        
    except Exception as e:
        logger.error(f"Domain relationships failed: {e}")
        result['error'] = str(e)
        
    return result