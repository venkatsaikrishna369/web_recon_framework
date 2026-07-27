# modules/dns_intelligence.py
import dns.resolver
import dns.query
import dns.zone
from utils.logger import get_logger

logger = get_logger()

def get_dns_intelligence(domain):
    """
    Advanced DNS intelligence gathering.
    Collects: A, AAAA, MX, TXT, CNAME, CAA, SRV, PTR, SOA, NS,
    DNSSEC, SPF, DMARC, DKIM, wildcard detection, zone transfer.
    """
    result = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']
    resolver.timeout = 10
    resolver.lifetime = 10
    
    # Record types to collect
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'CAA', 'SRV', 'PTR', 'SOA', 'NS']
    
    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            result[rtype] = [str(r) for r in answers]
        except:
            result[rtype] = []
            
    # DNSSEC Check
    try:
        result['dnssec'] = resolver.resolve(domain, 'DNSKEY') is not None
    except:
        result['dnssec'] = False
        
    # SPF (special TXT record)
    try:
        spf_records = resolver.resolve(domain, 'TXT')
        result['spf'] = [str(r) for r in spf_records if 'v=spf1' in str(r)]
    except:
        result['spf'] = []
        
    # DMARC
    try:
        dmarc = resolver.resolve(f'_dmarc.{domain}', 'TXT')
        result['dmarc'] = [str(r) for r in dmarc]
    except:
        result['dmarc'] = []
        
    # DKIM (look for common selectors)
    dkim_selectors = ['default', 'google', 'mail', 'dkim']
    result['dkim'] = []
    for selector in dkim_selectors:
        try:
            dkim = resolver.resolve(f'{selector}._domainkey.{domain}', 'TXT')
            if dkim:
                result['dkim'].extend([str(r) for r in dkim])
        except:
            pass
            
    # Wildcard DNS Detection
    try:
        random_subdomain = f"test-{hash(domain)}.{domain}"
        wildcard = resolver.resolve(random_subdomain, 'A')
        result['wildcard_dns'] = len(wildcard) > 0
    except:
        result['wildcard_dns'] = False
        
    # Zone Transfer Attempt (authorized only)
    result['zone_transfer'] = 'Not Attempted'
    
    # DNS TTL
    try:
        ns_records = resolver.resolve(domain, 'NS')
        if ns_records:
            result['dns_ttl'] = str(ns_records.response.message.max_ttl)
    except:
        result['dns_ttl'] = 'Unknown'
        
    # DNS Leaks (check if multiple nameservers respond differently)
    result['dns_leaks'] = check_dns_leaks(domain)
    
    return result

def check_dns_leaks(domain):
    """Check for DNS leaks by comparing responses from different resolvers"""
    resolvers = ['1.1.1.1', '8.8.8.8', '9.9.9.9']
    responses = []
    for ns in resolvers:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [ns]
            answers = resolver.resolve(domain, 'A')
            responses.append(set([str(r) for r in answers]))
        except:
            pass
    # If different resolvers return different IPs, there might be a leak
    if len(set([tuple(sorted(r)) for r in responses])) > 1:
        return 'Possible DNS leak detected'
    return 'No DNS leaks detected'