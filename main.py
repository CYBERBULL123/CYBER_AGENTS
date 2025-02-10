from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import agent routes
from agents.threat_detection.network_monitor import router as threat_detection_router
from agents.vulnerability_scanner.system_scanner import router as vulnerability_scanner_router
from agents.incident_response.response_automator import router as incident_response_router

# Import the Gemini agent components
from ai_system.langchain_config.gemini_agent import agent_executor, tool_names, tools_str

# Initialize FastAPI app
app = FastAPI(title="CyberAgent AI", description="AI-powered cybersecurity platform.")

# Configure static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

# Route handlers for pages
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/vulnerability-scanner")
async def vulnerability_page(request: Request):
    return templates.TemplateResponse("vulnerability.html", {"request": request})

@app.get("/incident-response")
async def incident_page(request: Request):
    return templates.TemplateResponse("incident_response.html", {"request": request})

@app.get("/threat-detection")
async def threat_page(request: Request):
    return templates.TemplateResponse("threat_detection.html", {"request": request})

# Cybersecurity Assistant endpoint
@app.post("/ask")
async def ask_agent(question: str = Form(...)):
    try:
        input_vars = {
            "input": question,
            "agent_scratchpad": "",
            "tool_names": tool_names,
            "tools": tools_str,
        }
        response = agent_executor.invoke(input_vars)
        
        # Extract the final answer from the response
        final_answer = response.get("response", "No response generated.")
        return {"response": final_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Include agent API routes
app.include_router(threat_detection_router, prefix="/api/threat-detection")
app.include_router(vulnerability_scanner_router, prefix="/api/vulnerability-scanner")
app.include_router(incident_response_router, prefix="/api/incident-response")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)