from pydantic import BaseModel

class ISBNRequest(BaseModel):
    isbn: str

class SafetyReport(BaseModel):
    title: str
    author: str
    violence: str
    profanity: str
    sexual_content: str
    recommended_age: str
    gender_identity: str