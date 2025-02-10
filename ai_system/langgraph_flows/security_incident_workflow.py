from langgraph.graph import StateGraph
from typing import TypedDict, List
from ai_system.langchain_config.agent_tools import (
    detect_network_anomalies,
    scan_for_vulnerabilities,
    handle_security_incident,
    analyze_email_for_phishing,
    investigate_security_breach,
)

# Define the state
class SecurityIncidentState(TypedDict):
    network_data: List[List[int]]
    incident_type: str
    email_text: str
    vulnerabilities: List[dict]
    response: str
    investigation: dict

# Create the workflow
def create_security_incident_workflow():
    workflow = StateGraph(SecurityIncidentState)

    # Add nodes
    workflow.add_node("detect_anomalies", detect_network_anomalies)
    workflow.add_node("scan_vulnerabilities", scan_for_vulnerabilities)
    workflow.add_node("handle_incident", handle_security_incident)
    workflow.add_node("analyze_email", analyze_email_for_phishing)
    workflow.add_node("investigate_breach", investigate_security_breach)

    # Define edges
    workflow.set_entry_point("detect_anomalies")
    workflow.add_edge("detect_anomalies", "scan_vulnerabilities")
    workflow.add_edge("scan_vulnerabilities", "handle_incident")
    workflow.add_conditional_edges(
        "handle_incident",
        lambda x: "phishing" if "phishing" in x["incident_type"].lower() else "breach",
        {
            "phishing": "analyze_email",
            "breach": "investigate_breach",
        },
    )
    workflow.set_finish_point("analyze_email")
    workflow.set_finish_point("investigate_breach")

    return workflow.compile()