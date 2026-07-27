# utils/validator.py
import re
from urllib.parse import urlparse

def validate_target(target):
    """
    Extract domain from URL or domain string.
    Returns cleaned domain or None if invalid.
    """
    target = target.strip()
    if not target:
        return None
    # Remove protocol if present
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        domain = parsed.netloc
    else:
        domain = target
    # Remove trailing slashes and path
    domain = domain.split('/')[0]
    # Basic domain validation (simple regex)
    # Allow IDN? We'll just check pattern
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    if re.match(pattern, domain):
        return domain
    # If it's an IP, allow it? We'll treat as domain for now, but we could handle.
    # For simplicity, accept if it has dots and not just numeric.
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
        return domain
    return None