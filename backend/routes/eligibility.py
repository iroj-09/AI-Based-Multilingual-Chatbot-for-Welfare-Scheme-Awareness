from fastapi import APIRouter

from models.user import UserInput
from services.recommender import recommend_schemes

router = APIRouter()


@router.post("/eligibility")
def eligibility(user: UserInput):
    return {"recommended_schemes": recommend_schemes(user.model_dump())}
