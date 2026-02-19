import os
import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import uvicorn

from src.metrics_service import get_model_metrics
from src.models_config import SUBJECT_MODELS_CONFIG
from main import run_phase_1
from jury_evaluation import run_jury_evaluation

app = FastAPI(title="EECT Framework API")

class ExperimentRequest(BaseModel):
    model_name: str
    concepts: Optional[List[str]] = None

def run_full_diagnostic(model_name: str):
    """
    Triggers Phase 1 (Data Collection) and Phase 2 (Jury Evaluation)
    """
    print(f"Starting full diagnostic battery for {model_name}...")
    try:
        # Phase 1: Collect responses
        run_phase_1(model_name)
        # Phase 2: Score responses
        run_jury_evaluation(model_name)
        print(f"Completed full diagnostic battery for {model_name}.")
    except Exception as e:
        print(f"Error during diagnostic battery for {model_name}: {e}")

@app.get("/score/{model_name}")
async def get_score(model_name: str, background_tasks: BackgroundTasks):
    metrics = get_model_metrics(model_name)
    
    if metrics:
        return metrics
    
    # Check if model is valid
    valid_model = any(m['model_name'] == model_name for m in SUBJECT_MODELS_CONFIG)
    
    if valid_model:
        background_tasks.add_task(run_full_diagnostic, model_name)
        return {"status": "started", "message": f"Diagnostic battery started for {model_name}"}
    else:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found in configuration")

@app.post("/run_experiment")
async def run_experiment(request: ExperimentRequest, background_tasks: BackgroundTasks):
    valid_model = any(m['model_name'] == request.model_name for m in SUBJECT_MODELS_CONFIG)
    
    if not valid_model:
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found in configuration")
    
    background_tasks.add_task(run_full_diagnostic, request.model_name)
    return {"status": "started", "message": f"Experiment started for {request.model_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
