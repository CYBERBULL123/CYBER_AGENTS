from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, Runnable
from langchain.agents import AgentExecutor
from langchain.agents.agent import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
import re
from typing import Union

from crewai import Crew
from typing import Dict, Any

# Import necessary modules
from ai_system.langchain_config.crewai_setup import security_crew
from ai_system.langchain_config.gemini_integration import  GeminiLLM
from ai_system.langchain_config.agent_tools import (
    detect_network_anomalies,
    scan_for_vulnerabilities,
    handle_security_incident,
    encrypt_sensitive_data,
    investigate_security_breach,
)

# Define tools
tools = [
    Tool(
        name="Detect Network Anomalies",
        func=detect_network_anomalies,
        description="Useful for detecting anomalies in network traffic.",
    ),
    Tool(
        name="Scan for Vulnerabilities",
        func=scan_for_vulnerabilities,
        description="Useful for scanning the system for vulnerabilities.",
    ),
    Tool(
        name="Handle Security Incident",
        func=handle_security_incident,
        description="Useful for handling security incidents like ransomware or phishing.",
    ),
    Tool(
        name="Encrypt Sensitive Data",
        func=encrypt_sensitive_data,
        description="Useful for encrypting sensitive data.",
    ),
    Tool(
        name="Investigate Security Breach",
        func=investigate_security_breach,
        description="Useful for investigating security breaches.",
    ),
]

# Add collaborative execution layer
class CollaborativeExecutor:
    def __init__(self, crew: Crew, llm: GeminiLLM):
        self.crew = crew
        self.llm = llm
        self.context_memory = []

    def execute_workflow(self, user_input: str) -> Dict[str, Any]:
        # Use Gemini for context understanding
        analysis_prompt = f"""User request analysis:
                           Input: {user_input}
                           Determine required tools and workflow"""
        
        analysis = self.llm.invoke(analysis_prompt)
        self.context_memory.append(analysis)

        # Map to CrewAI execution
        context = self._create_execution_context(user_input, analysis)
        return self.crew.autonomous_kickoff(context)

    def _create_execution_context(self, user_input: str, analysis: str) -> Dict[str, Any]:
        return {
            "user_input": user_input,
            "llm_analysis": analysis,
            "environment_state": self._get_system_status()
        }

    def _get_system_status(self) -> Dict[str, Any]:
        # Add actual system monitoring integration
        return {
            "network_status": "stable",
            "active_incidents": 0,
            "encryption_status": "active"
        }
# Initialize collaborative system
collaborative_system = CollaborativeExecutor(
    crew=security_crew,
    llm=GeminiLLM()
)

# --------------------------
# GeminiLLM Implementation
# --------------------------
# class GeminiLLMTEXT(Runnable):
#     def invoke(self, input: str) -> str:
#         """Required method for Runnable to function correctly."""
#         try:
#             # Ensure input is properly formatted as string
#             if isinstance(input, dict):
#                 prompt = input.get('input', '')
#                 if not prompt:
#                     return "Error: No input provided"
#             else:
#                 prompt = str(input)

#             # Generate the response using Gemini with proper formatting
#             response = generate_response({"text": prompt})
            
#             # The response from GeminiLLM will guide the agents on what to do
#             if isinstance(response, str) and "automate" in response.lower():
#                 return self.automate_crew_tasks(prompt)
            
#             return str(response) if response else "No response generated"
#         except Exception as e:
#             return f"Error generating response: {str(e)}"

#     def automate_crew_tasks(self, prompt: str) -> str:
#         try:
#             crew_task_prompt = f"Instructions for CrewAI agents: {prompt}"
#             result = security_crew.kickoff(inputs={"prompt": crew_task_prompt})
#             return str(result) if result else "No automation result"
#         except Exception as e:
#             return f"Error automating CrewAI tasks: {str(e)}"


# --------------------------
# Build dynamic tool variables for the prompt
# --------------------------
tool_names = ", ".join([tool.name for tool in tools])
tools_str = ", ".join([f"{tool.name}: {tool.description}" for tool in tools])

# --------------------------
# Define Prompt Template
# --------------------------
# The prompt template expects 4 variables: input, agent_scratchpad, tool_names, and tools.
prompt_template = PromptTemplate.from_template(""" 
    You are a cybersecurity AI assistant. Your goal is to help users with security tasks.
    Available tools: {tools}

    Use the following format:
    Question: the input question you must answer
    Thought: consider what to do next
    Action: choose one of [{tool_names}]
    Action Input: provide relevant data
    Observation: review the result
    ... (repeat Thought/Action/Observation as needed)
    Thought: I now know the final answer
    Final Answer: your response to the question

    Question: {input}
    Thought: {agent_scratchpad}
""")

# --------------------------
# Define Output Parser
# --------------------------
class GeminiOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Ensure llm_output is a string.
        if not isinstance(llm_output, str):
            llm_output = str(llm_output)
        
        # Extract the final answer
        final_answer_match = re.search(r"Final Answer:\s*(.*)", llm_output, re.IGNORECASE)
        final_answer = final_answer_match.group(1).strip() if final_answer_match else "No final answer found."

        # Extract tool usage details
        tool_usage_matches = re.findall(r"Action:\s*(.*?)\n", llm_output, re.IGNORECASE)
        used_tools = list(set(tool_usage_matches))  # Remove duplicates
        
        return AgentFinish(
            return_values={
                "final_answer": final_answer,
                "tools_used": used_tools if used_tools else ["No tools used"]
            },
            log=llm_output,
        )


# --------------------------
# Build the LLM Chain with RunnableLambda
# --------------------------
llm = GeminiLLM()
# Wrap the LLM invocation so its output is immediately parsed by GeminiOutputParser.
llm_chain = prompt_template | RunnableLambda(lambda x: GeminiOutputParser().parse(llm.invoke(x)))

# --------------------------
# Agent Executor Configuration
# --------------------------
# Update AgentExecutor integration
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=llm_chain,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
    early_stopping_method="generate"
)
