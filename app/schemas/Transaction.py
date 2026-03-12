from pydentic import BaseModel, PositiveInt, Base64Str, PositiveFloat, NonNegativeFloat, Field, NonNegativeInt
from datetime import datetime


class Transaction(BaseModel):
    
    TransactionID: PositiveInt
    Category: str
    TransactionAmount: PositiveFloat
    AnomalyScore: NonNegativeFloat
    MerchantID: PositiveInt
    Amount: PositiveInt
    CustomerID: PositiveInt
    Name: str
    Age: int = Field(gt=0, le=120)
    Address: str
    AccountBalance: NonNegativeFloat
    LastLogin: datetime
    SuspiciousFlag: NonNegativeInt
        