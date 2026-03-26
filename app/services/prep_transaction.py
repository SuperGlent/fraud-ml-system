from schemas import Transaction
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preproc_features(transaction: Transaction):
    # Превращаем Pydantic объект в словарь, а затем в DataFrame (1 строка)
    data = transaction.model_dump()
    df = pd.DataFrame([data])
    
    # Логика признаков
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['LastLogin'] = pd.to_datetime(df['LastLogin'])
    df['Hour'] = df['Timestamp'].dt.hour
    df['gap'] = (df['Timestamp'] - df['LastLogin']).dt.days.abs()
    
    # Для Category: если модель ожидает число, 
    # нужно использовать тот же LabelEncoder, что и при обучении.
    # Пока просто приведем к коду категории, если это строка.
    df['Category'] = df['Category'].astype('category').cat.codes
    
    # Удаляем лишнее, что не идет в модель (согласно train.py)
    # Оставляем только те колонки, на которых училась модель
    cols_to_drop = ['Timestamp', 'LastLogin']
    return df.drop(columns=cols_to_drop)