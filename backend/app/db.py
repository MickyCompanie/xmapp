import os 

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

load_dotenv()

class Base(DeclarativeBase, MappedAsDataclass):
    pass

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)