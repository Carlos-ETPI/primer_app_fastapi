from sqlmodel import Field, SQLModel

from app.models.audit import AuditMixin


class UserRolBase(SQLModel):
    user_id : int = Field(foreign_key="use.id")
    rol_id : int = Field(foreign_key="rol.id")


class UserRolCreate(UserRolBase):
    pass


class UserRolRead(UserRolBase):
    pass


class UserRolUpdate(UserRolBase):
    pass    


class UserRol(UserRolBase,AuditMixin,table=True):
    user_id : int = Field(default=None,foreign_key="user.id", primary_key=True)
    rol_id : int = Field(default=None, foreign_key="rol.id", primary_key=True)