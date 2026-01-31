
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.audit import AuditMixin
from app.models.rol_permission import RolPermission
if TYPE_CHECKING:
    from app.models.rol import Rol



class PermissionBase(SQLModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id : int

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase, AuditMixin, table=True):
    id : int = Field(default=None, primary_key=True)

    rols : list["Rol"] = Relationship(back_populates="permissions",link_model=RolPermission)
