import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
import os
import kagglehub
from sklearn.preprocessing import LabelEncoder


class Data():

    def __init__(self, db_uri: str):
        self.engine = sa.create_engine(db_uri) 
        self.connection = self.engine.connect()
        
            
    @staticmethod
    def load_local_data(uri) -> pd.DataFrame:
        path = kagglehub.download_dataset(uri)
        links = [os.listdir(path + f"/Data/{i}") + [i] for i in os.listdir(path + "/Data")]
        dfs = {}
        for link in links:
            for l in link:
                try:
                    dfs[l] = pd.read_csv(path + f"/Data/{link[-1]}/{l}")
                except FileNotFoundError as e:
                    continue
        data1 = pd.merge(dfs["transaction_metadata.csv"], dfs["transaction_records.csv"], on="TransactionID")
        data1 = pd.merge(data1, dfs["amount_data.csv"], on="TransactionID")
        data1 = pd.merge(data1, dfs["anomaly_scores.csv"], on="TransactionID")
        data1 = pd.merge(data1, dfs["fraud_indicators.csv"], on="TransactionID")
        data1 = pd.merge(data1, dfs["transaction_category_labels.csv"], on="TransactionID")
        data1 = pd.merge(data1, dfs["merchant_data.csv"], on="MerchantID")
        data2 = pd.merge(dfs["suspicious_activity.csv"], dfs["customer_data.csv"], on="CustomerID")
        data2 = pd.merge(data2, dfs["account_activity.csv"], on="CustomerID")
        data = pd.merge(data1, data2, on="CustomerID")
        return data
                

    def get_data(self):
        query = "SELECT * FROM transactions"
        data = pd.read_sql(query, self.connection)
        return data
        
    def preproccess(self, raw_data: pd.DataFrame):
        raw_data['Timestamp1'] = pd.to_datetime(raw_data['Timestamp'])
        raw_data['Hour'] = raw_data['Timestamp1'].dt.hour
        raw_data['LastLogin'] = pd.to_datetime(raw_data['LastLogin'])
        raw_data['gap'] = (raw_data['Timestamp1'] - raw_data['LastLogin']).dt.days.abs()
        
        label_encoder = LabelEncoder()
        raw_data['Category'] = label_encoder.fit_transform(raw_data['Category'])
        return raw_data
        
    
    def upload_data(self, data: pd.DataFrame, name="transactions", if_exists="replace"):
        data.to_sql(name=name, 
                    con=self.connection, 
                    if_exists=if_exists)
        