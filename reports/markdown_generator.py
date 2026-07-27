# reports/markdown_generator.py
import datetime

def generate_markdown_report(data, output_path):
    """Generate professional Markdown report"""
    
    target = data.get('target', {})
    dns = data.get('dns', {})
    infrastructure = data.get('infrastructure', {})
    http = data.get('http', {})
    ssl = data.get('ssl', {})
    tech = data.get('tech', {})
    robots = data.get('robots', {})
    sitemap = data.get('sitemap', {})
    security = data.get('security', {})
    stats = data.get('stats', {})
    
    # Get risk info
    risk_score = security.get('risk_score', 0)
    risk_level = security.get('risk_level', 'Secure')
    findings = {
        'critical': len(security.get('critical', [])),
        'high': len(security.get('high', [])),
        'medium': len(security.get('medium', [])),
        'low': len(security.get('low', []))
    }
    total_findings = sum(findings.values())
    
    lines = []
    lines.append(f"# 🔍 Recon Intelligence Report - {data.get('domain', 'Unknown')}")
    lines.append(f"**Generated:** {data.get('timestamp', datetime.datetime.now().isoformat())}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Executive Summary
    lines.append("## 📋 Executive Summary")
    lines.append(f"- **Target:** {data.get('domain', 'Unknown')}")
    lines.append(f"- **Risk Score:** {risk_score}/100 - **{risk_level}**")
    lines.append(f"- **Total Findings:** {total_findings}")
    lines.append(f"  - 🔴 Critical: {findings['critical']}")
    lines.append(f"  - 🟠 High: {findings['high']}")
    lines.append(f"  - 🟡 Medium: {findings['medium']}")
    lines.append(f"  - 🟢 Low: {findings['low']}")
    lines.append("")
    
    # Target Intelligence
    lines.append("## 🎯 Target Intelligence")
    lines.append(f"- **Domain:** {target.get('domain', 'N/A')}")
    lines.append(f"- **Registered Domain:** {target.get('registered_domain', 'N/A')}")
    lines.append(f"- **Hostname:** {target.get('hostname', 'N/A')}")
    lines.append(f"- **FQDN:** {target.get('fqdn', 'N/A')}")
    lines.append(f"- **Registrar:** {target.get('registrar', 'N/A')}")
    lines.append(f"- **DNSSEC:** {target.get('dnssec', 'N/A')}")
    lines.append(f"- **Registrant:** {target.get('registrant_organization', 'N/A')}")
    lines.append(f"- **Reverse DNS:** {target.get('reverse_dns', 'N/A')}")
    lines.append("")
    
    # IP Addresses
    lines.append("### IP Addresses")
    if target.get('ipv4'):
        lines.append(f"- **IPv4:** {', '.join(target.get('ipv4', []))}")
    if target.get('ipv6'):
        lines.append(f"- **IPv6:** {', '.join(target.get('ipv6', []))}")
    lines.append("")
    
    # DNS
    lines.append("## 🌐 DNS Intelligence")
    lines.append(f"- **DNSSEC:** {'✅ Yes' if dns.get('dnssec') else '❌ No'}")
    lines.append(f"- **Wildcard DNS:** {'✅ Yes' if dns.get('wildcard_dns') else '❌ No'}")
    lines.append(f"- **DNS Leaks:** {dns.get('dns_leaks', 'N/A')}")
    lines.append(f"- **SPF:** {'✅ Found' if dns.get('spf') else '❌ Not Found'}")
    lines.append(f"- **DMARC:** {'✅ Found' if dns.get('dmarc') else '❌ Not Found'}")
    lines.append(f"- **DKIM:** {'✅ Found' if dns.get('dkim') else '❌ Not Found'}")
    lines.append("")
    
    lines.append("### DNS Records")
    for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
        records = dns.get(record_type, [])
        if records:
            lines.append(f"- **{record_type}:** {', '.join(str(r) for r in records[:5])}")
    lines.append("")
    
    # Infrastructure
    lines.append("## 🏗️ Infrastructure & Geolocation")
    lines.append(f"- **IP Address:** {infrastructure.get('ip', 'N/A')}")
    lines.append(f"- **ASN:** {infrastructure.get('asn', 'N/A')}")
    lines.append(f"- **ASN Name:** {infrastructure.get('asn_name', 'N/A')}")
    lines.append(f"- **ISP:** {infrastructure.get('isp', 'N/A')}")
    lines.append(f"- **Country:** {infrastructure.get('country', 'N/A')}")
    lines.append(f"- **Region:** {infrastructure.get('region', 'N/A')}")
    lines.append(f"- **City:** {infrastructure.get('city', 'N/A')}")
    lines.append(f"- **Cloud Provider:** {infrastructure.get('cloud_provider', 'N/A')}")
    lines.append("")
    
    # HTTP
    lines.append("## 🌍 HTTP Intelligence")
    lines.append(f"- **Status Code:** {http.get('status_code', 'N/A')}")
    lines.append(f"- **Server Banner:** {http.get('server_banner', 'N/A')}")
    lines.append(f"- **CDN:** {http.get('cdn', 'N/A')}")
    lines.append(f"- **Compression:** {http.get('compression', 'N/A')}")
    lines.append(f"- **Content Type:** {http.get('content_type', 'N/A')}")
    lines.append("")
    
    # SSL
    lines.append("## 🔐 SSL/TLS Certificate")
    lines.append(f"- **Issuer:** {ssl.get('issuer', 'N/A')}")
    lines.append(f"- **Subject:** {ssl.get('subject', 'N/A')}")
    lines.append(f"- **Common Name:** {ssl.get('common_name', 'N/A')}")
    lines.append(f"- **Valid From:** {ssl.get('not_before', 'N/A')}")
    lines.append(f"- **Valid To:** {ssl.get('not_after', 'N/A')}")
    lines.append(f"- **Days Remaining:** {ssl.get('days_remaining', 'N/A')} days")
    lines.append(f"- **Wildcard:** {'✅ Yes' if ssl.get('wildcard') else '❌ No'}")
    if ssl.get('sans'):
        lines.append(f"- **SANs:** {', '.join(ssl.get('sans', []))}")
    lines.append("")
    
    # robots.txt
    lines.append("## 🤖 robots.txt")
    if robots.get('status'):
        lines.append(f"- **Status:** {robots.get('status')}")
        lines.append(f"- **Last Modified:** {robots.get('last_modified', 'N/A')}")
        lines.append("```")
        lines.append(robots.get('content', '')[:500])
        lines.append("```")
    else:
        lines.append("No robots.txt found")
    lines.append("")
    
    # sitemap
    lines.append("## 🗺️ sitemap.xml")
    if sitemap.get('url_count'):
        lines.append(f"- **URL Count:** {sitemap.get('url_count')}")
        lines.append("- **First URLs:**")
        for url in sitemap.get('first_urls', []):
            lines.append(f"  - {url}")
    else:
        lines.append(f"**Status:** {sitemap.get('error', 'Not found')}")
    lines.append("")
    
    # Technologies
    lines.append("## ⚙️ Technologies Detected")
    if tech.get('servers'):
        lines.append(f"- **Servers:** {', '.join(tech.get('servers', []))}")
    if tech.get('frameworks'):
        lines.append(f"- **Frameworks:** {', '.join(tech.get('frameworks', []))}")
    if tech.get('cdn'):
        lines.append(f"- **CDN:** {', '.join(tech.get('cdn', []))}")
    if tech.get('languages'):
        lines.append(f"- **Languages:** {', '.join(tech.get('languages', []))}")
    if tech.get('cms'):
        lines.append(f"- **CMS:** {', '.join(tech.get('cms', []))}")
    lines.append("")
    
    # Security Findings
    lines.append("## 🛡️ Security Findings")
    if security.get('critical'):
        lines.append("### 🔴 Critical")
        for finding in security.get('critical', []):
            lines.append(f"- {finding}")
    if security.get('high'):
        lines.append("### 🟠 High")
        for finding in security.get('high', []):
            lines.append(f"- {finding}")
    if security.get('medium'):
        lines.append("### 🟡 Medium")
        for finding in security.get('medium', []):
            lines.append(f"- {finding}")
    if security.get('low'):
        lines.append("### 🟢 Low")
        for finding in security.get('low', []):
            lines.append(f"- {finding}")
    lines.append("")
    
    # Statistics
    lines.append("## 📊 Page Statistics")
    lines.append(f"- **Status Code:** {stats.get('status_code', 'N/A')}")
    lines.append(f"- **Redirects:** {stats.get('redirects', 0)}")
    lines.append(f"- **Transfer Size:** {stats.get('transfer_size', 0)} bytes")
    lines.append(f"- **JS Files:** {stats.get('js_files', 0)}")
    lines.append(f"- **CSS Files:** {stats.get('css_files', 0)}")
    lines.append(f"- **Images:** {stats.get('images', 0)}")
    lines.append(f"- **HTTPS %:** {stats.get('https_percent', 0)}%")
    lines.append(f"- **HTTP %:** {stats.get('http_percent', 0)}%")
    lines.append(f"- **Domains:** {stats.get('domains', 0)}")
    lines.append("")
    
    # Directories
    if data.get('directory', {}).get('found'):
        lines.append("## 📁 Directories Found")
        for dir_path in data.get('directory', {}).get('found', []):
            lines.append(f"- {dir_path}")
        lines.append("")
    
    # HTTP Headers
    lines.append("## 📡 HTTP Headers")
    if http.get('headers'):
        for key, value in http['headers'].items():
            lines.append(f"- **{key}:** {value}")
    lines.append("")
    
    # Security Headers Analysis
    lines.append("## 🔒 Security Headers Analysis")
    security_headers = http.get('security_headers', {})
    for header, value in security_headers.items():
        status = '✅ Present' if value else '❌ Missing'
        lines.append(f"- **{header}:** {status}")
    lines.append("")
    
    lines.append("---")
    lines.append(f"_Generated by Web Recon Automation Framework on {data.get('timestamp', datetime.datetime.now().isoformat())}_")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return output_path