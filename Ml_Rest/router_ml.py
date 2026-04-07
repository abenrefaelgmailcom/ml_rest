from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import numpy as np
import os

from auth import get_current_user
from ml_model import train_and_save_model, predict_from_model


router = APIRouter(tags=["ML"])


class TrainRequest(BaseModel):
    X: list[float]
    Y: list[float]
    degree: int = Field(default=3, ge=1, le=10)


@router.post("/train")
def train_model(data: TrainRequest, current_user=Depends(get_current_user)):
    if len(data.X) == 0 or len(data.Y) == 0:
        raise HTTPException(status_code=400, detail="X and Y cannot be empty")

    if len(data.X) != len(data.Y):
        raise HTTPException(status_code=400, detail="X and Y must be same length")

    user_name = current_user["user_name"]

    model_name = f"{user_name}.pkl"

    X = np.array(data.X).reshape(-1, 1)
    Y = np.array(data.Y)

    try:
        train_and_save_model(X, Y, model_name, data.degree)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "message": "Model trained successfully",
        "user_name": user_name,
        "model_file": model_name,
        "degree": data.degree
    }


@router.get("/predict/{hours}")
def predict(hours: float, current_user=Depends(get_current_user)):
    user_name = current_user["user_name"]
    model_name = f"{user_name}.pkl"

    if not os.path.exists(model_name):
        raise HTTPException(
            status_code=404,
            detail="Model not found for this user. Train first."
        )

    try:
        prediction = predict_from_model(model_name, hours)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "user_name": user_name,
        "hours": hours,
        "predicted_running_time": prediction
    }