from pydantic import BaseModel
from datetime import datetime, date
from pandantic import Pandantic


"""Pydantci models and pandas validator for those models"""

class Transaction(BaseModel):
    FraudIndicator: int 
    Category: int 
    TransactionAmoun: float 
    AnomalyScore: float 
    Gap: int 
    Hour: int 
    Amount: float 
    AccountBalance: float 
    SuspiciousFlag: int 
    
validator = Pandantic(schema=Transaction)
