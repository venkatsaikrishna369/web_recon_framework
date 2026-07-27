# modules/ip_lookup.py
import socket
from utils.logger import get_logger

logger = get_logger()

def resolve_ip(domain):
    """
    Resolve IPv4 and IPv6 addresses for the domain.
    Returns dict with "ipv4", "ipv6", "resolved_ip" (first IPv4).
    """
    try:
        addrinfo = socket.getaddrinfo(domain, None)
        ipv4 = []
        ipv6 = []
        for addr in addrinfo:
            family, _, _, _, sockaddr = addr
            ip = sockaddr[0]
            if family == socket.AF_INET:
                ipv4.append(ip)
            elif family == socket.AF_INET6:
                ipv6.append(ip)
        # Deduplicate
        ipv4 = list(dict.fromkeys(ipv4))
        ipv6 = list(dict.fromkeys(ipv6))
        resolved_ip = ipv4[0] if ipv4 else (ipv6[0] if ipv6 else None)
        return {
            "resolved_ip": resolved_ip,
            "ipv4": ipv4,
            "ipv6": ipv6
        }
    except socket.gaierror as e:
        logger.error(f"IP resolution failed: {e}")
        return {"error": f"Resolution failed: {str(e)}"}