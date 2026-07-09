from fastapi import FastAPI
from routes.eligibility import router

app = FastAPI()

app.include_router(router)