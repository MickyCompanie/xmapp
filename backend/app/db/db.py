import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

load_dotenv()

class Base(DeclarativeBase, MappedAsDataclass):
    pass

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()