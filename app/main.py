from fastapi import FastAPI

from app.routers import category, movements, product, login,user
from app.core.config import settings

app = FastAPI(title="API de Gestión de Inventario")
app.include_router(category.router)
app.include_router(product.router)
app.include_router(movements.router)
app.include_router(login.router,prefix=settings.API_V1_STR)
app.include_router(user.router)

# @app.get("/")
# async def root():
#     return {"message": "Hola, Luis!"}
