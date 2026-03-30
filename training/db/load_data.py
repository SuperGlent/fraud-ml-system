from .data_preproccess import Data
import dotenv
from .database import database_uri
from .pydentic_models import validator

"""Load data file for airflow dag"""

dotenv.load_dotenv("./.env")


dataset_uri = "goyaladi/fraud-detection-dataset"

def main_load_data():
    data_manager = Data(database_uri)
    raw_data = data_manager.load_local_data(dataset_uri)
    prep_data = data_manager.preproccess(raw_data=raw_data)
    try:
        validator.validate(dataframe=prep_data, errors="raise")
    except ValueError:
        print("Validation failed!")
    data_manager.upload_data(prep_data, name="transactions")

