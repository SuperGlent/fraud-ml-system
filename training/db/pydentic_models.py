from pydantic import BaseModel
from datetime import datetime, date
from pandantic import Pandantic


"""Pydantic models and pandas validator for those models"""

class Transaction(BaseModel):
    FraudIndicator: int 
    Category: int 
    TransactionAmoun: float 
    Gap: int 
    Hour: int 
    Amount: float 
    AccountBalance: float 
    
validator = Pandantic(schema=Transaction)
