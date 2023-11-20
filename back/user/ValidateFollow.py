# Importaciones de librerías de terceros
from bson import ObjectId
from fastapi import APIRouter, Request, Header

# Importaciones internas
from jwt_utils.Guard import validate_token

# Configuración del enrutador para validar si dos usuarios se siguen
VALIDATE_IF_FOLLOWING = APIRouter()

@VALIDATE_IF_FOLLOWING.get('/validate-following')
def validate_if_following(request: Request,
                          follow_id: str,
                          authentication: str = Header(...)):
    """
    Valida si un usuario sigue a otro.

    Args:
        request (Request): Objeto Request de FastAPI.
        follow_id (str): ID del usuario al que se quiere verificar si se sigue.
        authentication (str): Token de autenticación en el encabezado.

    Returns:
        bool: True si el usuario sigue al otro, False si no.

    Esta función valida si el usuario representado por el token de
    autenticacióm
    sigue al usuario identificado por el ID `follow_id`. Utiliza la colección
    'follows' en la base de datos de la aplicación para realizar la
    verificación.

    Ejemplo:
    >>> validate_if_following(request, 'user456', 'token123')
    """
    # Valida el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Busca en la base de datos si hay una relación de seguimiento
    response = request.app.database['follows'].find_one({
        "$or": [
            {
                "user1_id": ObjectId(follow_id),
                "user2_id": ObjectId(user_id),
                "follow_back": True
            },
            {
                "user2_id": ObjectId(follow_id),
                "user1_id": ObjectId(user_id),
                "follow": True
            }
        ]
    })

    # Retorna True si existe una relación de seguimiento, False en caso
    # contrario
    return response is not None
