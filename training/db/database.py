from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
import os

database_uri = f"postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@db:5432/fraud_training"

class Base(DeclarativeBase):
    
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
    
    
    

