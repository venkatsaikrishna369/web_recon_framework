# modules/whois_lookup.py
import whois
from utils.logger import get_logger

logger = get_logger()

def get_whois(domain):
    """
    Collect WHOIS information for the domain.
    Returns dict with keys: domain_name, registrar, creation_date, updated_date,
    expiration_date, name_servers, registrant_organization, status.
    """
    try:
        w = whois.whois(domain)
        if not w:
            return {"error": "WHOIS data not available"}

        # Convert dates to string if present
        def fmt_date(dt):
            if dt:
                return dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)
            return "N/A"

        data = {
            "domain_name": w.domain_name if w.domain_name else domain,
            "registrar": w.registrar or "N/A",
            "creation_date": fmt_date(w.creation_date),
            "updated_date": fmt_date(w.updated_date),
            "expiration_date": fmt_date(w.expiration_date),
            "name_servers": w.name_servers if w.name_servers else [],
            "registrant_organization": w.org or "N/A",
            "status": w.status or "N/A",
        }
        logger.info(f"WHOIS lookup successful for {domain}")
        return data
    except Exception as e:
        logger.error(f"WHOIS lookup failed: {e}")
        return {"error": f"WHOIS lookup failed: {str(e)}"}