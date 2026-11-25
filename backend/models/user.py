from pydantic import BaseModel, Field


class UserInput(BaseModel):
    age: int = Field(ge=0, le=120)
    gender: str
    occupation: str
    income: int = Field(ge=0)
