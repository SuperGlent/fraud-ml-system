from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import mlflow
from mlflow.data import pandas_dataset
from data_preproccess import Data
from dotenv import load_dotenv

DB_PASSWORD = load_dotenv("../.env")["DB_PASSWORD"]
DB_USER = load_dotenv("../.env")["DB_USERNAME"]

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("fraud_detection")

with mlflow.start_run():
    
    data = Data(db_uri=f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432/fraud_db")
    data = data.get_data()
    data_x = data.drop("") #label
    data_y = data[""] #label
    X_train, Y_train, X_test, Y_test = train_test_split(data_x.to_numpy(), data_y.to_numpy())

    model = LogisticRegression()
    model.fit(X_train, Y_train)
    model1_info = mlflow.sklearn.log_model(model, name="log_regression_fraud")

    pred = model.predict(X=X_test)
    metrics_model = {"accuracy": accuracy_score(Y_test, pred), "roc_auc": roc_auc_score(Y_test, pred)}

    mlflow.log_metrics(metrics_model)




