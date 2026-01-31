from fastapi import FastAPI

from app.routers import category, movements, product


app = FastAPI(title="API de Gestión de Inventario")
app.include_router(category.router)
app.include_router(product.router)
app.include_router(movements.router)

# @app.get("/")
# async def root():
#     return {"message": "Hola, Luis!"}
