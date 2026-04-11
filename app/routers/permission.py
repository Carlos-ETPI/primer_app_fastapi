from fastapi import APIRouter, HTTPException,status
from sqlmodel import select

from app.database import SessionDep
from app.dependencies import CurrentUser
from app.models.permission import Permission, PermissionCreate, PermissionRead

router = APIRouter(tags=["Permissions"])

@router.post("/permissions",response_model=PermissionRead)
async def create_permission(permission_data : PermissionCreate, session : SessionDep, current_user: CurrentUser):
    permission_db = Permission.model_validate(permission_data.model_dump())
    session.add(permission_db)
    session.commit()
    session.refresh(permission_db)
    return permission_db


@router.get("/permissions",response_model=list[PermissionRead])
async def get_permissions(session : SessionDep, current_user: CurrentUser):
    return session.exec(select(Permission)).all()
