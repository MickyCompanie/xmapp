from sqlalchemy import create_engine
from app.db import Base, SessionLocal
from app.config import Config


engine = create_engine(Config.DATABASE_URL, echo=True)
SessionLocal.configure(bind=engine)
