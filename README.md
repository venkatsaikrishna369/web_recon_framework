# 🔍 Web Recon Automation Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)]()
[![Modules](https://img.shields.io/badge/Modules-23-orange?style=for-the-badge)]()

**Web Recon Automation Framework** is an advanced, modular, and production-ready reconnaissance platform that automates the entire process of gathering public intelligence about a target domain. With **23 specialized modules**, it collects everything from WHOIS information to security headers, and compiles it into a professional, client-ready report with a single command.

This framework is designed for penetration testers, red teamers, security engineers, and bug bounty hunters who need fast, reliable, and repeatable reconnaissance.

---

## Features

- **23 Specialized Modules** – Each module handles a specific reconnaissance task
- **Parallel Execution** – Modules run concurrently for maximum speed
- **Error Resilience** – Logs errors and continues – never crashes
- **Professional Reports** – HTML, Markdown, and JSON formats
- **Risk Scoring** – Automatic risk assessment with color-coded severity
- **Security Analysis** – CSP, HSTS, XFO, and 6+ other security headers
- **Crawl Engine** – Like Katana – extracts URLs, endpoints, forms, emails
- **Tech Fingerprinting** – Detects frameworks, libraries, and CMS
- **Visual Intelligence** – Page title, favicon, viewport, meta tags

---

## Tech Stack

### Core
- **Python** – Primary programming language
- **Jinja2** – HTML templating for report generation

### Dependencies
- `requests` – HTTP requests
- `python-whois` – WHOIS lookup
- `dnspython` – DNS resolution
- `cryptography` – SSL certificate parsing
- `beautifulsoup4` – HTML parsing
- `lxml` – XML parsing
- `tldextract` – Domain parsing
- `ipwhois` – IP/ASN intelligence
- `pillow` – Image processing

---

## Project Structure

```text
web_recon_framework/
├── main.py                 # Orchestrator - runs all modules
├── config.py               # Configuration settings
│
├── modules/                # 23 Intelligence Modules
│   ├── whois_lookup.py     # 1. WHOIS Information
│   ├── dns_lookup.py       # 2. DNS Records
│   ├── ip_lookup.py        # 3. IP Address
│   ├── geo_lookup.py       # 4. Geolocation
│   ├── headers.py          # 5. HTTP Headers
│   ├── ssl_info.py         # 6. SSL Certificate
│   ├── robots.py           # 7. robots.txt
│   ├── sitemap.py          # 8. sitemap.xml
│   ├── security_headers.py # 9. Security Headers
│   ├── target_intelligence.py    # 10. Target Intelligence
│   ├── dns_intelligence.py       # 11. DNS Intelligence
│   ├── infrastructure_mapping.py # 12. Infrastructure
│   ├── http_intelligence.py      # 13. HTTP Intelligence
│   ├── ssl_intelligence.py       # 14. SSL Intelligence
│   ├── technology_fingerprinting.py # 15. Tech Fingerprinting
│   ├── crawl_engine.py           # 16. Crawl Engine
│   ├── javascript_analysis.py    # 17. JS Analysis
│   ├── directory_enumeration.py  # 18. Directory Enumeration
│   ├── security_observations.py  # 19. Security Observations
│   ├── visual_intelligence.py    # 20. Visual Intelligence
│   ├── page_statistics.py        # 21. Page Statistics
│   ├── domain_relationships.py   # 22. Domain Relationships
│   └── report_engine.py          # 23. Report Engine
│
├── reports/                # Report Generators
│   ├── html_generator.py   # Professional HTML report
│   └── markdown_generator.py # Markdown report
│
├── utils/                  # Helper Utilities
│   ├── logger.py           # Logging setup
│   ├── validator.py        # Input validation
│   └── helpers.py          # Common helper functions
│
└── output/                 # Generated Reports
    ├── report.html
    ├── report.md
    └── report.json
---

# 🚀 Run Locally

Follow these steps to set up and run the **Web Recon Automation Framework** on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python **3.8** or higher
- pip (Python Package Manager)
- Git

---

## 📥 Clone the Repository

```bash
git clone https://github.com/venkatsaikrishna369/web_recon_framework.git

cd web_recon_framework
```

---

## 📦 Create a Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 📚 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📖 Python Packages Used

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.31.0+ | HTTP requests |
| python-whois | 0.8.0+ | WHOIS lookup |
| dnspython | 2.4.0+ | DNS resolution |
| cryptography | 41.0.0+ | SSL certificate parsing |
| Jinja2 | 3.1.0+ | HTML report templating |
| beautifulsoup4 | 4.12.0+ | HTML parsing |
| lxml | 4.9.0+ | XML parsing |
| tldextract | 3.5.0+ | Domain parsing |
| ipwhois | 1.3.0+ | IP & ASN intelligence |
| pillow | 10.0.0+ | Image processing |

---

# ▶️ Running the Framework

## Basic Usage

```bash
python main.py example.com
```

---

## Advanced Usage

### Save reports to a custom directory

```bash
python main.py google.com --output my_reports
```

### Skip HTML and Markdown report generation

```bash
python main.py github.com --no-html --no-md
```

### Set a custom timeout

```bash
python main.py hackthebox.com --timeout 30
```

### Interactive Mode

Run the framework without arguments to enter interactive mode.

```bash
python main.py
```

---

## 📁 Generated Output

After execution, the framework automatically creates an **output/** directory containing:

```text
output/
├── report.html
├── report.md
└── report.json
```

- **HTML Report** – Interactive professional report
- **Markdown Report** – Lightweight report for GitHub and documentation
- **JSON Report** – Raw reconnaissance data for automation and integration
---

# 📊 Output Reports

After a successful scan, the framework automatically generates three professional report formats inside the **output/** directory.

| Report | Format | Description |
|--------|--------|-------------|
| 🌐 HTML Report | `.html` | Interactive dashboard with risk score, visual styling, and printable report |
| 📝 Markdown Report | `.md` | Lightweight report suitable for GitHub, documentation, and wikis |
| 📄 JSON Report | `.json` | Complete structured reconnaissance data for automation and integrations |

### Output Directory

```text
output/
├── report.html
├── report.md
└── report.json
```

---

# 🧩 Module Breakdown

The framework consists of **23 specialized reconnaissance modules**, each responsible for collecting a specific category of intelligence.

| # | Module | File | Description |
|---|--------|------|-------------|
| 1 | WHOIS Information | `whois_lookup.py` | Retrieves domain registration details, registrar, creation date, expiry date, and name servers. |
| 2 | DNS Records | `dns_lookup.py` | Collects A, AAAA, MX, NS, TXT, and CNAME records. |
| 3 | IP Address Lookup | `ip_lookup.py` | Resolves IPv4 and IPv6 addresses. |
| 4 | Geolocation | `geo_lookup.py` | Identifies country, city, ISP, ASN, and geographical information. |
| 5 | HTTP Headers | `headers.py` | Extracts HTTP response headers from the target website. |
| 6 | SSL Certificate | `ssl_info.py` | Analyzes SSL certificate issuer, validity period, and Subject Alternative Names (SANs). |
| 7 | robots.txt | `robots.py` | Downloads and analyzes the robots.txt file. |
| 8 | sitemap.xml | `sitemap.py` | Parses sitemap.xml and extracts indexed URLs. |
| 9 | Security Headers | `security_headers.py` | Checks CSP, HSTS, XFO, XCTO, Referrer Policy, and other security headers. |
| 10 | Target Intelligence | `target_intelligence.py` | Collects domain, IP, ASN, DNSSEC, and hosting provider information. |
| 11 | DNS Intelligence | `dns_intelligence.py` | Detects SPF, DKIM, DMARC, and wildcard DNS configurations. |
| 12 | Infrastructure Mapping | `infrastructure_mapping.py` | Maps IP addresses, reverse DNS, ASN, ISP, and cloud providers. |
| 13 | HTTP Intelligence | `http_intelligence.py` | Analyzes redirects, HTTP status, compression, and detected technologies. |
| 14 | SSL Intelligence | `ssl_intelligence.py` | Extracts cipher suites, key sizes, protocol versions, and certificate expiration. |
| 15 | Technology Fingerprinting | `technology_fingerprinting.py` | Detects frameworks, CMS platforms, JavaScript libraries, and web technologies. |
| 16 | Crawl Engine | `crawl_engine.py` | Crawls pages to discover URLs, forms, images, endpoints, and email addresses. |
| 17 | JavaScript Analysis | `javascript_analysis.py` | Identifies API endpoints, secrets, JWT tokens, and JavaScript resources. |
| 18 | Directory Enumeration | `directory_enumeration.py` | Discovers common directories and hidden resources. |
| 19 | Security Observations | `security_observations.py` | Detects common security misconfigurations and weaknesses. |
| 20 | Visual Intelligence | `visual_intelligence.py` | Extracts page title, favicon, viewport, Open Graph tags, and metadata. |
| 21 | Page Statistics | `page_statistics.py` | Calculates website statistics, HTTPS ratio, and resource counts. |
| 22 | Domain Relationships | `domain_relationships.py` | Identifies subdomains, shared IPs, and domain relationships. |
| 23 | Report Engine | `report_engine.py` | Generates reports, calculates risk score, and provides recommendations. |

---

# 🚨 Security Findings

The framework categorizes findings based on their severity to help prioritize remediation.

| Severity | Examples |
|----------|----------|
| 🔴 **Critical** | Exposed `.git` repository, exposed `.env` files, directory listing enabled |
| 🟠 **High** | Missing Content Security Policy (CSP), missing HSTS, exposed backup files |
| 🟡 **Medium** | Missing `X-Frame-Options`, missing `X-Content-Type-Options` |
| 🟢 **Low** | Exposed `Server` banner, missing `Referrer-Policy` |

> **Note:** Severity levels are automatically calculated by the Report Engine based on the identified security observations.

---

# 📄 Sample Report Preview

Below is an example of the summary generated after completing a reconnaissance scan.

```text
🔍 Recon Intelligence Report
├── Target: example.com
├── Risk Score: 14/100 (High Risk)
├── Findings: 6 Total
│   ├── 🔴 Critical : 0
│   ├── 🟠 High     : 1
│   ├── 🟡 Medium   : 2
│   └── 🟢 Low      : 3
├── SSL Status: Valid (115 Days Remaining)
├── Security Headers: 2 / 9 Present
└── Technologies: Cloudflare, Bootstrap, React
```

> **Note:** The actual report contains significantly more information, including WHOIS records, DNS analysis, SSL certificate details, HTTP headers, security observations, technology fingerprinting, visual intelligence, and a detailed risk assessment.

---

# 📖 About the Project

The **Web Recon Automation Framework** is a modular and production-ready reconnaissance platform developed to automate the process of collecting publicly available intelligence about a target domain.

Designed for **penetration testers**, **red teamers**, **security researchers**, **SOC analysts**, and **bug bounty hunters**, the framework combines **23 specialized reconnaissance modules** into a single workflow, allowing users to perform comprehensive web reconnaissance with a single command.

The project focuses on speed, scalability, automation, and professional reporting by generating detailed **HTML**, **Markdown**, and **JSON** reports that can be used for security assessments, documentation, or further analysis.

---

# 🏆 Key Achievements

- ✅ Developed **23 modular reconnaissance engines** for comprehensive intelligence gathering.
- ✅ Automated the complete reconnaissance workflow with a **single command**.
- ✅ Generated professional **HTML**, **Markdown**, and **JSON** reports.
- ✅ Implemented automatic **risk scoring** with severity-based categorization.
- ✅ Built a **parallel execution engine** to significantly reduce scan time.
- ✅ Added comprehensive **error handling and logging** for improved reliability.
- ✅ Implemented **technology fingerprinting**, **SSL analysis**, **DNS intelligence**, and **security header analysis**.
- ✅ Designed a scalable architecture, making it easy to add future reconnaissance modules.
- ✅ Organized the project using a clean and modular Python codebase following best practices.
