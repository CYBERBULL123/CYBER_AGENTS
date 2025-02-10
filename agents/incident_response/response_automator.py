from fastapi import APIRouter

router = APIRouter()

class IncidentResponder:
    def __init__(self):
        self.playbooks = {
            "ransomware": self._handle_ransomware,
            "phishing": self._handle_phishing,
        }

    def handle_incident(self, incident_type):
        if incident_type in self.playbooks:
            return self.playbooks[incident_type]()
        return {"response": "No playbook available for this incident."}

    def _handle_ransomware(self):
        return {"response": "Isolate infected devices, disconnect from network, and notify IT team."}

    def _handle_phishing(self):
        return {"response": "Quarantine email, reset compromised credentials, and scan for malware."}

responder = IncidentResponder()

@router.post("/handle")
async def handle(incident_type: str):
    return responder.handle_incident(incident_type)