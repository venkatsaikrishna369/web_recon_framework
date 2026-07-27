import dns.resolver
from utils.logger import get_logger

logger = get_logger()

def get_dns_records(domain):
    records = {"A": [], "AAAA": [], "MX": [], "NS": [], "TXT": [], "CNAME": []}
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]

    # Use Cloudflare's DNS (or Google) for reliability
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']   # <-- add this
    resolver.timeout = 10
    resolver.lifetime = 10

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            for rdata in answers:
                if rtype == "MX":
                    records["MX"].append(str(rdata.exchange).rstrip('.'))
                elif rtype == "TXT":
                    txt = ''.join([s.decode('utf-8') if isinstance(s, bytes) else str(s) for s in rdata.strings])
                    records["TXT"].append(txt)
                else:
                    records[rtype].append(str(rdata))
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            logger.error(f"DNS lookup for {rtype} failed: {e}")
    return records