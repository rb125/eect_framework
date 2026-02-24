import json
import os
import threading
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.metrics_service import get_model_metrics
from src.models_config import SUBJECT_MODELS_CONFIG

app = FastAPI(title="EECT Framework API")

_in_flight_lock = threading.Lock()
_in_flight = set()



def _running_on_vercel() -> bool:
    return bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))


def run_full_diagnostic(model_name: str) -> None:
    """
    Triggers Phase 1 (Data Collection) and Phase 2 (Jury Evaluation)
    """
    print(f"Starting full diagnostic battery for {model_name}...")
    try:
        # Lazy import to keep /score available even if optional experiment deps fail.
        from main import run_phase_1
        from jury_evaluation import run_jury_evaluation

        # Phase 1: Collect responses
        run_phase_1(model_name)
        # Phase 2: Score responses
        run_jury_evaluation(model_name)
        print(f"Completed full diagnostic battery for {model_name}.")
    finally:
        with _in_flight_lock:
            _in_flight.discard(model_name)


def _is_valid_model(model_name: str) -> bool:
    return any(m.get("model_name") == model_name for m in SUBJECT_MODELS_CONFIG)


def _start_diagnostic_in_background(model_name: str) -> bool:
    with _in_flight_lock:
        if model_name in _in_flight:
            return False
        _in_flight.add(model_name)

    thread = threading.Thread(target=run_full_diagnostic, args=(model_name,), daemon=True)
    thread.start()
    return True


class ModelRequest(BaseModel):
    model_name: str


@app.get("/")
async def root():
    return {"message": "EECT Framework API is running."}


@app.get("/score/{model_name}")
async def get_score(model_name: str):
    """
    Return aggregated metrics for a model. If no scores exist yet, 
    start the full diagnostic battery in the background.
    """
    metrics = get_model_metrics(model_name)
    if metrics:
        return metrics

    if not _is_valid_model(model_name):
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found in configuration")

    if _running_on_vercel():
        raise HTTPException(
            status_code=400,
            detail="Pre-computed scores only. Background diagnostics are not supported on Vercel."
        )

    started = _start_diagnostic_in_background(model_name)
    status = "started" if started else "already_running"
    return {
        "status": status,
        "message": f"Diagnostic battery {status} for {model_name}"
    }


@app.post("/experiment")
async def run_experiment(request: ModelRequest):
    """
    Start the full diagnostic battery for a model.
    """
    model_name = request.model_name
    if not _is_valid_model(model_name):
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found in configuration")

    if _running_on_vercel():
        raise HTTPException(
            status_code=400,
            detail="Background experiments are disabled on Vercel. Run locally and commit results."
        )

    started = _start_diagnostic_in_background(model_name)
    status = "started" if started else "already_running"
    return {
        "status": status,
        "message": f"Experiment {status} for {model_name}"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
