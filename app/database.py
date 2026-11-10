from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings

Base = declarative_base()

def get_engine():
    try:
        return create_engine(settings.DATABASE_URL)
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
