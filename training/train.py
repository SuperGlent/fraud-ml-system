from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import mlflow
from mlflow.tracking import MlflowClient
from db.data_preproccess import Data
from db.database import database_uri
from imblearn.over_sampling import SMOTE

"""Main training script with mflow tracking"""

mlflow.set_tracking_uri("http://mlflow:5000") #set mlflow client 
mlflow.set_experiment("fraud_detection") #set new experiment

#main function
def train_model():
    with mlflow.start_run(run_name="Logistic_Regression_SMOTE"):
        #downloading data from db
        data_manager = Data(db_uri=database_uri)
        data = data_manager.get_data()
        
        # features managing
        drop_cols = ['FraudIndicator', 'Timestamp', 'Timestamp1', 'LastLogin']
        existing_drop_cols = [c for c in drop_cols if c in data.columns]
        
        #X and Y columns
        X = data.drop(existing_drop_cols, axis=1)
        Y = data['FraudIndicator']
        
        #SMOTE for balancing classes destribution
        smote = SMOTE(random_state=42)
        X_resampled, Y_resampled = smote.fit_resample(X, Y)
        
        #train-test split
        X_train, X_test, Y_train, Y_test = train_test_split(
            X_resampled, Y_resampled, random_state=42, test_size=0.2
        )

        #Training
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, Y_train)
        
        #Model logging
        model_info = mlflow.sklearn.log_model(
            sk_model=model, 
            artifact_path="model", 
            registered_model_name="fraud_detection_model"
        )

        #Roc-Auc metrics
        pred = model.predict(X_test)
        pred_proba = model.predict_proba(X_test)[:, 1] # Вероятность класса 1
        
        metrics = {
            "accuracy": accuracy_score(Y_test, pred),
            "roc_auc": roc_auc_score(Y_test, pred_proba) # ТУТ БЫЛА ОШИБКА
        }
        mlflow.log_metrics(metrics)

        #hand over the model with client
        client = MlflowClient()
        #get the last version
        latest_version = client.get_latest_versions("fraud_detection_model", stages=["None"])[0].version
        
        #Model version trasition
        client.transition_model_version_stage(
            name="fraud_detection_model",
            version=latest_version,
            stage="Production"
        )

        print(f"Successfully trained version {latest_version} and moved to Production.")

#entry point
if __name__ == "__main__":
    train_model()