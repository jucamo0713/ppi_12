# Importaciones de librerías necesarias
from bson import ObjectId
from fastapi import APIRouter, Request, Header

from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token
from notifications.Notification import Notification

# Definición de un router para las operaciones de búsqueda de notificaciones
SEARCH_ALL_NOTIFICATIONS = APIRouter()


@SEARCH_ALL_NOTIFICATIONS.get("/all")
def search_all_notifications(request: Request, limit: int = 15, page: int = 1,
                             authentication: str = Header(...)):
    """
    Busca todas las notificaciones para un usuario específico.

    Parameters:
    - request (Request): Objeto de solicitud de FastAPI.
    - limit (int): Número máximo de notificaciones a devolver (
    predeterminado: 15).
    - page (int): Número de página de notificaciones (predeterminado: 1).
    - authentication (str): Token de autenticación en la cabecera.

    Returns:
    - dict: Un diccionario que contiene datos y metadatos de las
    notificaciones.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = ObjectId(token_data['id'])

    # Realizar una búsqueda paginada de notificaciones en la base de datos
    response = list(request.app.database['notifications'].aggregate(
        paginated_search(
            page=int(page), limit=int(limit),
            query={
                "user_id": user_id
            }
        )
    ))

    if len(response) > 0:
        response = response.pop()
    else:
        return {
            'data': [],
            "metadata": {}
        }

    # Convertir los datos de notificación a objetos Notification
    response["data"] = [Notification(**x) for x in response["data"]]
    return response
