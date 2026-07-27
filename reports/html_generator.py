# reports/html_generator.py - Clean version with single PDF download
import os
from jinja2 import Template
import datetime
import json

def generate_html_report(data, output_path):
    """Generate professional HTML report with PDF download button"""
    
    # Extract data with fallbacks for both old and new structure
    domain = data.get('domain', 'Unknown')
    timestamp = data.get('timestamp', datetime.datetime.now().isoformat())
    
    # Core modules (old structure)
    whois = data.get('whois', {})
    dns_records = data.get('dns_records', {})
    ip = data.get('ip', {})
    geo = data.get('geo', {})
    http_headers = data.get('http_headers', {})
    ssl_cert = data.get('ssl_cert', {})
    robots = data.get('robots', {})
    sitemap = data.get('sitemap', {})
    security_headers = data.get('security_headers', {})
    
    # Intelligence modules (new structure)
    target_intel = data.get('target_intel', {})
    dns_intel = data.get('dns_intel', {})
    infrastructure = data.get('infrastructure', {})
    http_intel = data.get('http_intel', {})
    ssl_intel = data.get('ssl_intel', {})
    tech_fingerprint = data.get('tech_fingerprint', {})
    crawl_data = data.get('crawl_data', {})
    js_analysis = data.get('js_analysis', {})
    directory_enum = data.get('directory_enum', {})
    security_obs = data.get('security_obs', {})
    visual_intel = data.get('visual_intel', {})
    page_stats = data.get('page_stats', {})
    domain_relations = data.get('domain_relations', {})
    
    # Summary
    summary = data.get('summary', {})
    risk_score = summary.get('risk_score', 0)
    risk_level = summary.get('overall_status', 'Secure')
    risks = summary.get('risks', {'critical': 0, 'high': 0, 'medium': 0, 'low': 0})
    total_findings = sum(risks.values())
    
    # For backward compatibility - use http_intel if available, else http_headers
    headers_data = http_intel.get('headers', {}) if http_intel.get('headers') else http_headers
    
    # Security headers from both sources
    sec_headers = security_headers.get('checks', {}) if security_headers.get('checks') else http_intel.get('security_headers', {})
    security_headers_present = sum(1 for v in sec_headers.values() if v is not None)
    
    # Get technologies
    technologies = tech_fingerprint.get('technologies', [])
    if not technologies:
        technologies = http_intel.get('technologies', [])
    
    # Get CDN
    cdn_list = tech_fingerprint.get('cdn', [])
    if not cdn_list:
        cdn_list = [http_intel.get('cdn', '')] if http_intel.get('cdn') else []
    
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recon Intelligence Report - {{ domain }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f0f4f8;
            color: #1a202c;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
            overflow: hidden;
            position: relative;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 50px;
            position: relative;
        }
        .header h1 {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .header .subtitle {
            font-size: 16px;
            opacity: 0.9;
        }
        .header .badge-top {
            position: absolute;
            right: 40px;
            top: 40px;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        /* PDF Download Button - SINGLE BUTTON */
        .download-bar {
            background: #f7fafc;
            padding: 12px 50px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        .download-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            font-family: 'Inter', sans-serif;
        }
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .download-btn svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
        }
        .download-info {
            font-size: 13px;
            color: #718096;
        }
        
        .risk-section {
            padding: 30px 50px;
            background: #f7fafc;
            border-bottom: 1px solid #e2e8f0;
        }
        .risk-grid {
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 30px;
            align-items: center;
        }
        .risk-score {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            text-align: center;
            min-width: 150px;
        }
        .risk-score .score {
            font-size: 42px;
            font-weight: 700;
        }
        .risk-score .label {
            font-size: 12px;
            opacity: 0.8;
        }
        .risk-status .badge {
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 600;
        }
        .badge-critical { background: #fed7d7; color: #9b2c2c; }
        .badge-high { background: #feb2b2; color: #9b2c2c; }
        .badge-medium { background: #fefcbf; color: #975a16; }
        .badge-low { background: #fefcbf; color: #975a16; }
        .badge-secure { background: #c6f6d5; color: #276749; }
        .content { padding: 30px 50px; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #e2e8f0;
            margin-bottom: 24px;
            transition: all 0.3s ease;
        }
        .card:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }
        .card-header {
            font-size: 20px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .card-header .icon { font-size: 28px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
        .grid-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; }
        .table-wrap { overflow-x: auto; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        th {
            background: #f7fafc;
            color: #4a5568;
            font-weight: 600;
            padding: 10px 12px;
            text-align: left;
            border-bottom: 2px solid #e2e8f0;
        }
        td {
            padding: 8px 12px;
            border-bottom: 1px solid #edf2f7;
        }
        tr:hover td { background: #f7fafc; }
        .value-missing { color: #e53e3e; font-weight: 500; }
        .value-present { color: #38a169; font-weight: 500; }
        .tech-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            background: #bee3f8;
            color: #2b6cb0;
            margin: 3px 4px 3px 0;
        }
        .tech-tag.cdn { background: #fbd38d; color: #975a16; }
        .tech-tag.server { background: #feb2b2; color: #9b2c2c; }
        .tech-tag.framework { background: #c6f6d5; color: #276749; }
        .finding-critical { border-left: 4px solid #e53e3e; padding-left: 12px; margin: 6px 0; }
        .finding-high { border-left: 4px solid #ed8936; padding-left: 12px; margin: 6px 0; }
        .finding-medium { border-left: 4px solid #ecc94b; padding-left: 12px; margin: 6px 0; }
        .finding-low { border-left: 4px solid #48bb78; padding-left: 12px; margin: 6px 0; }
        .stat-box {
            background: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-box .number {
            font-size: 28px;
            font-weight: 700;
            color: #2d3748;
        }
        .stat-box .label {
            font-size: 12px;
            color: #718096;
        }
        .footer {
            background: #f7fafc;
            padding: 20px 40px;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 14px;
            text-align: center;
        }
        details { margin-top: 10px; }
        summary {
            cursor: pointer;
            font-weight: 500;
            color: #667eea;
            padding: 8px;
            background: #f7fafc;
            border-radius: 6px;
        }
        summary:hover { background: #edf2f7; }
        
        /* Print styles for PDF - HIDE download bar */
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; border-radius: 0; }
            .download-bar { display: none !important; }
            .card:hover { box-shadow: none; border-color: #e2e8f0; }
            .card { break-inside: avoid; page-break-inside: avoid; }
            .header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .risk-score { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .badge { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            /* Hide file path that might appear */
            .file-path { display: none !important; }
        }
        
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
            .risk-grid { grid-template-columns: 1fr; text-align: center; }
            .header { padding: 30px 20px; }
            .content { padding: 20px; }
            .header .badge-top { position: static; margin-top: 10px; display: inline-block; }
            .download-bar { padding: 12px 20px; justify-content: center; }
        }
    </style>
</head>
<body>
<div class="container">
    <!-- Header - Clean, no file path -->
    <div class="header">
        <h1>🔍 Recon Intelligence Report</h1>
        <div class="subtitle">{{ domain }} · {{ timestamp }}</div>
        <div class="badge-top">Web Recon Automation Framework</div>
    </div>
    
    <!-- Download Bar - SINGLE BUTTON ONLY -->
    <div class="download-bar">
        <span class="download-info">📄 Download PDF Report</span>
        <button class="download-btn" onclick="downloadPDF()">
            <svg viewBox="0 0 24 24"><path d="M14,2H6A2,2,0,0,0,4,4V20a2,2,0,0,0,2,2H18a2,2,0,0,0,2-2V8ZM12,18,8,14h2.5V10h3v4H16ZM13,9V3.5L18.5,9Z"/></svg>
            Download PDF
        </button>
    </div>
    
    <!-- Risk Section -->
    <div class="risk-section">
        <div class="risk-grid">
            <div class="risk-score">
                <div class="score">{{ risk_score }}</div>
                <div class="label">Risk Score / 100</div>
            </div>
            <div class="risk-status">
                <span class="badge badge-{{ risk_level|lower }}">{{ risk_level }}</span>
                <div style="margin-top: 8px; font-size: 14px; color: #718096;">
                    {{ total_findings }} findings detected
                </div>
            </div>
            <div style="font-size: 14px; color: #718096;">
                <div>🔴 Critical: {{ risks.critical }}</div>
                <div>🟠 High: {{ risks.high }}</div>
                <div>🟡 Medium: {{ risks.medium }}</div>
                <div>🟢 Low: {{ risks.low }}</div>
            </div>
        </div>
    </div>
    
    <!-- Content -->
    <div class="content">
        <!-- Quick Stats -->
        <div class="grid-4" style="margin-bottom: 24px;">
            <div class="stat-box">
                <div class="number">{{ http_intel.status_code if http_intel else 'N/A' }}</div>
                <div class="label">HTTP Status</div>
            </div>
            <div class="stat-box">
                <div class="number">{{ dns_intel.A|length if dns_intel.A else 0 }}</div>
                <div class="label">A Records</div>
            </div>
            <div class="stat-box">
                <div class="number">{{ ssl_intel.days_remaining|default('N/A') }}</div>
                <div class="label">SSL Days Left</div>
            </div>
            <div class="stat-box">
                <div class="number">{{ technologies|length }}</div>
                <div class="label">Technologies</div>
            </div>
        </div>
        
        <!-- Target Intelligence -->
        <div class="card">
            <div class="card-header"><span class="icon">🎯</span> Target Intelligence</div>
            <div class="grid-2">
                <div>
                    <table>
                        <tr><td><strong>Domain</strong></td><td>{{ target_intel.domain or domain }}</td></tr>
                        <tr><td><strong>Registered Domain</strong></td><td>{{ target_intel.registered_domain or 'N/A' }}</td></tr>
                        <tr><td><strong>Hostname</strong></td><td>{{ target_intel.hostname or 'N/A' }}</td></tr>
                        <tr><td><strong>FQDN</strong></td><td>{{ target_intel.fqdn or domain }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>Registrar</strong></td><td>{{ whois.registrar or 'N/A' }}</td></tr>
                        <tr><td><strong>DNSSEC</strong></td><td>{{ target_intel.dnssec or 'Unknown' }}</td></tr>
                        <tr><td><strong>Registrant</strong></td><td>{{ whois.registrant_organization or 'N/A' }}</td></tr>
                        <tr><td><strong>Reverse DNS</strong></td><td>{{ target_intel.reverse_dns or 'N/A' }}</td></tr>
                    </table>
                </div>
            </div>
            <div style="margin-top: 12px;">
                <strong>IP Addresses:</strong>
                {% if target_intel.ipv4 %}
                <div>IPv4: {{ target_intel.ipv4|join(', ') }}</div>
                {% endif %}
                {% if target_intel.ipv6 %}
                <div>IPv6: {{ target_intel.ipv6|join(', ') }}</div>
                {% endif %}
            </div>
        </div>
        
        <!-- DNS Records -->
        <div class="card">
            <div class="card-header"><span class="icon">🌐</span> DNS Records</div>
            <div class="grid-3">
                <div>
                    <table>
                        <tr><td><strong>DNSSEC</strong></td><td>{{ '✅ Yes' if dns_intel.dnssec else '❌ No' }}</td></tr>
                        <tr><td><strong>Wildcard DNS</strong></td><td>{{ '✅ Yes' if dns_intel.wildcard_dns else '❌ No' }}</td></tr>
                        <tr><td><strong>DNS Leaks</strong></td><td>{{ dns_intel.dns_leaks or 'None detected' }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>SPF</strong></td><td>{{ '✅ Found' if dns_intel.spf else '❌ Not Found' }}</td></tr>
                        <tr><td><strong>DMARC</strong></td><td>{{ '✅ Found' if dns_intel.dmarc else '❌ Not Found' }}</td></tr>
                        <tr><td><strong>DKIM</strong></td><td>{{ '✅ Found' if dns_intel.dkim else '❌ Not Found' }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>MX Records</strong></td><td>{{ dns_intel.MX|length if dns_intel.MX else 0 }}</td></tr>
                        <tr><td><strong>NS Records</strong></td><td>{{ dns_intel.NS|length if dns_intel.NS else 0 }}</td></tr>
                        <tr><td><strong>A Records</strong></td><td>{{ dns_intel.A|length if dns_intel.A else 0 }}</td></tr>
                    </table>
                </div>
            </div>
            <details>
                <summary>📋 View All DNS Records</summary>
                <div style="margin-top: 10px;">
                    {% if dns_intel.A %}<div><strong>A:</strong> {{ dns_intel.A|join(', ') }}</div>{% endif %}
                    {% if dns_intel.AAAA %}<div><strong>AAAA:</strong> {{ dns_intel.AAAA|join(', ') }}</div>{% endif %}
                    {% if dns_intel.MX %}<div><strong>MX:</strong> {{ dns_intel.MX|join(', ') }}</div>{% endif %}
                    {% if dns_intel.NS %}<div><strong>NS:</strong> {{ dns_intel.NS|join(', ') }}</div>{% endif %}
                    {% if dns_intel.TXT %}<div><strong>TXT:</strong> {{ dns_intel.TXT|join(', ') }}</div>{% endif %}
                    {% if dns_intel.SOA %}<div><strong>SOA:</strong> {{ dns_intel.SOA|join(', ') }}</div>{% endif %}
                </div>
            </details>
        </div>
        
        <!-- Infrastructure & Geolocation -->
        <div class="card">
            <div class="card-header"><span class="icon">🏗️</span> Infrastructure & Geolocation</div>
            <div class="grid-2">
                <div>
                    <table>
                        <tr><td><strong>IP Address</strong></td><td>{{ infrastructure.ip or 'N/A' }}</td></tr>
                        <tr><td><strong>ASN</strong></td><td>{{ infrastructure.asn or 'N/A' }}</td></tr>
                        <tr><td><strong>ASN Name</strong></td><td>{{ infrastructure.asn_name or 'N/A' }}</td></tr>
                        <tr><td><strong>ISP</strong></td><td>{{ infrastructure.isp or 'N/A' }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>Country</strong></td><td>{{ infrastructure.country or geo.country or 'N/A' }}</td></tr>
                        <tr><td><strong>Region</strong></td><td>{{ infrastructure.region or geo.region or 'N/A' }}</td></tr>
                        <tr><td><strong>City</strong></td><td>{{ infrastructure.city or geo.city or 'N/A' }}</td></tr>
                        <tr><td><strong>Cloud Provider</strong></td><td>{{ infrastructure.cloud_provider or 'Unknown' }}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- HTTP Headers -->
        <div class="card">
            <div class="card-header"><span class="icon">📡</span> HTTP Headers</div>
            <div class="table-wrap">
                <table>
                    <tr><th>Header</th><th>Value</th></tr>
                    {% if headers_data %}
                    {% for key, value in headers_data.items() %}
                    <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                    {% endfor %}
                    {% else %}
                    <tr><td colspan="2">No headers available</td></tr>
                    {% endif %}
                </table>
            </div>
        </div>
        
        <!-- SSL Certificate -->
        <div class="card">
            <div class="card-header"><span class="icon">🔐</span> SSL/TLS Certificate</div>
            <div class="grid-2">
                <div>
                    <table>
                        <tr><td><strong>Issuer</strong></td><td>{{ ssl_intel.issuer or ssl_cert.issuer or 'N/A' }}</td></tr>
                        <tr><td><strong>Subject</strong></td><td>{{ ssl_intel.subject or ssl_cert.subject or 'N/A' }}</td></tr>
                        <tr><td><strong>Common Name</strong></td><td>{{ ssl_intel.common_name or 'N/A' }}</td></tr>
                        <tr><td><strong>Organization</strong></td><td>{{ ssl_intel.organization or 'N/A' }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>Valid From</strong></td><td>{{ ssl_intel.not_before or ssl_cert.valid_from or 'N/A' }}</td></tr>
                        <tr><td><strong>Valid To</strong></td><td>{{ ssl_intel.not_after or ssl_cert.valid_to or 'N/A' }}</td></tr>
                        <tr><td><strong>Days Remaining</strong></td><td>{{ ssl_intel.days_remaining or 'N/A' }} days</td></tr>
                        <tr><td><strong>Wildcard</strong></td><td>{{ '✅ Yes' if ssl_intel.wildcard else '❌ No' }}</td></tr>
                    </table>
                </div>
            </div>
            {% if ssl_intel.sans %}
            <div style="margin-top: 10px;"><strong>Subject Alternative Names:</strong> {{ ssl_intel.sans|join(', ') }}</div>
            {% endif %}
        </div>
        
        <!-- robots.txt -->
        <div class="card">
            <div class="card-header"><span class="icon">🤖</span> robots.txt</div>
            {% if robots.status %}
            <p><strong>Status:</strong> {{ robots.status }}</p>
            <p><strong>Last Modified:</strong> {{ robots.last_modified or 'N/A' }}</p>
            <details>
                <summary>📄 View Content</summary>
                <pre style="background: #f7fafc; padding: 15px; border-radius: 6px; overflow-x: auto; margin-top: 10px; font-size: 13px;">{{ robots.content }}</pre>
            </details>
            {% else %}
            <p>No robots.txt found or inaccessible</p>
            {% endif %}
        </div>
        
        <!-- sitemap.xml -->
        <div class="card">
            <div class="card-header"><span class="icon">🗺️</span> sitemap.xml</div>
            {% if sitemap.url_count %}
            <p><strong>URL Count:</strong> {{ sitemap.url_count }}</p>
            <p><strong>First URLs:</strong></p>
            <ul>
                {% for url in sitemap.first_urls %}
                <li>{{ url }}</li>
                {% endfor %}
            </ul>
            {% else %}
            <p>{{ sitemap.error or 'No sitemap.xml found' }}</p>
            {% endif %}
        </div>
        
        <!-- Technologies -->
        <div class="card">
            <div class="card-header"><span class="icon">⚙️</span> Technologies Detected</div>
            <div>
                {% if http_intel.server_banner %}
                <div><strong>Server:</strong> <span class="tech-tag server">{{ http_intel.server_banner }}</span></div>
                {% endif %}
                {% if technologies %}
                <div><strong>Technologies:</strong> 
                    {% for t in technologies %}<span class="tech-tag">{{ t }}</span>{% endfor %}
                </div>
                {% endif %}
                {% if cdn_list %}
                <div><strong>CDN:</strong> 
                    {% for c in cdn_list %}<span class="tech-tag cdn">{{ c }}</span>{% endfor %}
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Security Findings -->
        <div class="card" style="border-color: #fc8181;">
            <div class="card-header"><span class="icon">🛡️</span> Security Findings</div>
            {% if security_obs.critical %}
            <div><strong style="color: #e53e3e;">🔴 Critical:</strong></div>
            {% for finding in security_obs.critical %}
            <div class="finding-critical">{{ finding }}</div>
            {% endfor %}
            {% endif %}
            {% if security_obs.high %}
            <div><strong style="color: #ed8936;">🟠 High:</strong></div>
            {% for finding in security_obs.high %}
            <div class="finding-high">{{ finding }}</div>
            {% endfor %}
            {% endif %}
            {% if security_obs.medium %}
            <div><strong style="color: #ecc94b;">🟡 Medium:</strong></div>
            {% for finding in security_obs.medium %}
            <div class="finding-medium">{{ finding }}</div>
            {% endfor %}
            {% endif %}
            {% if security_obs.low %}
            <div><strong style="color: #48bb78;">🟢 Low:</strong></div>
            {% for finding in security_obs.low %}
            <div class="finding-low">{{ finding }}</div>
            {% endfor %}
            {% endif %}
            {% if not security_obs.critical and not security_obs.high and not security_obs.medium and not security_obs.low %}
            <div style="color: #38a169;">✅ No security findings detected</div>
            {% endif %}
        </div>
        
        <!-- Page Statistics -->
        <div class="card">
            <div class="card-header"><span class="icon">📊</span> Page Statistics</div>
            <div class="grid-3">
                <div>
                    <table>
                        <tr><td><strong>Status</strong></td><td>{{ page_stats.status_code or 'N/A' }}</td></tr>
                        <tr><td><strong>Redirects</strong></td><td>{{ page_stats.redirects or 0 }}</td></tr>
                        <tr><td><strong>Transfer Size</strong></td><td>{{ page_stats.transfer_size or 0 }} bytes</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>JS Files</strong></td><td>{{ page_stats.js_files or 0 }}</td></tr>
                        <tr><td><strong>CSS Files</strong></td><td>{{ page_stats.css_files or 0 }}</td></tr>
                        <tr><td><strong>Images</strong></td><td>{{ page_stats.images or 0 }}</td></tr>
                    </table>
                </div>
                <div>
                    <table>
                        <tr><td><strong>HTTPS %</strong></td><td>{{ page_stats.https_percent or 0 }}%</td></tr>
                        <tr><td><strong>HTTP %</strong></td><td>{{ page_stats.http_percent or 0 }}%</td></tr>
                        <tr><td><strong>Domains</strong></td><td>{{ page_stats.domains or 0 }}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Directories Found -->
        {% if directory_enum.found %}
        <div class="card">
            <div class="card-header"><span class="icon">📁</span> Directories Found</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                {% for dir in directory_enum.found %}
                <span class="tech-tag">{{ dir }}</span>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <!-- Crawl Data -->
        {% if crawl_data.links %}
        <div class="card">
            <div class="card-header"><span class="icon">🔗</span> Crawl Data</div>
            <div class="grid-2">
                <div>
                    <strong>Internal Links:</strong> 
                    {% if crawl_data.links.internal %}
                        {{ crawl_data.links.internal|length if crawl_data.links.internal is iterable else 0 }}
                    {% else %}0{% endif %}
                    <details>
                        <summary style="cursor: pointer; color: #667eea;">Show</summary>
                        <div style="max-height: 200px; overflow-y: auto; font-size: 13px;">
                            {% if crawl_data.links.internal %}
                                {% for link in crawl_data.links.internal|list %}
                                    {% if loop.index <= 20 %}
                                    <div>{{ link }}</div>
                                    {% endif %}
                                {% endfor %}
                            {% endif %}
                        </div>
                    </details>
                </div>
                <div>
                    <strong>External Links:</strong>
                    {% if crawl_data.links.external %}
                        {{ crawl_data.links.external|length if crawl_data.links.external is iterable else 0 }}
                    {% else %}0{% endif %}
                    <details>
                        <summary style="cursor: pointer; color: #667eea;">Show</summary>
                        <div style="max-height: 200px; overflow-y: auto; font-size: 13px;">
                            {% if crawl_data.links.external %}
                                {% for link in crawl_data.links.external|list %}
                                    {% if loop.index <= 20 %}
                                    <div>{{ link }}</div>
                                    {% endif %}
                                {% endfor %}
                            {% endif %}
                        </div>
                    </details>
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Security Headers Analysis -->
        <div class="card">
            <div class="card-header"><span class="icon">🔒</span> Security Headers Analysis</div>
            <div class="table-wrap">
                <table>
                    <tr><th>Header</th><th>Status</th></tr>
                    {% if sec_headers %}
                    {% for header, value in sec_headers.items() %}
                    <tr>
                        <td>{{ header }}</td>
                        <td class="{{ 'value-present' if value else 'value-missing' }}">
                            {{ '✅ Present' if value else '❌ Missing' }}
                        </td>
                    </tr>
                    {% endfor %}
                    {% else %}
                    <tr><td colspan="2">No security headers data available</td></tr>
                    {% endif %}
                </table>
            </div>
        </div>
        
        <!-- Executive Summary -->
        <div class="card" style="background: #ebf8ff; border-color: #bee3f8;">
            <div class="card-header"><span class="icon">📋</span> Executive Summary</div>
            <div style="font-size: 15px; line-height: 1.8;">
                <p><strong>Target:</strong> {{ domain }}</p>
                <p><strong>Risk Score:</strong> {{ risk_score }}/100 - <span class="badge badge-{{ risk_level|lower }}">{{ risk_level }}</span></p>
                <p><strong>Findings:</strong> {{ total_findings }} total</p>
                <p><strong>SSL Status:</strong> {% if ssl_intel.days_remaining and ssl_intel.days_remaining > 0 %}Valid for {{ ssl_intel.days_remaining }} days{% else %}⚠️ Expired or missing{% endif %}</p>
                <p><strong>Security Headers:</strong> {{ security_headers_present }}/{{ sec_headers|length }} present</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        Generated by Web Recon Automation Framework &bull; {{ timestamp }}
    </div>
</div>

<!-- JavaScript for PDF Download - SINGLE FUNCTION -->
<script>
function downloadPDF() {
    // Trigger browser print dialog with PDF option
    window.print();
}

// Keyboard shortcut: Ctrl+P
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        // Let browser handle print
        return true;
    }
});
</script>

</body>
</html>
    """
    
    template = Template(html_template)
    html = template.render(
        domain=domain,
        timestamp=timestamp,
        # Core data
        whois=whois,
        dns_records=dns_records,
        ip=ip,
        geo=geo,
        http_headers=http_headers,
        ssl_cert=ssl_cert,
        robots=robots,
        sitemap=sitemap,
        security_headers=security_headers,
        # Intelligence data
        target_intel=target_intel,
        dns_intel=dns_intel,
        infrastructure=infrastructure,
        http_intel=http_intel,
        ssl_intel=ssl_intel,
        tech_fingerprint=tech_fingerprint,
        crawl_data=crawl_data,
        js_analysis=js_analysis,
        directory_enum=directory_enum,
        security_obs=security_obs,
        visual_intel=visual_intel,
        page_stats=page_stats,
        domain_relations=domain_relations,
        # Summary
        risk_score=risk_score,
        risk_level=risk_level,
        risks=risks,
        total_findings=total_findings,
        security_headers_present=security_headers_present,
        # Derived
        headers_data=headers_data,
        technologies=technologies,
        cdn_list=cdn_list,
        sec_headers=sec_headers,
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path