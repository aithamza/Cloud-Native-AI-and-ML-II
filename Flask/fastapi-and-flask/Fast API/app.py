
from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import numpy as np
from sklearn import *
import pandas as pd


with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

class PredictRequest(BaseModel):
    bedrooms : int
    bathrooms : float
    sqft_living:int
    sqft_lot: int
    floors:float
    waterfront: int
    view: int
    condition:  int
    grade: int
    sqft_above: int
    sqft_basement :int
    yr_built:int
    yr_renovated : int
    zipcode: int
    lat:float
    long:float
    sqft_living15 : int
    sqft_lot15: int



@app.post('/predict')
def predict(request: PredictRequest):
    features = pd.DataFrame([{
            "bedrooms": request.bedrooms,
            "bathrooms": request.bathrooms,
            "sqft_living": request.sqft_living,
            "sqft_lot": request.sqft_lot,
            "floors": request.floors,
            "waterfront": request.waterfront,
            "view": request.view,
            "condition": request.condition,
            "grade": request.grade,
            "sqft_above": request.sqft_above,
            "sqft_basement": request.sqft_basement,
            "yr_built": request.yr_built,
            "yr_renovated": request.yr_renovated,
            "zipcode": request.zipcode,
            "lat": request.lat,
            "long": request.long,
            "sqft_living15": request.sqft_living15,
            "sqft_lot15": request.sqft_lot15,
        }])
    prediction = model.predict(features)
    return {"prediction": prediction[0]}
