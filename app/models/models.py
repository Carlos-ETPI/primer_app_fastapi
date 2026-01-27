from typing import Optional
from sqlmodel import SQLModel, Field
from .audit import AuditMixin


"""Modelos de Producto"""
class ProductBase(SQLModel):
    name: str = Field(index=True)
    sku: str = Field(unique=True, index=True)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(foreign_key="category.id")

class ProductCreate(ProductBase):
    pass

class Product(ProductBase, AuditMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductRead(ProductBase):
    id: int


"""Modelos de Categoría de Producto"""
class CategoryBase(SQLModel):
    name : str = Field(index=True)
    description: Optional[str] = Field(default=None)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase, AuditMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CategoryRead(CategoryBase):
    id: int


"""Modelos de Movimiento de Inventario"""
class InventoryMovementBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    reason: str = Field(min_length=3)

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovement(InventoryMovementBase, AuditMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class InventoryMovementRead(InventoryMovementBase):
    id: int
