from fastapi import  FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

model = joblib.load("btc_direction_model.pkl")
#pred = model.predict(new_data)

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
        df = pd.DataFrame([data.dict()])
        pred = model.predict(df)[0]
        return {"prediction": int(pred)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))