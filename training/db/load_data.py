from .data_preproccess import Data
import dotenv
from .database import database_uri
from .models import Transaction

dotenv.load_dotenv("./.env")


dataset_uri = "goyaladi/fraud-detection-dataset"

def main_load_data():
    data_manager = Data(database_uri)
    raw_data = data_manager.load_local_data(dataset_uri)
    prep_data = data_manager.preproccess(raw_data=raw_data)
    data_manager.upload_data(prep_data, name="transactions")

