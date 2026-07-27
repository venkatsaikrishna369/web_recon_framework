# modules/target_intelligence.py
import socket
import whois
import tldextract
from ipwhois import IPWhois
from utils.logger import get_logger

logger = get_logger()

def get_target_intelligence(domain):
    """
    Comprehensive target intelligence gathering.
    Returns: domain, registered domain, root domain, hostname, FQDN,
    IP addresses, ASN, CIDR, organization, reverse DNS, hosting provider,
    cloud provider, registrar, DNSSEC, DNS propagation info.
    """
    result = {}
    
    try:
        # Domain parsing
        ext = tldextract.extract(domain)
        result['domain'] = domain
        result['registered_domain'] = f"{ext.domain}.{ext.suffix}"
        result['root_domain'] = ext.suffix
        result['hostname'] = ext.subdomain if ext.subdomain else domain
        result['fqdn'] = domain
        
        # IP Resolution
        try:
            ips = socket.gethostbyname_ex(domain)
            result['ipv4'] = ips[2] if len(ips) > 2 else [ips[0]]
            result['ip_addresses'] = result['ipv4']
        except:
            result['ipv4'] = []
            result['ip_addresses'] = []
            
        try:
            # IPv6 resolution (may fail)
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['1.1.1.1', '8.8.8.8']
            answers = resolver.resolve(domain, 'AAAA')
            result['ipv6'] = [str(r) for r in answers]
        except:
            result['ipv6'] = []
            
        # WHOIS Information
        try:
            w = whois.whois(domain)
            result['registrar'] = w.registrar if w.registrar else 'N/A'
            result['registrant_organization'] = w.org if w.org else 'N/A'
            result['dnssec'] = w.dnssec if hasattr(w, 'dnssec') else 'Unknown'
            result['creation_date'] = str(w.creation_date) if w.creation_date else 'N/A'
            result['expiration_date'] = str(w.expiration_date) if w.expiration_date else 'N/A'
            result['name_servers'] = w.name_servers if w.name_servers else []
        except:
            result['registrar'] = 'N/A'
            result['dnssec'] = 'Unknown'
            result['creation_date'] = 'N/A'
            result['expiration_date'] = 'N/A'
            result['name_servers'] = []
            
        # ASN & Organization (using first IP) - FIXED: use lookup_rdap()
        if result.get('ipv4') and len(result['ipv4']) > 0:
            try:
                ip_obj = IPWhois(result['ipv4'][0])
                ip_info = ip_obj.lookup_rdap()
                result['asn'] = ip_info.get('asn', 'N/A')
                result['asn_name'] = ip_info.get('asn_description', 'N/A')
                result['organization'] = ip_info.get('org', 'N/A')
                network = ip_info.get('network', {})
                if isinstance(network, dict):
                    result['cidr'] = network.get('cidr', 'N/A')
                else:
                    result['cidr'] = 'N/A'
            except Exception as e:
                logger.warning(f"ASN lookup failed: {e}")
                result['asn'] = 'N/A'
                result['asn_name'] = 'N/A'
                result['organization'] = 'N/A'
                result['cidr'] = 'N/A'
                
        # Reverse DNS - FIXED: proper indentation
        if result.get('ipv4') and len(result['ipv4']) > 0:
            try:
                # Try multiple methods for reverse DNS
                ip = result['ipv4'][0]
                try:
                    result['reverse_dns'] = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    try:
                        result['reverse_dns'] = socket.getnameinfo((ip, 0), 0)[0]
                    except:
                        result['reverse_dns'] = 'N/A'
            except:
                result['reverse_dns'] = 'N/A'
                
        # Hosting Provider Detection
        result['hosting_provider'] = detect_hosting_provider(str(result.get('asn', '')))
        result['cloud_provider'] = detect_cloud_provider(str(result.get('asn', '')))
        
        # DNS Propagation (simplified)
        result['dns_propagation'] = {
            'cloudflare': 'Detected' if 'cloudflare' in str(result.get('asn', '')).lower() else 'Unknown',
            'google': 'Detected' if 'google' in str(result.get('asn', '')).lower() else 'Unknown',
        }
        
    except Exception as e:
        logger.error(f"Target intelligence failed: {e}")
        result['error'] = str(e)
        
    return result

def detect_hosting_provider(asn):
    """Detect hosting provider based on ASN"""
    providers = {
        '13335': 'Cloudflare',
        '15169': 'Google Cloud',
        '16509': 'AWS',
        '8075': 'Microsoft Azure',
        '32934': 'Facebook',
        '54113': 'Fastly',
        '14618': 'Amazon',
        '16276': 'OVH',
    }
    asn_str = str(asn)
    for code, name in providers.items():
        if code in asn_str:
            return name
    return 'Unknown'

def detect_cloud_provider(asn):
    """Detect cloud provider based on ASN"""
    cloud_providers = {
        '13335': 'Cloudflare',
        '15169': 'Google Cloud Platform',
        '16509': 'Amazon Web Services',
        '8075': 'Microsoft Azure',
        '16276': 'OVH Cloud',
        '20473': 'Vultr',
        '14618': 'Amazon AWS',
        '54113': 'Fastly',
    }
    asn_str = str(asn)
    for code, name in cloud_providers.items():
        if code in asn_str:
            return name
    return 'Unknown'