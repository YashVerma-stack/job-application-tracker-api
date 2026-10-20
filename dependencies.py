from database import SessionLocal
from fastapi import Depends, HTTPException
from typing import Annotated
from config import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.user import User

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
        
def get_current_user(token: Annotated[str, Depends(oauth_bearer)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token", headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        token_role = payload.get("role")
        
        if  (
            not isinstance(username, str)
            or not username
            or type(user_id) is not int
            or user_id <= 0
            or not isinstance(token_role, str)
        ):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    if user.username != username:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
        
    return {
        'username': user.username,
        'id': user.id,
        'role': user.role
    }
    
user_dependency = Annotated[dict, Depends(get_current_user)]

def get_current_admin(user: user_dependency):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Admin access required')
    
    return user
    
admin_dependency = Annotated[dict, Depends(get_current_admin)]