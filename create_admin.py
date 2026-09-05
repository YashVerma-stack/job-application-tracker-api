from database import SessionLocal
from models.user import User
from passlib.context import CryptContext

bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')

db = SessionLocal()

admin_user = User(
    username='test2',
    email = 'test2@gmail.com',
    hashed_password = bcrypt_context.hash("test2"),
    is_active = True,
    role = "admin"
)

db.add(admin_user)
db.commit()

db.close()