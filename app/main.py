# main.py
from fastapi import FastAPI
from app.routers import evaluations
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(evaluations.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Language Learning Evaluator"}