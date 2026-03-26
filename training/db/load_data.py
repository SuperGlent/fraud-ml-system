from .data_preproccess import Data
import dotenv
from database import database_uri
from .models import Transaction

dotenv.load_dotenv("./.env")


dataset_uri = "goyaladi/fraud-detection-dataset"

def main_load_data():
    data = Data(database_uri)
    raw_data = data.load_local_data(dataset_uri)
    prep_data = data.preproccess(raw_data=raw_data)
    validated = Transaction(prep_data)
    data.upload_data(validated)

