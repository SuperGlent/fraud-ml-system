from data_preproccess import Data
import os
import dotenv

dotenv.load_dotenv("./.env")

dataset_uri = "goyaladi/fraud-detection-dataset"
database_uri = f"postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@db:5432/fraud_db"

def main_load_data():
    data = Data(database_uri)
    raw_data = data.load_local_data(dataset_uri)
    prep_data = data.preproccess(raw_data=raw_data)
    data.upload_data(prep_data)

