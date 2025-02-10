from fastapi import APIRouter

router = APIRouter()

class BreachInvestigator:
    def __init__(self):
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def investigate(self):
        # Simulate forensic analysis
        return {"timeline": self.logs}

investigator = BreachInvestigator()

@router.post("/add-log")
async def add_log(log: str):
    investigator.add_log(log)
    return {"message": "Log added successfully"}

@router.get("/investigate")
async def investigate():
    return investigator.investigate()