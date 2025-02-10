from fastapi import APIRouter
from transformers import pipeline

router = APIRouter()

# class PhishingDetector:
#     def __init__(self):
#         self.model = pipeline("text-classification", model="distilbert-base-uncased")

#     def analyze_email(self, email_text):
#         result = self.model(email_text)
#         return {"is_phishing": result[0]["label"] == "PHISHING"}

# detector = PhishingDetector()

# @router.post("/analyze")
# async def analyze(email_text: str):
#     return detector.analyze_email(email_text)