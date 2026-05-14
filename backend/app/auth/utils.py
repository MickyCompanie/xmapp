from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.config import Config

# moteur de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY) 
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=Config.REFRESH_TOKEN_EXPIRY))