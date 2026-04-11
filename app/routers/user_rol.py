from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.database import SessionDep
from app.dependencies import CurrentUser
from app.models.user_rol import UserRol, UserRolCreate, UserRolRead

router = APIRouter(tags=["User-Rol"])

@router.post("/user_rol",response_model=UserRolRead)
async def create_user_rol(user_rol_data : UserRolCreate, session : SessionDep, current_user: CurrentUser):
    user_rol_db = UserRol.model_validate(user_rol_data.model_dump())
    session.add(user_rol_db)
    session.commit()
    session.refresh(user_rol_db)
    return user_rol_db


@router.get("/user_rol",response_model=list[UserRolRead])
async def get_user_rols(session : SessionDep, current_user: CurrentUser):
    return session.exec(select(UserRol)).all()
