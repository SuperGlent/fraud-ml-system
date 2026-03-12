from fastapi import FastAPI, Body
from sqlalchemy.engine import Engine
from fastapi.responses import HTMLResponse, JSONResponse
from services import preproc, preproc_features
import mlflow
import mlflow.pyfunc


app = FastAPI()

mlflow.set_tracking_uri("http://mlflow:5000")
model = mlflow.pyfunc.load_model("models:/fraud_detection_model/Production")


@app.post("/send-transaction")
async def main(data=Body()):
    response = preproc(data)
    if isinstance(response, Exception):
        return JSONResponse(content={"Data is not valid": response}, status_code=400)
    prep_response = preproc_features(response)
    predict = await model.predict(prep_response)
    return JSONResponse(content={"Is fraud": predict})
    
    
    
    
    
