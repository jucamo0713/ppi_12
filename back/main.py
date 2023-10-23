from fastapi import FastAPI
from .book.BookRoutes import BookRoutes
from .auth.AuthRoutes import AuthRoutes
from .datasets.DatasetsRoutes import DATASETS_ROUTES
from .db.Connection import Connection
from .user.UserRoutes import USER_ROUTES

# Crear una instancia de FastAPI
app = FastAPI()

# Importar los módulos y configuraciones necesarios
modules = [Connection]

# Inicializar los módulos de la aplicación
for module in modules:
    module(app)


# Ruta raíz de la aplicación
@app.get("/")
async def root():
    return {"success": True}


# Obtener las rutas y controladores
routers = [*BookRoutes, *AuthRoutes, *USER_ROUTES, *DATASETS_ROUTES]

# Agregar las rutas y controladores a la aplicación
for router in routers:
    print(router)
    app.include_router(router['instance'], tags=[router['tag']],
                       prefix=router['path'])
