from database import Base, CustomBase
from sqlalchemy import Column, Integer, Float, DateTime, Date
import datetime

class Transaction(Base, CustomBase):
    FraudIndicator = Column(Integer)
    Category = Column(Integer)
    TransactionAmount = Column(Float)
    AnomalyScore = Column(Float)
    Gap = Column(Integer)
    Hour = Column(Integer)
    Timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    LastLogin = Column(Date)
    Amount = Column(Float)
    AccountBalance = Column(Float)
    SuspiciousFlag = Column(Integer)