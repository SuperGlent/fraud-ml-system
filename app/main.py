from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services.prep_transaction import preproc_features
from services.ModelManager import ModelManager
from contextlib import asynccontextmanager
from fastapi.exceptions import HTTPException
from schemas.Transaction import Transaction


"""Main file for fast-api application"""
#model manager object
model = ModelManager()

#creating lifespan for immediate model loading when start app
@asynccontextmanager
async def lifespan(app: FastAPI):
    model.load_model()
    yield
    
app = FastAPI(lifespan=lifespan)

#send transaction end-point return "isfraud" flag true or false
@app.post("/send-transaction")
async def main(data: Transaction):
    try:
        prep_tr = preproc_features(data)
        predict = model.predict(prep_tr)
        
        if predict is None:
            raise HTTPException(status_code=503, detail="Model is not available")
            
        return JSONResponse(content={"Is fraud": bool(predict[0])})
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))

#end-point for model reloading
@app.post("/admin/reload-model")
def reload_model():
    model.load_model()
    return {"status": "model reloaded"}
    
    
