from database import SessionLocal
from models.user import User
from passlib.context import CryptContext
from models.application import Application

bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')

db = SessionLocal()

new_user = User(
    username = 'test1',
    email = 'test1@gmail.com',
    hashed_password = bcrypt_context.hash('test1'),
    is_active = True,
    role = "user"
)

db.add(new_user)
db.commit()
db.refresh(new_user)


db.close()