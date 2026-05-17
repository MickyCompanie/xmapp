from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.db import get_db
from app.config import Config
from app.user import services as user_service 
from app.user.model import User, UserRole
from app.auth.schemas import TokenData

# dit à FastAPI la route de login pour le "Authorize" du Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{Config.PREFIX}{Config.VERSION}/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def must_be_authenticated(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return True

def authorized_role(*allowed_roles: UserRole | str):
    roles_as_strings = {
        r.value if isinstance(r, UserRole) else str(r) 
        for r in allowed_roles
    }

    def _role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user is not active"
            )
            
        if current_user.role.value not in roles_as_strings:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong role to access this endpoint"
            )
            
        return current_user

    return _role_checker