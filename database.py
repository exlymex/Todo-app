from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLACHEMY_DATABASE_URL = 'sqlite:///todoapp.db'
SQLACHEMY_DATABASE_URL = 'postgresql://postgres:123123@localhost:5432/TodoApplicationDatabase'

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
