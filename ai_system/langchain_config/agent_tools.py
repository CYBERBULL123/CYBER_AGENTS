from langchain.tools import tool
from agents.threat_detection.network_monitor import NetworkMonitor
from agents.vulnerability_scanner.system_scanner import SystemScanner
from agents.incident_response.response_automator import IncidentResponder
# from agents.phishing_detection.email_analyzer import PhishingDetector
from agents.data_protection.encryption_manager import EncryptionManager
from agents.forensic_analysis.breach_investigator import BreachInvestigator

# Initialize agents
threat_monitor = NetworkMonitor()
vulnerability_scanner = SystemScanner()
incident_responder = IncidentResponder()
# phishing_detector = PhishingDetector()
encryption_manager = EncryptionManager()
breach_investigator = BreachInvestigator()

# Define LangChain tools
@tool
def detect_network_anomalies(network_data: list) -> dict:
    """Detect anomalies in network traffic."""
    return threat_monitor.detect_anomalies(network_data)

@tool
def scan_for_vulnerabilities() -> dict:
    """Scan the system for vulnerabilities."""
    return vulnerability_scanner.scan_system()

@tool
def handle_security_incident(incident_type: str) -> dict:
    """Handle a security incident (e.g., ransomware, phishing)."""
    return incident_responder.handle_incident(incident_type)

# @tool
# def analyze_email_for_phishing(email_text: str) -> dict:
#     """Analyze an email for phishing attempts."""
#     return phishing_detector.analyze_email(email_text)

@tool
def encrypt_sensitive_data(data: str) -> dict:
    """Encrypt sensitive data."""
    return encryption_manager.encrypt_data(data)

@tool
def investigate_security_breach() -> dict:
    """Investigate a security breach."""
    return breach_investigator.investigate()