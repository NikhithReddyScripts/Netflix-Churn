from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import mlflow.sklearn

# Load the ML model
model = mlflow.sklearn.load_model("model")  # Change path if needed

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class UserInput(BaseModel):
    features: list  # 27 PCA-transformed values

# Prediction route
@app.post("/predict")
def predict(data: UserInput):
    arr = np.array(data.features).reshape(1, -1)
    pred = model.predict(arr)[0]
    prob = model.predict_proba(arr)[0][1]
    return {
        "prediction": int(pred),
        "churn_probability": round(prob, 4)
    }