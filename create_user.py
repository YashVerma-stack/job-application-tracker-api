from database import SessionLocal
from models.user import User
from passlib.context import CryptContext
from models.application import Application


bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')

db = SessionLocal()

new_user = User(
    username = 'test3',
    email = 'test3@gmail.com',
    hashed_password = bcrypt_context.hash('test3'),
    is_active = True,
    role = "user"
)

db.add(new_user)
db.commit()
db.refresh(new_user)


db.close()