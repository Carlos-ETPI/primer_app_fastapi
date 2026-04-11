from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.database import SessionDep
from app.dependencies import CurrentUser
from app.models.rol_permission import RolPermission, RolPermissionCreate, RolPermissionRead

router = APIRouter(tags=["Rol-Permission"])

@router.post("/rol_permission",response_model=RolPermissionRead)
async def create_rol_permission(rol_permission_data : RolPermissionCreate, session : SessionDep, current_user: CurrentUser):
    rol_permission_db = RolPermission.model_validate(rol_permission_data.model_dump())
    session.add(rol_permission_db)
    session.commit()
    session.refresh(rol_permission_db)
    return rol_permission_db


@router.get("/rol_permission",response_model=list[RolPermissionRead])
async def get_rol_permissions(session : SessionDep, current_user: CurrentUser):
    return session.exec(select(RolPermission)).all()
