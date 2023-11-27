# Importar librerías necesarias
from bson import ObjectId
from fastapi import APIRouter, Request, Header
from jwt_utils.Guard import validate_token

DELETE_NOTIFICATION = APIRouter()


@DELETE_NOTIFICATION.delete("/delete")
def search_all_notifications(request: Request, id: str,
                             authentication: str = Header(...)):
    """
    Elimina una notificación por su ID.

    Parameters:
    - request (Request): Objeto de solicitud de FastAPI.
    - id (str): ID de la notificación a eliminar.
    - authentication (str): Token de autenticación en la cabecera.

    Returns:
    - dict: Un diccionario indicando el éxito de la operación.
    """
    # Validar el token de autenticación utilizando la función
    # validate_token
    validate_token(authentication)

    # Buscar y eliminar la notificación por su ID en la base de datos
    request.app.database['notifications'].find_one_and_delete({
        "_id": ObjectId(id)
    })

    # Devolver un diccionario indicando el éxito de la operación
    return {"success": True}
