# modules/security_headers.py
from utils.logger import get_logger

logger = get_logger()

def analyze_security_headers(headers):
    """
    Check for security headers and produce findings.
    Returns dict with checks, missing, and server banner detection.
    """
    # Security headers to check
    security_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Embedder-Policy",
        "Cross-Origin-Resource-Policy"
    ]
    # Normalize keys (case-insensitive)
    headers_lower = {k.lower(): v for k, v in headers.items()}
    results = {}
    missing = []
    for h in security_headers:
        val = headers_lower.get(h.lower())
        if val:
            results[h] = val
        else:
            missing.append(h)
            results[h] = None

    # Server banner and X-Powered-By
    server = headers_lower.get("server", None)
    x_powered_by = headers_lower.get("x-powered-by", None)
    
    # Risk scoring: count missing critical headers
    # critical: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
    critical = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options"]
    missing_critical = [h for h in critical if h.lower() in missing]
    risk_score = len(missing_critical)  # higher is worse

    return {
        "checks": results,
        "missing": missing,
        "server_banner": server,
        "x_powered_by": x_powered_by,
        "risk_score": risk_score,
        "summary": {
            "has_csp": "Content-Security-Policy" in results and results["Content-Security-Policy"] is not None,
            "has_hsts": "Strict-Transport-Security" in results and results["Strict-Transport-Security"] is not None,
            "server_exposed": server is not None,
            "x_powered_exposed": x_powered_by is not None
        }
    }