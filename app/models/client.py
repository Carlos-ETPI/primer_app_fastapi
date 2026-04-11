import uuid
from uuid import uuid4
from sqlmodel import SQLModel, Field
class Client(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid4, primary_key=True)
    client_id: str = Field(unique=True, index=True)
    client_secret_hash: str
    name: str  # Ejemplo: "Servicio de Inventario"
    is_active: bool = True