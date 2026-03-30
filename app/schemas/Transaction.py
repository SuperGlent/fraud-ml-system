from pydantic import BaseModel
from datetime import datetime, date

#transaction scheme to validate data from user
class Transaction(BaseModel):
    Category: str 
    TransactionAmount: float
    AnomalyScore: float
    Timestamp: datetime
    LastLogin: date
    Amount: float
    AccountBalance: float
    SuspiciousFlag: int