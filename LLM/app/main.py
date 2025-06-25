import os
from fastapi import FastAPI, Request
from model import Model
import json


model = Model('./model')
app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    data = await request.body()
    data_str = data.decode("utf-8")
    data_dict = json.loads(data_str)

    pred = model.predict(data_dict['text'], n_labels=2)
    resp = ', '.join([f"{label['label']}: {label['score']}" for label in pred])
    return {"prediction": resp}
