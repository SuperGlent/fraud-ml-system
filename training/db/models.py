from database import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Transaction(Base):
    FraudIndicator: Mapped[int]
    Category: Mapped[int]
    TransactionAmount: Mapped[float]
    AnomalyScore: Mapped[float]
    Gap: Mapped[int]
    Hour: Mapped[int]
    Timestemp: Mapped[datetime.datetime]
    LastLogin: Mapped[datetime.date]
    Amount: Mapped[float]
    AccountBalance: Mapped[float]
    SuspiciousFlag: Mapped[int]