from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from models import ProcessModel, ProcessCreateRequest
from db import db
from llm_service import generate_process_model
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(
    title="Modus Enterprise AI Process Designer",
    description="API for analyzing and transforming business processes using AI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "AI Future Process Designer API is running",
        "docs": "/docs"
    }
@app.post("/api/analyze", response_model=ProcessModel)
def analyze_process(request: ProcessCreateRequest):
    """
    Takes a process name, generates the AI transformation architecture via Groq, 
    saves it to the database, and returns the structured data.
    """
    try:
        # 1. Call the AI Service
        generated_process = generate_process_model(
            process_name=request.process_name, 
            industry=request.industry
        )
        
        # 2. Save to persistent JSON database
        db.save(generated_process)
        
        return generated_process
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

@app.get("/api/processes", response_model=List[ProcessModel])
def get_all_processes():
    """
    Retrieves all saved processes. Proves data persistence across restarts.
    """
    return db.get_all()

@app.get("/api/processes/search", response_model=List[ProcessModel])
def search_processes(
    role: Optional[str] = Query(None, description="Filter by human role (e.g., 'Accountant')"),
    system: Optional[str] = Query(None, description="Filter by software system (e.g., 'ERP')")
):
    """
    Query endpoint. Proves the application can query structured components.
    """
    if role:
        return db.search_by_role(role)
    if system:
        return db.search_by_system(system)
    
    return db.get_all()

@app.get("/api/processes/{process_id}", response_model=ProcessModel)
def get_process_by_id(process_id: str):
    """
    Retrieves a specific process for detailed comparison on the frontend.
    """
    process = db.get_by_id(process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process

@app.delete("/api/processes/{process_id}")
def delete_process(process_id: str):
    """
    Removes a process from the database.
    """
    success = db.delete(process_id)
    if not success:
        raise HTTPException(status_code=404, detail="Process not found")
    return {"message": "Process deleted successfully"}
