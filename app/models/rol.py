from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from app.models.audit import AuditMixin
from app.models.rol_permission import RolPermission
from app.models.user_rol import UserRol


if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.users import User

class RolBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description : str = Field(default=None)

class RolCreate(RolBase):
    pass


class RolRead(RolBase):
    id : int


class Rol(RolBase, AuditMixin, table=True ):
    id : int = Field(default=None, primary_key=True)

    users : list["User"] = Relationship(back_populates="rols",link_model=UserRol)
    permissions : list["Permission"] = Relationship(back_populates="rols",link_model=RolPermission)
