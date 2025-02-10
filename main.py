from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import agent routes
from agents.threat_detection.network_monitor import router as threat_detection_router
from agents.vulnerability_scanner.system_scanner import router as vulnerability_scanner_router
from agents.incident_response.response_automator import router as incident_response_router

# Import the Gemini agent components
from ai_system.langchain_config.gemini_agent import agent_executor, tool_names, tools_str

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware - adjust as needed for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Cybersecurity AI Agents System"}

# Pydantic model to validate the input
class QuestionRequest(BaseModel):
    question: str

# Gemini-powered agent endpoint
@app.post("/ask")
async def ask_agent(request: QuestionRequest):
    """Endpoint to ask the agent a question."""
    try:
        # Build the input dictionary with all required variables
        input_vars = {
            "input": request.question,
            "agent_scratchpad": "",
            "tool_names": tool_names,
            "tools": tools_str,
        }
        response = agent_executor.invoke(input_vars)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")

# Include agent routes for specific cybersecurity tasks
app.include_router(threat_detection_router, prefix="/threat-detection")
app.include_router(vulnerability_scanner_router, prefix="/vulnerability-scanner")
app.include_router(incident_response_router, prefix="/incident-response")

# Run the app with Uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
