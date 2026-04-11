from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.database import SessionDep
from app.dependencies import CurrentUser
from app.models.rol import Rol, RolCreate, RolRead

router = APIRouter(tags=["Roles"])

@router.post("/roles",response_model=RolRead)
async def create_rol(rol_data : RolCreate, session : SessionDep, current_user: CurrentUser):
    rol_dict = rol_data.model_dump()
    rol_dict["created_by"] = current_user.username
    rol_db = Rol.model_validate(rol_dict)
    session.add(rol_db)
    session.commit()
    session.refresh(rol_db)
    return rol_db


@router.get("/roles",response_model=list[RolRead])
async def get_roles(session : SessionDep, current_user: CurrentUser):
    return session.exec(select(Rol)).all()
