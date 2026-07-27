#!/usr/bin/env python3
"""
Web Recon Automation Framework - Complete Integration
All 22 modules working together
"""
import sys
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from utils.logger import setup_logger
from utils.validator import validate_target
from utils.helpers import ensure_output_dir
import config

# ============================================================
# IMPORT ALL 22 MODULES
# ============================================================

# CORE MODULES (Original Requirements)
from modules.whois_lookup import get_whois
from modules.dns_lookup import get_dns_records
from modules.ip_lookup import resolve_ip
from modules.geo_lookup import get_geolocation
from modules.headers import fetch_headers
from modules.ssl_info import get_ssl_info
from modules.robots import fetch_robots
from modules.sitemap import fetch_sitemap
from modules.security_headers import analyze_security_headers

# ENHANCED MODULES (Level 2 - Intelligence)
from modules.target_intelligence import get_target_intelligence
from modules.dns_intelligence import get_dns_intelligence
from modules.infrastructure_mapping import get_infrastructure_mapping
from modules.http_intelligence import get_http_intelligence
from modules.ssl_intelligence import get_ssl_intelligence
from modules.technology_fingerprinting import get_technology_fingerprint
from modules.crawl_engine import get_crawl_data
from modules.javascript_analysis import get_javascript_analysis
from modules.directory_enumeration import get_directory_enumeration
from modules.security_observations import get_security_observations
from modules.visual_intelligence import get_visual_intelligence
from modules.page_statistics import get_page_statistics
from modules.domain_relationships import get_domain_relationships
from modules.report_engine import ReportEngine

# REPORT GENERATORS
from reports.html_generator import generate_html_report
from reports.markdown_generator import generate_markdown_report

logger = setup_logger()


def collect_core_data(domain):
    """Collect data from core modules (Original Requirements)"""
    logger.info("Collecting core module data...")
    
    # FIXED: Proper indentation for core_tasks
    core_tasks = {
        'whois': lambda: get_whois(domain),
        'dns': lambda: get_dns_records(domain),
        'ip': lambda: resolve_ip(domain),
        'geo': lambda: get_geolocation(domain),
        'headers': lambda: fetch_headers(f"https://{domain}"),
        'ssl': lambda: get_ssl_info(domain),
        'robots': lambda: fetch_robots(f"https://{domain}/robots.txt"),
        'sitemap': lambda: fetch_sitemap(domain),
    }
    
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_name = {executor.submit(task): name for name, task in core_tasks.items()}
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                results[name] = future.result()
            except Exception as e:
                logger.error(f"Core module {name} failed: {e}")
                results[name] = {"error": str(e)}
    
    # Security headers depend on headers
    headers_result = results.get('headers', {})
    if isinstance(headers_result, dict) and 'error' not in headers_result:
        results['security_headers_analysis'] = analyze_security_headers(headers_result)
    else:
        results['security_headers_analysis'] = {"error": "Headers not available"}
    
    return results


def collect_intelligence_data(domain):
    """Collect data from enhanced modules (Level 2)"""
    logger.info("Collecting intelligence module data...")
    
    intel_tasks = {
        'target': lambda: get_target_intelligence(domain),
        'dns_intel': lambda: get_dns_intelligence(domain),
        'infrastructure': lambda: get_infrastructure_mapping(domain),
        'http_intel': lambda: get_http_intelligence(domain),
        'ssl_intel': lambda: get_ssl_intelligence(domain),
        'tech': lambda: get_technology_fingerprint(domain),
        'crawl': lambda: get_crawl_data(domain, max_urls=30),
        'js': lambda: get_javascript_analysis(domain),
        'directory': lambda: get_directory_enumeration(domain),
        'security': lambda: get_security_observations(domain),
        'visual': lambda: get_visual_intelligence(domain),
        'stats': lambda: get_page_statistics(domain),
        'relationships': lambda: get_domain_relationships(domain),
    }
    
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_name = {executor.submit(task): name for name, task in intel_tasks.items()}
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                results[name] = future.result()
            except Exception as e:
                logger.error(f"Intelligence module {name} failed: {e}")
                results[name] = {"error": str(e)}
    
    return results


def collect_all_data(domain):
    """Collect ALL data from ALL 22 modules"""
    logger.info(f"🚀 Starting comprehensive reconnaissance on {domain}")
    logger.info("=" * 60)
    
    # Collect core data
    core_data = collect_core_data(domain)
    
    # Collect intelligence data
    intel_data = collect_intelligence_data(domain)
    
    # Merge all data
    all_data = {
        'domain': domain,
        'timestamp': datetime.now().isoformat(),
        # Core modules
        'whois': core_data.get('whois', {}),
        'dns_records': core_data.get('dns', {}),
        'ip': core_data.get('ip', {}),
        'geo': core_data.get('geo', {}),
        'http_headers': core_data.get('headers', {}),
        'ssl_cert': core_data.get('ssl', {}),
        'robots': core_data.get('robots', {}),
        'sitemap': core_data.get('sitemap', {}),
        'security_headers': core_data.get('security_headers_analysis', {}),
        # Intelligence modules
        'target_intel': intel_data.get('target', {}),
        'dns_intel': intel_data.get('dns_intel', {}),
        'infrastructure': intel_data.get('infrastructure', {}),
        'http_intel': intel_data.get('http_intel', {}),
        'ssl_intel': intel_data.get('ssl_intel', {}),
        'tech_fingerprint': intel_data.get('tech', {}),
        'crawl_data': intel_data.get('crawl', {}),
        'js_analysis': intel_data.get('js', {}),
        'directory_enum': intel_data.get('directory', {}),
        'security_obs': intel_data.get('security', {}),
        'visual_intel': intel_data.get('visual', {}),
        'page_stats': intel_data.get('stats', {}),
        'domain_relations': intel_data.get('relationships', {}),
    }
    
    # Add summary using ReportEngine
    engine = ReportEngine(all_data)
    all_data['summary'] = engine.generate_summary()
    
    return all_data


