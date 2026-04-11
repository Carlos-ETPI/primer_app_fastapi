from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import CurrentUser
from app.routers import category, login_client, movements, permission, product, login, rol, rol_permission,user, user_rol
from app.core.config import settings

"""para desactivar la documentación de la API, se puede establecer el parámetro docs_url a None al crear la instancia de FastAPI. Esto evitará que se genere la documentación interactiva de Swagger UI.
,docs_url=None, redoc_url=None
"""
app = FastAPI(title="API de Gestión de Inventario")
app.include_router(category.router)
app.include_router(product.router)
app.include_router(movements.router)
app.include_router(login.router,prefix=settings.API_V1_STR)
app.include_router(user.router)
app.include_router(permission.router)
app.include_router(rol.router)
app.include_router(rol_permission.router)
app.include_router(user_rol.router)
app.include_router(login_client.router, prefix=settings.API_V1_STR)


if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        #allow_origins=settings.all_cors_origins,
        allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
    ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# @app.get("/")
# async def root(current_user: CurrentUser = Depends(SecurityChecker(allowed_roles=["admin", "empleado"]))):
#     usuario_actual = current_user.rols
#     nombres = [r.name for r in usuario_actual]

#     return {"message": f"roles son: {nombres}"}