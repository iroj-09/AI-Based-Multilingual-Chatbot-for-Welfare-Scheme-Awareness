from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserInput(BaseModel):
    age: int
    gender: str
    occupation: str
    income: int

@router.post("/eligibility")
def eligibility(user: UserInput):

    schemes = []

    if user.occupation == "Farmer":
        schemes.append("PM-KISAN")

    if user.income < 300000:
        schemes.append("Ayushman Bharat")

    return {
        "recommended_schemes": schemes
    }