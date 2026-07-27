# modules/ssl_intelligence.py
import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime
from utils.logger import get_logger

logger = get_logger()

def get_ssl_intelligence(domain):
    """
    Comprehensive SSL/TLS certificate intelligence.
    """
    result = {}
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                der_cert = ssock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())
                
                # Basic Info
                result['issuer'] = cert.issuer.rfc4514_string()
                result['subject'] = cert.subject.rfc4514_string()
                result['organization'] = get_organization(cert)
                result['common_name'] = get_common_name(cert)
                
                # Validity
                not_before = cert.not_valid_before_utc
                not_after = cert.not_valid_after_utc
                
                result['not_before'] = not_before.strftime("%Y-%m-%d %H:%M:%S")
                result['not_after'] = not_after.strftime("%Y-%m-%d %H:%M:%S")
                result['expiration'] = not_after.strftime("%Y-%m-%d")
                
                now = datetime.datetime.now(datetime.timezone.utc)
                result['days_remaining'] = (not_after - now).days
                
                # SAN
                san_list = []
                try:
                    san_ext = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                    san_list = [name.value for name in san_ext.value if isinstance(name, x509.DNSName)]
                except:
                    pass
                result['sans'] = san_list
                
                # Signature
                result['signature_algorithm'] = cert.signature_algorithm_oid._name
                result['version'] = cert.version.value
                result['serial_number'] = str(cert.serial_number)
                
                # Key
                public_key = cert.public_key()
                if hasattr(public_key, 'key_size'):
                    result['key_size'] = public_key.key_size
                else:
                    result['key_size'] = 'Unknown'
                
                # Cipher
                result['cipher'] = str(ssock.cipher())
                
                # Wildcard
                result['wildcard'] = any('*' in san for san in san_list)
                
                # Self Signed
                result['self_signed'] = cert.issuer == cert.subject
                
                # Expired
                result['expired'] = not_after < now
                
    except Exception as e:
        logger.error(f"SSL intelligence failed: {e}")
        result['error'] = str(e)
        
    return result

def get_organization(cert):
    """Extract organization from certificate subject with fallbacks"""
    # Try organizationName
    for attr in cert.subject:
        if attr.oid._name == 'organizationName':
            return attr.value
    
    # Try organizationalUnitName
    for attr in cert.subject:
        if attr.oid._name == 'organizationalUnitName':
            return attr.value
    
    # Try commonName as fallback
    for attr in cert.subject:
        if attr.oid._name == 'commonName':
            cn = attr.value
            # Extract organization from common name if possible
            if '.' in cn:
                parts = cn.split('.')
                if len(parts) >= 2:
                    return parts[-2].capitalize()
            return cn
    
    # Try emailAddress
    for attr in cert.subject:
        if attr.oid._name == 'emailAddress':
            return attr.value.split('@')[-1].split('.')[0].capitalize()
    
    return 'N/A'

def get_common_name(cert):
    """Extract common name from certificate subject"""
    for attr in cert.subject:
        if attr.oid._name == 'commonName':
            return attr.value
    return 'N/A'