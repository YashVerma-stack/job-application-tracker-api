from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from starlette import status
from schema.user import CreateUser, UserResponse
from schema.token import Token
from models.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timezone, timedelta, datetime
from jose import jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import db_dependency, user_dependency, admin_dependency


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(['bcrypt'], deprecated = 'auto')


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def get_access_token(username: str, id: int, role: str, expiry_delta: timedelta):
    payload = ({'sub': username, 'id': id, 'role': role})
    expires = datetime.now(timezone.utc) + expiry_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/', response_model=UserResponse, status_code = status.HTTP_201_CREATED)
async def create_user(db: db_dependency, new_user: CreateUser):
    create_new_user = User(
        username = new_user.username,
        email = new_user.email,
        hashed_password = bcrypt_context.hash(new_user.password),
        is_active = True
    )
    
    db.add(create_new_user)
    db.commit()
    db.refresh(create_new_user)
    
    return create_new_user

@router.post('/token', status_code = status.HTTP_200_OK, response_model = Token)
async def login_to_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = 'Unauthorized User')
    token = get_access_token(user.username, user.id, user.role, timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {'access_token': token, 'token_type': 'bearer'}  

@router.get('/me', status_code = status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = 'user is not authorized')
    return db.query(User).filter(User.id == user.get('id')).first()


@router.get('/admin-test')
async def admin_test(admin: admin_dependency):
    return {'msg': 'You are an admin'}