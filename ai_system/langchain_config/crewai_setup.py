from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from ai_system.langchain_config.gemini_integration import GeminiLLM
from ai_system.langchain_config.agent_tools import (
    detect_network_anomalies,
    scan_for_vulnerabilities,
    handle_security_incident,
    encrypt_sensitive_data,
    investigate_security_breach,
)
from crewai import LLM
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Basic configuration
llm = LLM(
    model="gemini/gemini-1.5-flash-latest",
    temperature=0.7,
    timeout=120,           # Seconds to wait for response
    max_tokens=4000,       # Maximum length of response
    top_p=0.9,            # Nucleus sampling parameter
    frequency_penalty=0.1, # Reduce repetition
    presence_penalty=0.1,  # Encourage topic diversity
    response_format={"type": "json"},  # For structured outputs
    seed=42,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Load API key from environment variable
os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")

# Define Cybersecurity Tools for Agents
security_tools = [
    detect_network_anomalies,  # Tool for Threat Detection
    scan_for_vulnerabilities,  # Tool for Vulnerability Scanning
    handle_security_incident,  # Tool for Incident Response
    encrypt_sensitive_data,  # Tool for Data Protection
    investigate_security_breach  # Tool for Investigating Breaches
]

# Define Cybersecurity Agents
threat_detection_agent = Agent(
    role="Threat Analyst",
    goal="Detect and analyze network anomalies in real-time",
    backstory="""Expert in network traffic analysis with 10+ years experience in 
               identifying sophisticated cyber threats""",
    tools=[security_tools[0]],  # Detect Network Anomalies
    llm=llm,  # Pass the Gemini model via Langchain
    verbose=True
)

vulnerability_agent = Agent(
    role="Vulnerability Researcher",
    goal="Identify system vulnerabilities and suggest patches",
    backstory="""Former white-hat hacker with deep knowledge of system vulnerabilities
               and security best practices""",
    tools=[security_tools[1]],  # Scan for Vulnerabilities
    llm=llm,  # Pass the Gemini model via Langchain
    verbose=True
)

incident_response_agent = Agent(
    role="Incident Commander",
    goal="Coordinate incident response efforts",
    backstory="""Experienced cybersecurity incident manager with track record of 
               handling critical breaches""",
    tools=[security_tools[2], security_tools[4]],  # Handle Incident & Investigate Breach
    llm=llm,  # Pass the Gemini model via Langchain
    verbose=True
)

data_protection_agent = Agent(
    role="Cryptography Expert",
    goal="Ensure data security through encryption",
    backstory="""Cryptography specialist with expertise in data protection 
               and secure communication""",
    tools=[security_tools[3]],  # Encrypt Sensitive Data
    llm=llm,  # Pass the Gemini model via Langchain
    verbose=True
)

# Define Collaborative Tasks
threat_analysis_task = Task(
    description="""Analyze network traffic data for potential threats: {network_data}""",
    expected_output="Detailed threat report with anomaly locations",
    agent=threat_detection_agent,
    output_file="threat_report.md"
)

vulnerability_scan_task = Task(
    description="Perform full system vulnerability scan",
    expected_output="Prioritized list of vulnerabilities with CVSS scores",
    agent=vulnerability_agent,
    output_file="vulnerability_report.md"
)

incident_response_task = Task(
    description="""Respond to detected {incident_type} incident. 
                Current status: {incident_status}""",
    expected_output="Incident resolution report with timeline of actions",
    agent=incident_response_agent,
    output_file="incident_response.md"
)

data_protection_task = Task(
    description="Encrypt sensitive data payload: {sensitive_data}",
    expected_output="Encrypted data and encryption metadata",
    agent=data_protection_agent,
    output_file="encryption_report.md"
)

# Create Autonomous Security Crew
security_crew = Crew(
    agents=[threat_detection_agent, vulnerability_agent, incident_response_agent, data_protection_agent],
    tasks=[threat_analysis_task, vulnerability_scan_task, incident_response_task, data_protection_task],
   # llm=llm,
    verbose=True,
    memory=True  # Enable conversational memory
)

# Enhanced kickoff function with Gemini integration
def autonomous_kickoff(context: Dict[str, Any]) -> str:
    """
    Orchestrate collaborative workflow with Gemini-powered decision making.
    The function uses Gemini to analyze the situation and suggest a workflow plan.
    """
    # Use Gemini for initial situation analysis
    situation_prompt = f"""Security scenario analysis:
                        Context: {context}
                        Recommend appropriate workflow sequence"""
    
    try:
        # Get the workflow plan from Gemini via Langchain (using the invoke method for AI-based decision)
        workflow_plan = GeminiLLM.invoke(situation_prompt)
        
        # Execute CrewAI workflow with dynamic adjustments based on Gemini's recommendations
        result = security_crew.kickoff(
            inputs=context,
            workflow=workflow_plan,
            callback=handle_crew_update
        )
        return result

    except Exception as e:
        return f"Workflow execution failed: {str(e)}"

def handle_crew_update(message: str):
    """Real-time monitoring handler for Crew updates"""
    print(f"CREW UPDATE: {message}")
    # Add integration with monitoring systems, logging, or alerting as needed
    # e.g., send to monitoring systems, save logs, trigger alert notifications, etc.
    # Example: `send_alert(message)`
