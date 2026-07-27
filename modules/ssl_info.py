# modules/ssl_info.py
import ssl
import socket
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from utils.logger import get_logger

logger = get_logger()

def get_ssl_info(domain):
    """
    Retrieve SSL/TLS certificate details.
    Returns dict with issuer, subject, validity, SANs, etc.
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                der_cert = ssock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())

                def fmt_date(dt):
                    return dt.strftime("%Y-%m-%d %H:%M:%S")

                issuer = cert.issuer.rfc4514_string()
                subject = cert.subject.rfc4514_string()
                not_before = fmt_date(cert.not_valid_before)
                not_after = fmt_date(cert.not_valid_after)
                sig_alg = cert.signature_algorithm_oid._name
                version = cert.version.value
                serial = str(cert.serial_number)

                # Subject Alternative Names
                san_ext = None
                try:
                    san_ext = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                except x509.ExtensionNotFound:
                    pass
                san_list = []
                if san_ext:
                    san_list = [str(name) for name in san_ext.value]

                return {
                    "issuer": issuer,
                    "subject": subject,
                    "valid_from": not_before,
                    "valid_to": not_after,
                    "expiry": not_after,
                    "signature_algorithm": sig_alg,
                    "version": version,
                    "serial_number": serial,
                    "sans": san_list
                }
    except Exception as e:
        logger.error(f"SSL info retrieval failed: {e}")
        return {"error": str(e)}