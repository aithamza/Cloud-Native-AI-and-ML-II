
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()
class iris(BaseModel):
 a:float
 b:float
 c:float
 d:float

from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle
#we are loading the model using pickle
model = pickle.load(open(r'C:\Users\PC\Documents\UM6P\S3\Cloud Native AI and ML II\TP2\Lab folder - FastAPI Pydantic\model_iris', 'rb'))
@app.get("/")
def home():
 return {'ML model for Iris prediction'}
@app.post('/make_predictions')
async def make_predictions(features: iris):
  return({"prediction":str(model.predict([[features.a,features.b,features.c,features.d]])[0])})
if __name__ == "__main__":
 uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)

