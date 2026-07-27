# modules/report_engine.py
import json
from datetime import datetime
from utils.logger import get_logger
import os

logger = get_logger()


class ReportEngine:
    """Professional report generation with risk scoring"""
    
    def __init__(self, data):
        self.data = data
        self.domain = data.get('domain', 'Unknown')
        self.timestamp = datetime.now().isoformat()
    
    def generate_summary(self):
        """Generate executive summary"""
        security = self.data.get('security_obs', {})
        risks = {
            'critical': len(security.get('critical', [])),
            'high': len(security.get('high', [])),
            'medium': len(security.get('medium', [])),
            'low': len(security.get('low', []))
        }
        
        summary = {
            'domain': self.domain,
            'timestamp': self.timestamp,
            'risk_score': self.calculate_risk_score(risks),
            'risks': risks,
            'overall_status': self.get_overall_status(risks),
            'recommendations': self.generate_recommendations()
        }
        return summary
    
    def calculate_risk_score(self, risks):
        """Calculate overall risk score"""
        score = (risks['critical'] * 10) + (risks['high'] * 5) + (risks['medium'] * 3) + (risks['low'] * 1)
        return min(100, score)
    
    def get_overall_status(self, risks):
        """Get overall security status"""
        if risks['critical'] > 0:
            return 'Critical'
        elif risks['high'] > 0:
            return 'High Risk'
        elif risks['medium'] > 0:
            return 'Medium Risk'
        elif risks['low'] > 0:
            return 'Low Risk'
        return 'Secure'
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []
        security = self.data.get('security_obs', {})
        
        for risk_type in ['critical', 'high', 'medium']:
            for finding in security.get(risk_type, []):
                recommendations.append({
                    'priority': risk_type,
                    'finding': finding,
                    'suggestion': self.get_mitigation(finding)
                })
        return recommendations
    
    def get_mitigation(self, finding):
        """Get mitigation suggestion for a finding"""
        mitigations = {
            '.git repository exposed': 'Remove .git directory from web root or restrict access',
            'Missing Content-Security-Policy': 'Implement CSP header to prevent XSS attacks',
            'Missing Strict-Transport-Security': 'Enable HSTS to enforce HTTPS',
            'Directory listing enabled': 'Disable directory listing in web server configuration',
            'Sensitive file exposed': 'Restrict access to sensitive files',
            'Cookies missing Secure flag': 'Set Secure flag for cookies',
            'Cookies missing HttpOnly flag': 'Set HttpOnly flag for cookies',
        }
        return mitigations.get(finding, 'Review and address the finding')
    
    def generate_html_report(self, output_path):
        """Generate HTML report"""
        from reports.html_generator import generate_html_report
        return generate_html_report(self.data, output_path)
    
    def generate_json_report(self, output_path):
        """Generate JSON report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, default=str)
        return output_path