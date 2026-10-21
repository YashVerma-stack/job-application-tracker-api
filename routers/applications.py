from fastapi import APIRouter, HTTPException, Query
from starlette import status
from schema.application import ApplicationResponse, CreateApplication, ApplicationStatus
from dependencies import user_dependency, db_dependency
from models.application import Application
from typing import List
from sqlalchemy import or_

router = APIRouter(
    prefix = '/application',
    tags = ['applications']
)



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ApplicationResponse])
async def get_all_applicaattion_of_user(
        user: user_dependency,
        db: db_dependency,
        application_status: ApplicationStatus | None = None,
        company: str | None = None,
        search: str | None = None,
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100)
    ):
    
    query = db.query(Application).filter(Application.user_id == user.get('id'))

    if application_status is not None:
        query = query.filter(Application.status == application_status)
        
        
    if company is not None:
        company = company.strip().casefold()
        if company:
            query = query.filter(
                Application.company.ilike(f"%{company}%")
            )
        
    if search is not None:
        search = search.strip()
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Application.job_title.ilike(search_pattern),
                    Application.company.ilike(search_pattern)
                )
            )
        
    return (
        query
        .order_by(Application.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get('/{id}', status_code = status.HTTP_200_OK, response_model = ApplicationResponse)
async def get_application_by_id(user: user_dependency, db: db_dependency ,id: int):
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "user is unauthenticated")
    application_detail = db.query(Application).filter(Application.id == id).filter(Application.user_id == user.get('id')).first()
    if application_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Application not found')
    return application_detail
    

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ApplicationResponse)
async def craete_new_application(db: db_dependency, user: user_dependency, new_application: CreateApplication):

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "user is unauthenticated")
        
    create_application = Application(
        user_id = user.get('id'),
        company = new_application.company,
        job_title = new_application.job_title,
        location = new_application.location,
        salary = new_application.salary,
        status = new_application.status,
        applied_date = new_application.applied_date,
        notes = new_application.notes
    )
    
    db.add(create_application)
    db.commit()
    db.refresh(create_application)
    
    return create_application

@router.put('/update/{application_id}', status_code=status.HTTP_200_OK, response_model = ApplicationResponse)
async def update_application(db: db_dependency, user: user_dependency, application_id: int, new_application: CreateApplication):
    
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "user is unauthenticated")
    
    existing_application = db.query(Application).filter(Application.id == application_id, Application.user_id == user.get('id')).first()
    
    if existing_application is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'application is not found')
    
    existing_application.company = new_application.company
    existing_application.job_title = new_application.job_title
    existing_application.location = new_application.location
    existing_application.salary = new_application.salary
    existing_application.status = new_application.status
    existing_application.applied_date = new_application.applied_date
    existing_application.notes = new_application.notes
    

    db.commit()
    db.refresh(existing_application)
    
    return existing_application


@router.delete('/delete/{application_id}', status_code = status.HTTP_200_OK)
async def delete_application(db: db_dependency, user: user_dependency, application_id: int):
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "user is unauthenticated")
    existing_application = db.query(Application).filter(Application.user_id == user.get('id')).filter(Application.id == application_id).first()
    if existing_application is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='application is not found')
    
    db.delete(existing_application)
    db.commit()
    
    return {'msg': 'Application is Deleted'}
