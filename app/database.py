import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings

Base = declarative_base()

def get_engine():
    try:
        # Check if using SQLite to add necessary connect_args for multithreading in tests
        db_url = getattr(settings, "DATABASE_URL", "sqlite:///./test.db")
        connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
        return create_engine(db_url, connect_args=connect_args)
    except SQLAlchemyError as e:
        print(f"Error creating engine: {e}")
        raise

def get_sessionmaker(engine):
    return sessionmaker(autoflush=False, bind=engine)

engine = get_engine()
SessionLocal = get_sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        