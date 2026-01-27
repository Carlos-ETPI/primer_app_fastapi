from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class AuditMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    
    created_by: Optional[str] = Field(default="system")
    updated_by: Optional[str] = Field(default=None)