from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List
from starlette import status
from schema.user import UserResponse
from dependencies import admin_dependency, db_dependency
from models.user import User


router = APIRouter(
    prefix = '/admin',
    tags = ['admin']
)

@router.get('/users', response_model = List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_user(admin: admin_dependency, db: db_dependency):
    user = db.query(User).all()
    return user

        
@router.delete('/users/{user_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(admin: admin_dependency, db: db_dependency, user_id: int = Path(gt = 0)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
    db.delete(existing_user)
    db.commit()
    

@router.patch('/users/{user_id}/', status_code = status.HTTP_204_NO_CONTENT)
async def toggle_activity_of_user(admin: admin_dependency, db: db_dependency, user_id: int = Path(gt = 0)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
    user.is_active = not user.is_active
    
    db.commit()
    
        
    


    
    
    