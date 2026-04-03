import mlflow
from .prep_transaction import preproc_features
import pandas as pd

#class for managing ml model
class ModelManager:
    
    #initialize model and mlflow client
    def __init__(self):
        self.model = None
        self.model_uri = "models:/fraud_detection_model@champion"
        mlflow.set_tracking_uri("http://mlflow:5000")
        
    #load model
    def load_model(self):
        try:
            self.model = mlflow.pyfunc.load_model(self.model_uri)
            print("Model loaded succesfully!")
            
        except Exception as e:
            print("Model isn't available", e)
        
        
    #predict is user request is a fraud.
    def predict(self, data: pd.DataFrame):
        if self.model:
            pred = self.model.predict(data)
            return pred
            
        else:
            print(f"Check if model is available. Current model is: {self.model}")
            return None