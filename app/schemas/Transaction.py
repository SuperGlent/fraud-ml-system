from pydantic import BaseModel
from datetime import datetime, date

#transaction scheme to validate data from user
class Transaction(BaseModel):
    Amount: float
    TransactionAmount: float
    Category: str 
    AccountBalance: float
    Timestamp: datetime
    LastLogin: date