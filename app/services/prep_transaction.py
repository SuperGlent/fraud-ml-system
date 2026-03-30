from schemas import Transaction
import pandas as pd
from sklearn.preprocessing import LabelEncoder

#function for preparing data from user, as we have timestamp and last login features converted to gap in a model.
def preproc_features(transaction: Transaction):
    #pydentic model to dict and to df frame then
    data = transaction.model_dump()
    df = pd.DataFrame([data])
    
    #Feauture engineering
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['LastLogin'] = pd.to_datetime(df['LastLogin'])
    df['Hour'] = df['Timestamp'].dt.hour
    df['gap'] = (df['Timestamp'] - df['LastLogin']).dt.days.abs()
    
    #making category num feature if not
    df['Category'] = df['Category'].astype('category').cat.codes
    
    #deleting garbage
    cols_to_drop = ['Timestamp', 'LastLogin']
    return df.drop(columns=cols_to_drop)