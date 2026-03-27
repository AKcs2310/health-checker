from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

from backend.llm import analyze_symptoms
from backend.database import init_db, save_query, get_history

app = FastAPI(title="Healthcare Symptom Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SymptomRequest(BaseModel):
    symptoms: str = Field(..., min_length=3, max_length=2000,
                          description="Describe your symptoms")


class SymptomResponse(BaseModel):
    symptoms: str
    analysis: str


@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/api/check", response_model=SymptomResponse)
async def check_symptoms(req: SymptomRequest):
    try:
        analysis = await analyze_symptoms(req.symptoms)
        await save_query(req.symptoms, analysis)
        return SymptomResponse(symptoms=req.symptoms, analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def query_history():
    return await get_history()
