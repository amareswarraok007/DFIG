# ======================================================
# FINAL FIXED VERSION - DFIG Predict Service (app.py)
# ======================================================

import os, joblib, pandas as pd, logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("predict-service")

# ---------- App Setup ----------
app = FastAPI(title="DFIG Crop Prediction Service")
MODEL_PATH = os.getenv("MODEL_PATH", "../model/pipeline.pkl")

# ---------- Load model ----------
try:
    pipeline = joblib.load(MODEL_PATH)
    supports_proba = hasattr(pipeline, "predict_proba")
    log.info(f"✅ Loaded model from {MODEL_PATH}")
except Exception as e:
    log.exception("❌ Failed to load model.")
    raise

# ---------- CORS Middleware ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # for demo; restrict later in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Input Schema ----------
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict_one(payload: CropInput):
    try:
        df = pd.DataFrame([payload.dict()])
        pred = pipeline.predict(df)[0]
        conf = None
        if supports_proba:
            conf = round(float(max(pipeline.predict_proba(df)[0])), 3)
        return {"prediction": pred, "confidence": conf}
    except Exception as e:
        log.exception("Prediction error")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict_batch")
def predict_batch(payload: List[CropInput]):
    try:
        df = pd.DataFrame([p.dict() for p in payload])
        preds = pipeline.predict(df).tolist()
        return {"predictions": preds}
    except Exception as e:
        log.exception("Batch prediction error")
        raise HTTPException(status_code=400, detail=str(e))
