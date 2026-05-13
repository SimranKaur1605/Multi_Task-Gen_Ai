"""
main.py — FastAPI Backend for Multi-Task GenAI System
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# ── Import task runners from app.py ──────────────────────────────────────────
from app import (
    get_llm,
    run_summarize,
    run_qa,
    run_quiz,
    run_study_plan,
    run_explain_code,
)

app = FastAPI(
    title="Multi-Task GenAI API",
    description="LangChain + Groq-powered document intelligence system",
    version="1.0.0",
)

# Allow all origins for local dev — tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Shared LLM instance (lazy-loaded) ────────────────────────────────────────
_llm = None

def get_cached_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


# ── Request / Response models ─────────────────────────────────────────────────

class SummarizeRequest(BaseModel):
    document: str

class QARequest(BaseModel):
    document: str
    question: str

class QuizRequest(BaseModel):
    document: str
    num_questions: int = 5

class StudyPlanRequest(BaseModel):
    document: str
    duration_days: int = 7

class ExplainCodeRequest(BaseModel):
    code: str

class TaskResponse(BaseModel):
    result: str
    task: str


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "model": "llama-3.3-70b-versatile (Groq)"}


# ── Task endpoints ────────────────────────────────────────────────────────────

@app.post("/summarize", response_model=TaskResponse)
def summarize(req: SummarizeRequest):
    try:
        llm = get_cached_llm()
        result = run_summarize(req.document, llm)
        return TaskResponse(result=result, task="summarize")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/qa", response_model=TaskResponse)
def question_answer(req: QARequest):
    try:
        llm = get_cached_llm()
        result = run_qa(req.document, req.question, llm)
        return TaskResponse(result=result, task="qa")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/quiz", response_model=TaskResponse)
def generate_quiz(req: QuizRequest):
    try:
        llm = get_cached_llm()
        result = run_quiz(req.document, req.num_questions, llm)
        return TaskResponse(result=result, task="quiz")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/study-plan", response_model=TaskResponse)
def study_plan(req: StudyPlanRequest):
    try:
        llm = get_cached_llm()
        result = run_study_plan(req.document, req.duration_days, llm)
        return TaskResponse(result=result, task="study_plan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain-code", response_model=TaskResponse)
def explain_code(req: ExplainCodeRequest):
    try:
        llm = get_cached_llm()
        result = run_explain_code(req.code, llm)
        return TaskResponse(result=result, task="explain_code")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
