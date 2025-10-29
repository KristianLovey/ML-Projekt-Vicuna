from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib


model = joblib.load("btc_direction_model_docker.pkl")


app = FastAPI(
    title="Bitcoin Price Direction API",
    description="API koji predviđa hoće li cijena Bitcoina porasti ili pasti u sljedećem satu.",
    version="1.0.0"
)

class InputData(BaseModel):
    Open: float
    High: float
    Low: float
    Close: float
    Trades: float
    Volume: float

@app.get("/info")
def info():
    return {
        "model": "RandomForestClassifier",
        "target": "Direction (0 = pad, 1 = rast)",
        "description": "Model treniran na satnim Bitcoin podacima s tehničkim indikatorima"
    }

@app.post("/predict")
def predict(data: InputData):
    try:
        df = pd.DataFrame([data.model_dump()])
     
        df["ratio_high_low"] = df["High"] / df["Low"]
        df["ratio_close_open"] = df["Close"] / df["Open"]
        df["momentum"] = df["Close"] - df["Open"]
        df["hour"] = pd.Timestamp.now().hour
        df["day_of_week"] = pd.Timestamp.now().dayofweek
        df["month"] = pd.Timestamp.now().month

    
        expected_cols = model.feature_names_in_
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_cols]

        pred = model.predict(df)[0]
        return {"prediction": int(pred)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
