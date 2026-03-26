from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import mlflow
from mlflow.tracking import MlflowClient
from training.db.data_preproccess import Data
from .db.database import database_uri
from imblearn.over_sampling import SMOTE

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("fraud_detection")

with mlflow.start_run():
    
    data = Data(db_uri=database_uri)
    data = data.get_data()
    
    X = data.drop(['FraudIndicator','Timestamp','Timestamp1','LastLogin'], axis=1)
    Y = data['FraudIndicator']
    smote = SMOTE(random_state=42)
    X_resampled, Y_resampled = smote.fit_resample(X, Y)
    X_train, X_test, Y_train, Y_test = train_test_split(X_resampled, Y_resampled, random_state=42, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, Y_train)
    model1_info = mlflow.sklearn.log_model(sk_model=model, artifact_path="log_regression_fraud", registered_model_name="fraud_detection_model")

    pred = model.predict(X=X_test)
    metrics_model = {"accuracy": accuracy_score(Y_test, pred), "roc_auc": roc_auc_score(Y_test, pred)}

    mlflow.log_metrics(metrics_model)

    client = MlflowClient()
    model_version = client.get_latest_versions("fraud_detection_model", stages=["None"])[0].version
    client.transition_model_version_stage(
    name="fraud_detection_model",
    version=model_version,
    stage="Production"
    )



