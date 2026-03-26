import mlflow
from .prep_transaction import preproc_features

class ModelManager:
    
    def __init__(self):
        self.model = None
        self.model_uri = "models:/fraud_detection_model/Production"
        mlflow.set_tracking_uri("http://mlflow:5000")
        
    def load_model(self):
        
        try:
            self.model = mlflow.pyfunc.load_model(self.model_uri)
            print("Model loaded succesfully!")
            
        except Exception as e:
            print("Model isn't available", e)
        
        
    def predict(self, data):
        if self.model:
            data = preproc_features(data)
            pred = self.model.predict(data)
            return pred
            
        else:
            print(f"Check if model is available. Current model is: {self.model}")
            return None