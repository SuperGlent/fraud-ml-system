from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services.prep_transaction import preproc_features
from services.ModelManager import ModelManager
from contextlib import asynccontextmanager
from fastapi.exceptions import HTTPException
from .schemas.Transaction import Transaction

model = ModelManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    model.load_model()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.post("/send-transaction")
async def main(data: Transaction):
    try:
        prep_tr = preproc_features(data)
        predict = model.predict(prep_tr)
        
        if predict is None:
            raise HTTPException(status_code=503, detail="Model is not available")
            
        return JSONResponse(content={"Is fraud": int(predict[0])})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/admin/reload-model")
def reload_model():
    model.load_model()
    return {"status": "model reloaded"}
    
    
