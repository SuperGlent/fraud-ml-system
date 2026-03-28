from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer
import os

pg_user = os.environ.get("POSTGRES_USER", "airflow")
pg_pass = os.environ.get("POSTGRES_PASSWORD", "airflow")
pg_db = os.environ.get("POSTGRES_DB", "fraud_training")


database_uri = f"postgresql://{pg_user}:{pg_pass}@db:5432/{pg_db}"

Base = declarative_base()

class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    

