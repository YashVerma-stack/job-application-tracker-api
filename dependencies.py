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
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        role: str = payload.get('role')
        
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ='UNAUTHORIZED USER' )
        
        user = db.query(User).filter(User.id == id).first()
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "user not found")
        
        if not user.is_active:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'user is inactive')
        
        return {
            'username': user.username,
            'id': user.id,
            'role': user.role
        }
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ='UNAUTHORIZED USER' )
    
user_dependency = Annotated[dict, Depends(get_current_user)]

def get_current_admin(user: user_dependency):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Admin access required')
    
    return user
    
admin_dependency = Annotated[dict, Depends(get_current_admin)]