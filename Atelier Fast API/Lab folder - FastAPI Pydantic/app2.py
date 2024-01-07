import numpy as np
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pickle
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # assuming your templates are in a "templates" directory

model = pickle.load(open(r'C:\Users\PC\Documents\UM6P\S3\Cloud Native AI and ML II\TP2\Lab folder - FastAPI Pydantic\model_iris', 'rb'))  # loads ML model

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/predict')
async def predict(request: Request, features: list = Form(...)):
    int_features = [float(x) for x in features]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = prediction[0]

    return templates.TemplateResponse("index.html", {"request": request, "prediction_text": f'Iris species: {output}'})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081, reload=True)
