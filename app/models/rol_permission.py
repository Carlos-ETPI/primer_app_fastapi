
from sqlmodel import Field, SQLModel

from app.models.audit import AuditMixin


class RolPermissionBase(SQLModel):
    rol_id : int = Field(foreign_key="rol.id")
    permission_id :int = Field(foreign_key="permission.id")

class RolPermissionCreate(RolPermissionBase):
    pass

class RolPermissionRead(RolPermissionBase):
    pass

class RolPermissionUpdate(RolPermissionBase):
    pass 

class RolPermission( RolPermissionBase, AuditMixin, table=True):
    rol_id :int = Field(default=None, foreign_key="rol.id", primary_key=True)
    permission_id :int = Field(default=None, foreign_key="permission.id", primary_key=True)