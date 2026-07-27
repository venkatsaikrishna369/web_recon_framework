# config.py
import os

# Timeouts (seconds)
DNS_TIMEOUT = 5
HTTP_TIMEOUT = 10
WHOIS_TIMEOUT = 10
SSL_TIMEOUT = 10

# User-Agent for HTTP requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Output directories
OUTPUT_DIR = "output"
REPORT_HTML = os.path.join(OUTPUT_DIR, "report.html")
REPORT_MD = os.path.join(OUTPUT_DIR, "report.md")
REPORT_JSON = os.path.join(OUTPUT_DIR, "report.json")

# Enable parallel execution
PARALLEL = True

# Logging level
LOG_LEVEL = "INFO"