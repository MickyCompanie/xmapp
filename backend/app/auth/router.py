from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.config import Config
from app.db import get_db
from app.auth.utils import verify_password, create_access_token, create_refresh_token
from app.user.model import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import jwt
from app.auth.schemas import RefreshTokenRequest


auth_router = APIRouter()
@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="this user is deactivated.")

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post('/refresh', status_code=status.HTTP_200_OK)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(body.refresh_token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise credentials_exception

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY)
    new_access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }