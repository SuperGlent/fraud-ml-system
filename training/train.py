from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import mlflow
from mlflow.tracking import MlflowClient
from db.data_preproccess import Data
from db.database import database_uri
from imblearn.over_sampling import SMOTE

"""Main training script with mflow tracking"""

mlflow.set_tracking_uri("http://mlflow:5000") # Connect to remote MLflow server
mlflow.set_experiment("fraud_detection") #set new experiment

#main function
def train_model():
    with mlflow.start_run(run_name="Descision_Tree_SMOTE"):
        #downloading data from db
        data_manager = Data(db_uri=database_uri)
        data = data_manager.get_data()
        
        # features managing
        drop_cols = ['FraudIndicator', 'Timestamp', 'Timestamp1', 'LastLogin']
        existing_drop_cols = [c for c in drop_cols if c in data.columns]
        
        expected_order = ['Amount', 'TransactionAmount', 'Category', 'AccountBalance', 'Hour', 'gap']
        
        #X and Y columns
        X = data.drop(existing_drop_cols, axis=1)[expected_order]
        Y = data['FraudIndicator']
        
        #SMOTE for balancing classes destribution
        smote = SMOTE(random_state=42)
        X_resampled, Y_resampled = smote.fit_resample(X, Y)
        
        #train-test split
        X_train, X_test, Y_train, Y_test = train_test_split(
            X_resampled, Y_resampled, random_state=42, test_size=0.2
        )

        #Training
        model = DecisionTreeClassifier()
        model.fit(X_train, Y_train)
        
        #Roc-Auc metrics
        pred = model.predict(X_test)
        pred_proba = model.predict_proba(X_test)[:, 1] # Вероятность класса 1
        
        metrics = {
            "accuracy": accuracy_score(Y_test, pred),
            "roc_auc": roc_auc_score(Y_test, pred_proba) # ТУТ БЫЛА ОШИБКА
        }
        mlflow.log_metrics(metrics)

        
        #Model logging
        mlflow.sklearn.log_model(
            sk_model=model, 
            artifact_path="model",
            registered_model_name="fraud_detection_model"
        )

        #hand over the model with client
        client = MlflowClient()
        
        #get the last version
        run_id = mlflow.active_run().info.run_id
        model_versions = client.search_model_versions(f"run_id='{run_id}'")
        model_version = model_versions[0].version
        
        try: 
            champion = client.get_model_version_by_alias(
                name="fraud_detection_model",
                alias="champion"
            )
            champion_run = client.get_run(champion.run_id)
            old_auc = champion_run.data.metrics["roc_auc"]
            promote = metrics["roc_auc"] > old_auc
        
        except:
            promote = True
            
        if promote:
            client.set_registered_model_alias(
                name="fraud_detection_model",
                alias="champion",
                version=model_version
            )
            print(f"Successfully trained version {model_version} and moved to Production.")
        else:
            client.set_registered_model_alias(
                name="fraud_detection_model",
                alias="candidate",
                version=model_version
            )
            print(f"Successfully trained version, but previous version has a better performance. Current model is {champion.version}")

#entry point
if __name__ == "__main__":
    train_model()