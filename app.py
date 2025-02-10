from flask import Flask, render_template, request, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session storage

FASTAPI_BACKEND_URL = "http://127.0.0.1:8000/ask"  # FastAPI Backend URL

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tools")
def security_tools():
    return render_template("tools.html")

@app.route("/cybersecurity-assistant")
def cybersecurity_assistant():
    return render_template("cybersecurity_assistant.html")

@app.route("/threat-detection")
def threat_detection():
    return render_template("threat_detection.html")

@app.route("/vulnerability-scanner")
def vulnerability_scanner():
    return render_template("vulnerability_scanner.html")

@app.route("/incident-response")
def incident_response():
    return render_template("incident_response.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = requests.post(FASTAPI_BACKEND_URL, json={"question": question})
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get response from AI: {str(e)}"}), 500

    formatted_response = format_response(data)

    # Store in session history
    if "chat_history" not in session:
        session["chat_history"] = []
    
    session["chat_history"].append({
        "question": question,
        "response": formatted_response
    })
    session.modified = True  # Ensure session updates are saved

    # 🔹 Return JSON with formatted HTML for HTMX
    return jsonify({"html": formatted_response})

def format_response(data):
    """Format AI response into a structured HTML block."""
    input_text = data.get("response", {}).get("input", "No input received")
    final_answer = data.get("response", {}).get("final_answer", "No answer available")
    tools_used = ", ".join(data.get("response", {}).get("tools_used", [])) or "None"

    return f"""
    <div class='bg-gray-800 text-white p-4 rounded-lg shadow-md animate-fadeIn'>
        <h3 class='text-lg font-semibold text-blue-400 flex items-center'>
            <span class="material-icons text-blue-400">security</span>
            AI Threat Analysis
        </h3>
        <p class='mt-2'><strong>🔎 Input:</strong> {input_text}</p>
        <p class='mt-2'><strong>🛡️ Final Answer:</strong> {final_answer}</p>
        <p class='mt-2'><strong>🛠️ Tools Used:</strong> {tools_used}</p>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True)
