from database import SessionLocal
from fastapi import Depends, HTTPException
from typing import Annotated
from config import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        role: str = payload.get('role')
        
        if username is None or id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ='UNAUTHORIZED USER' )
        return {'username': username, 'id': id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ='UNAUTHORIZED USER' )
    
def get_current_admin(user: user_dependency):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Admin access required')
    
    return user
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
admin_dependency = Annotated[dict, Depends(get_current_admin)]