def print_summary(data):
    """Print a summary of collected data"""
    summary = data.get('summary', {})
    
    print("\n" + "=" * 60)
    print("📊 RECON SUMMARY")
    print("=" * 60)
    print(f"🌐 Domain: {data.get('domain', 'Unknown')}")
    print(f"📅 Timestamp: {data.get('timestamp', 'Unknown')}")
    print(f"📈 Risk Score: {summary.get('risk_score', 0)}/100")
    print(f"🛡️ Status: {summary.get('overall_status', 'Unknown')}")
    
    risks = summary.get('risks', {})
    print(f"\n🔴 Critical: {risks.get('critical', 0)}")
    print(f"🟠 High: {risks.get('high', 0)}")
    print(f"🟡 Medium: {risks.get('medium', 0)}")
    print(f"🟢 Low: {risks.get('low', 0)}")
    
    # Module status
    modules_status = {
        'WHOIS': data.get('whois', {}).get('error') is None,
        'DNS': data.get('dns_records', {}).get('error') is None,
        'IP': data.get('ip', {}).get('error') is None,
        'Geo': data.get('geo', {}).get('error') is None,
        'Headers': data.get('http_headers', {}).get('error') is None,
        'SSL': data.get('ssl_cert', {}).get('error') is None,
        'Robots': data.get('robots', {}).get('error') is None,
        'Sitemap': data.get('sitemap', {}).get('error') is None,
        'Target Intel': data.get('target_intel', {}).get('error') is None,
        'DNS Intel': data.get('dns_intel', {}).get('error') is None,
        'Infrastructure': data.get('infrastructure', {}).get('error') is None,
        'HTTP Intel': data.get('http_intel', {}).get('error') is None,
        'SSL Intel': data.get('ssl_intel', {}).get('error') is None,
        'Tech Fingerprint': data.get('tech_fingerprint', {}).get('error') is None,
        'Crawl': data.get('crawl_data', {}).get('error') is None,
        'JS Analysis': data.get('js_analysis', {}).get('error') is None,
        'Directory': data.get('directory_enum', {}).get('error') is None,
        'Security Obs': data.get('security_obs', {}).get('error') is None,
        'Visual': data.get('visual_intel', {}).get('error') is None,
        'Page Stats': data.get('page_stats', {}).get('error') is None,
        'Relationships': data.get('domain_relations', {}).get('error') is None,
    }
    
    print("\n📦 Module Status:")
    for name, status in modules_status.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Web Recon Automation Framework - All 22 Modules",
        epilog="Example: python main.py example.com"
    )
    parser.add_argument("target", nargs="?", help="Target domain or URL")
    parser.add_argument("--timeout", type=int, default=config.HTTP_TIMEOUT)
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML report")
    parser.add_argument("--no-md", action="store_true", help="Skip Markdown report")
    parser.add_argument("--no-json", action="store_true", help="Skip JSON report")
    args = parser.parse_args()
    
    # Get target
    target = args.target or input("Enter target domain (e.g., example.com): ").strip()
    if not target:
        print("❌ No target provided.")
        sys.exit(1)
    
    # Validate target
    domain = validate_target(target)
    if not domain:
        print(f"❌ Invalid target: {target}")
        sys.exit(1)
    
    # Ensure output directory
    ensure_output_dir(args.output)
    
    print(f"\n🔍 Starting reconnaissance on {domain}")
    print(f"📁 Output directory: {args.output}")
    print("-" * 60)
    
    # Collect ALL data from ALL 22 modules
    data = collect_all_data(domain)
    
    # Print summary
    print_summary(data)
    
    # Generate reports
    print("\n📄 Generating reports...")
    
    # HTML Report
    if not args.no_html:
        html_path = f"{args.output}/report.html"
        generate_html_report(data, html_path)
        print(f"  ✅ HTML Report: {html_path}")
    
    # Markdown Report
    if not args.no_md:
        md_path = f"{args.output}/report.md"
        generate_markdown_report(data, md_path)
        print(f"  ✅ Markdown Report: {md_path}")
    
    # JSON Report
    if not args.no_json:
        json_path = f"{args.output}/report.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  ✅ JSON Report: {json_path}")
    
    print("\n" + "=" * 60)
    print("✅ Recon complete!")
    print(f"📁 Reports saved to: {args.output}/")
    print("=" * 60)


if __name__ == "__main__":
    main()