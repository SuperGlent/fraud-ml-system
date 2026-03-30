from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer
import os

"""database config file"""

#get env variables
pg_user = os.environ.get("DB_USERNAME")
pg_pass = os.environ.get("DB_PASSWORD")
pg_db = os.environ.get("POSTGRES_DB", "fraud_training")

#database uri
database_uri = f"postgresql://{pg_user}:{pg_pass}@db:5432/{pg_db}"

#base SQLAlchemy class
Base = declarative_base()

class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    

