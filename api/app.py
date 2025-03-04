import os
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import uvicorn
import pickle
import numpy as np
from datetime import datetime

# Database imports.
from api.database import engine, SessionLocal, PredictionLog, Base
from sqlalchemy.orm import Session

# Create database tables if not exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time Fraud Detection API with Monitoring")

# --- Prometheus Monitoring Setup ---
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

API_KEY = os.getenv("API_KEY", "secret-key")
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

class PredictionRequest(BaseModel):
    features: list  # List of numerical features.
    transaction_id: Optional[str] = "default"

@app.post("/predict", dependencies=[Depends(verify_api_key)])
def predict_endpoint(request: PredictionRequest, db: Session = Depends(get_db)):
    model_path = os.getenv("MODEL_PATH", "model/fraud_model.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model load error: {e}")
    
    features = np.array(request.features, dtype=np.float32).reshape(1, -1)
    try:
        fraud_prob = model.predict_proba(features)[0][1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
    
    log_entry = PredictionLog(
        equipment_id=request.transaction_id,
        sensor_data=str(request.features),
        prediction=str(fraud_prob),
        timestamp=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    return {
        "transaction_id": request.transaction_id,
        "fraud_probability": fraud_prob,
        "timestamp": log_entry.timestamp.isoformat()
    }

@app.get("/history/{transaction_id}", dependencies=[Depends(verify_api_key)])
def get_history(transaction_id: str, db: Session = Depends(get_db)):
    logs = db.query(PredictionLog).filter(PredictionLog.equipment_id == transaction_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No history found for this transaction ID.")
    return [
        {
            "sensor_data": log.sensor_data,
            "prediction": log.prediction,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
