import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
import os
import kagglehub

class Data():
    
    __tablename__ = "transactions"
    
    def __init__(self, db_uri: str):
        self.engine = sa.create_engine(db_uri) 
        self.connection = self.engine.connect()
        
            
    @staticmethod
    def load_local_data(uri) -> pd.DataFrame:
        path = kagglehub.download_dataset(uri)
        file_list = []
        for i, file in enumerate(os.listdir(path)):        
            with open(str(path).join(file)) as datafile:
                df = pd.read_csv(datafile)
                file_list.append(df)
        return pd.concat(file_list)
        

    def get_data(self):
        query = "SELECT * FROM transactions"
        data = pd.read_sql(query, self.connection)
        return data
        
    def preproccess(self, raw_data: pd.DataFrame):
        pass
        
    
    def upload_data(self, data: pd.DataFrame, name="transactions", if_exists="replace"):
        data.to_sql(name=name, 
                    con=self.connection, 
                    if_exists=if_exists)
        