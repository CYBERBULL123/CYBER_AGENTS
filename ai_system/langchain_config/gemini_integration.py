import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_core.runnables import Runnable

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Check if API key is loaded
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# ---------------------------------
# ✅ Advanced GeminiLLM Class for CrewAI & Reasoning
# ---------------------------------
class GeminiLLM(Runnable):
    """Advanced class integrating Gemini LLM for reasoning and CrewAI task automation."""

    def __init__(self):
        # Initialize any additional parameters or configurations
        self.model = model  # Use initialized Gemini model
        self.error_message = "Error during reasoning or task automation."

    def invoke(self, input: str) -> dict:
        """Process input, generate reasoning, and automate CrewAI tasks when needed."""
        try:
            # Ensure input is properly formatted
            prompt = self._prepare_prompt(input)

            # Step 1: Use Gemini to analyze the input and make a decision
            reasoning = self._analyze_input(prompt)

            # Step 2: Trigger task automation if required based on Gemini's reasoning
            if self._requires_automation(reasoning):
                automated_result = self._automate_tasks(prompt)
                return self._generate_response("automated", automated_result)

            # Step 3: Return the reasoning response if no automation is needed
            return self._generate_response("reasoned", reasoning)

        except Exception as e:
            return self._handle_error(str(e))

    def _prepare_prompt(self, input: str) -> str:
        """Prepares the input by ensuring it's in the correct format for the Gemini model."""
        if isinstance(input, dict):
            return input.get('input', '')
        return str(input)

    def _analyze_input(self, prompt: str) -> str:
        """Generates reasoning using Gemini LLM."""
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text
            return self.error_message
        except Exception as e:
            return f"{self.error_message}: {str(e)}"

    def _requires_automation(self, reasoning: str) -> bool:
        """Check if Gemini's response suggests task automation."""
        return "automate" in reasoning.lower() or "execute" in reasoning.lower()

    def _automate_tasks(self, prompt: str) -> str:
        """Automates tasks using CrewAI, triggered by Gemini's reasoning."""
        try:
            # Lazy import to avoid circular dependency
            from ai_system.langchain_config.crewai_setup import security_crew
            crew_task_prompt = f"Cybersecurity Task: {prompt}"
            result = security_crew.kickoff(inputs={"prompt": crew_task_prompt})
            return str(result) if result else "No automation result from CrewAI."
        except Exception as e:
            return f"Error automating CrewAI tasks: {str(e)}"

    def _generate_response(self, type: str, content: str) -> dict:
        """Generates the final response based on the type (automated or reasoned)."""
        if type == "automated":
            return {
                "thoughts": "Gemini decided to execute CrewAI tasks.",
                "tools_used": ["CrewAI Agents"],
                "response": content
            }
        return {
            "thoughts": "Gemini analyzed the query.",
            "tools_used": ["Gemini Reasoning"],
            "response": content
        }

    def _handle_error(self, error_message: str) -> dict:
        """Handles errors gracefully and returns a consistent error response."""
        return {
            "error": f"Error during reasoning or task automation: {error_message}"
        }
