"""Service database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_session():
    """Returns database session"""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
