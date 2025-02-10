# CyberAgent AI Platform 🛡️

**CyberAgent** is an AI-powered cybersecurity platform designed to automate threat detection, vulnerability scanning, and incident response. Built with **FastAPI** for the backend and integrated with **Gemini AI**, **CrewAI**, and **LangGraph**, it provides a robust and scalable solution for modern cybersecurity challenges.

---

## Features ✨

- **Cybersecurity Assistant**: Ask questions and get AI-powered insights on cybersecurity threats, vulnerabilities, and best practices.
- **Threat Detection**: Real-time monitoring and anomaly detection using AI agents.
- **Vulnerability Scanning**: Automated system scans to identify security weaknesses.
- **Incident Response**: AI-driven workflows for handling security incidents.
- **Gemini AI Integration**: Advanced threat modeling and reasoning capabilities.
- **CrewAI Orchestration**: Multi-agent collaboration for complex tasks.
- **LangGraph Workflows**: Stateful automation for cybersecurity processes.

---

## Tech Stack 🛠️

### Backend
- **FastAPI**: High-performance Python framework for building APIs.
- **Uvicorn**: ASGI server for running FastAPI.
- **Pydantic**: Data validation and settings management.

### AI Integration
- **Gemini AI**: Advanced AI models for threat analysis and reasoning.
- **CrewAI**: Multi-agent task delegation and orchestration.
- **LangGraph**: Stateful workflow automation.

### Frontend
- **Tailwind CSS**: Utility-first CSS framework for responsive design.
- **HTMX**: Lightweight library for dynamic HTML without JavaScript.
- **Jinja2**: Templating engine for rendering HTML.

---

## Project Structure 📂

```
Cyber_Agents/
├── agents/                  # AI agents for specific tasks
│   ├── threat_detection/    # Threat detection agents
│   ├── vulnerability_scanner/ # Vulnerability scanning agents
│   └── incident_response/   # Incident response agents
│
├── ai_system/               # AI integration and orchestration
│   ├── langchain_config/    # LangChain and Gemini configurations
│   └── langgraph_flows/     # Stateful workflows
│
├── frontend/                # Frontend templates and static files
│   ├── static/              # CSS, JS, and images
│   └── templates/           # HTML templates
│
├── core/                    # Core application logic
│   ├── data_models/         # Pydantic models
│   └── workflows/           # Business logic and workflows
│
├── infrastructure/          # Infrastructure and integrations
│   ├── data_connectors/     # SIEM and cloud integrations
│   └── message_brokers/     # Kafka and RabbitMQ handlers
│
├── tests/                   # Unit and integration tests
│
├── docker/                  # Docker configurations
│
└── README.md                # Project documentation
```

---

## Installation 🚀

### Prerequisites
- Python 3.9+
- Docker (optional)
- PostgreSQL (optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/CYBERBULL123/CYBER_AGENTS.git
   cd CYBER_AGENTS
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and add the following:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/cyberagent
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

6. Access the platform:
   Open your browser and navigate to `http://localhost:8000`.

---

## Usage 🖥️

### Homepage
- **Ask the AI Agent**: Enter a cybersecurity question and get real-time insights.
- **Quick Actions**: Navigate to threat detection, vulnerability scanning, or incident response.

### Threat Detection
- Monitor real-time network activity.
- View detected threats and anomalies.

### Vulnerability Scanner
- Run system scans to identify vulnerabilities.
- View detailed scan reports.

### Incident Response
- Submit incident details for automated handling.
- Track incident resolution status.

---

## API Endpoints 🌐

| Endpoint                  | Method | Description                          |
|---------------------------|--------|--------------------------------------|
| `/`                       | GET    | Homepage                             |
| `/ask`                    | POST   | Ask the AI agent a question          |
| `/threat-detection/data`  | GET    | Fetch real-time threat data          |
| `/vulnerability-scanner/scan` | POST | Run a vulnerability scan         |
| `/incident-response/trigger` | POST | Trigger incident response        |

---

## Contributing 🤝

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.


---