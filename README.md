# 🔍 Web Recon Automation Framework

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Modules-23-orange?style=for-the-badge" alt="Modules">
</p>

## 📌 Overview

**Web Recon Automation Framework** is an advanced, modular, and production-ready reconnaissance platform that automates the entire process of gathering public intelligence about a target domain. With **23 specialized modules**, it collects everything from WHOIS information to security headers, and compiles it into a professional, client-ready report with a single command.

This framework is designed for penetration testers, red teamers, security engineers, and bug bounty hunters who need fast, reliable, and repeatable reconnaissance.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **23 Specialized Modules** | Each module handles a specific reconnaissance task |
| ⚡ **Parallel Execution** | Modules run concurrently for maximum speed |
| 🛡️ **Error Resilience** | Logs errors and continues - never crashes |
| 📊 **Professional Reports** | HTML, Markdown, and JSON formats |
| 📈 **Risk Scoring** | Automatic risk assessment with color-coded severity |
| 🔒 **Security Analysis** | CSP, HSTS, XFO, and 6+ other security headers |
| 🌐 **Crawl Engine** | Like Katana - extracts URLs, endpoints, forms, emails |
| 🔍 **Tech Fingerprinting** | Detects frameworks, libraries, and CMS |
| 📱 **Visual Intelligence** | Page title, favicon, viewport, meta tags |

---

## 🏗️ Architecture

The framework follows a **modular architecture** where each module is independent and responsible for a single task.
web_recon_framework/
├── main.py # Orchestrator - runs all modules
├── config.py # Configuration settings
├── modules/ # 23 Intelligence Modules
│ ├── whois_lookup.py # 1. WHOIS Information
│ ├── dns_lookup.py # 2. DNS Records
│ ├── ip_lookup.py # 3. IP Address
│ ├── geo_lookup.py # 4. Geolocation
│ ├── headers.py # 5. HTTP Headers
│ ├── ssl_info.py # 6. SSL Certificate
│ ├── robots.py # 7. robots.txt
│ ├── sitemap.py # 8. sitemap.xml
│ ├── security_headers.py # 9. Security Headers
│ ├── target_intelligence.py # 10. Target Intelligence
│ ├── dns_intelligence.py # 11. DNS Intelligence
│ ├── infrastructure_mapping.py # 12. Infrastructure
│ ├── http_intelligence.py # 13. HTTP Intelligence
│ ├── ssl_intelligence.py # 14. SSL Intelligence
│ ├── technology_fingerprinting.py # 15. Tech Fingerprinting
│ ├── crawl_engine.py # 16. Crawl Engine
│ ├── javascript_analysis.py # 17. JS Analysis
│ ├── directory_enumeration.py # 18. Directory Enumeration
│ ├── security_observations.py # 19. Security Observations
│ ├── visual_intelligence.py # 20. Visual Intelligence
│ ├── page_statistics.py # 21. Page Statistics
│ ├── domain_relationships.py # 22. Domain Relationships
│ └── report_engine.py # 23. Report Engine
├── reports/ # Report Generators
│ ├── html_generator.py # Professional HTML report
│ └── markdown_generator.py # Markdown report
├── utils/ # Helper Utilities
│ ├── logger.py # Logging setup
│ ├── validator.py # Input validation
│ └── helpers.py # Common helper functions
└── output/ # Generated Reports
├── report.html
├── report.md
└── report.json



---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/venkatsaikrishna369/web_recon_framework.git
cd web_recon_framework

Step 2: Create Virtual Environment (Recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
