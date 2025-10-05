import os, joblib, pandas as pd, logging
from fastapi import FastAPI, HTTPException, Request
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("predict-service")

app = FastAPI(title="Agri Model Service")
MODEL_PATH = os.getenv("MODEL_PATH", "../model/pipeline.pkl")

# Load pipeline once at startup
try:
    pipeline = joblib.load(MODEL_PATH)
    supports_proba = hasattr(pipeline, "predict_proba")
    log.info(f"Loaded pipeline from {MODEL_PATH}")
except Exception as e:
    log.exception("Failed to load model at startup")
    raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict_single(request: Request):
    try:
        payload = await request.json()
        # accept dict for single prediction
        if isinstance(payload, dict):
            df = pd.DataFrame([payload])
        else:
            raise HTTPException(status_code=400, detail="Expected a JSON object for single prediction")
        preds = pipeline.predict(df).tolist()
        result = {"predictions": preds}
        if supports_proba:
            result["probabilities"] = pipeline.predict_proba(df).tolist()
        return result
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Prediction error")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict_batch")
async def predict_batch(request: Request):
    try:
        payload = await request.json()
        if isinstance(payload, list):
            df = pd.DataFrame(payload)
        else:
            raise HTTPException(status_code=400, detail="Expected a JSON array for batch prediction")
        preds = pipeline.predict(df).tolist()
        result = {"predictions": preds}
        if supports_proba:
            result["probabilities"] = pipeline.predict_proba(df).tolist()
        return result
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Batch prediction error")
        raise HTTPException(status_code=400, detail=str(e))
