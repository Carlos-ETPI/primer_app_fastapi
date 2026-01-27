from fastapi import FastAPI
from app.routers import category


app = FastAPI(title="API de Gestión de Inventario")
app.include_router(category.router)

# @app.get("/")
# async def root():
#     return {"message": "Hola, Luis!"}
