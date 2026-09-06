from fastapi import FastAPI
from routers import auth, applications, admin
from database import Base, engine
from models.user import User
from models.application import Application


Base.metadata.create_all(bind=engine)

app = FastAPI(title = 'JOB_APPLICATION_TRACKER_API')

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(admin.router)

@app.get('/')
async def get_all():
    return {'msg': "hello there"}
