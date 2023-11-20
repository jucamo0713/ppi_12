# Importaciones de librerías de terceros
from bson import ObjectId
from dotenv import dotenv_values
from fastapi import APIRouter, Request,Header
from pymongo import ReturnDocument

from jwt_utils.Guard import validate_token
from user.Follow import Follow

# Configura el enrutador para las actualizaciones de usuarios
UNFOLLOW_USER = APIRouter()

# Carga la configuración desde un archivo .env
config = dotenv_values(".env")

# Define la ruta para la acción de dejar de seguir a un usuario
@UNFOLLOW_USER.put("")
def unfollow_user(request: Request, follow_id: str,
                  authentication: str = Header(...)):
    """
    Deja de seguir a otro usuario.

    Args:
        request (Request): Objeto Request de FastAPI.
        follow_id (str): ID del usuario a dejar de seguir.
        authentication (str): Token de autenticación en el encabezado.

    Returns:
        Follow: Objeto Follow que representa la relación actualizada.

    Raises:
        HTTPException: Excepción HTTP en caso de error.

    Esta función maneja las solicitudes para dejar de seguir a otro usuario.
    Utiliza la información del token de autenticación para identificar al
    usuario que realiza la acción.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']
    # Busca la relación de seguimiento en ambas direcciones
    data = request.app.database['follows'].find_one({
        'user1_id': ObjectId(follow_id), "user2_id": ObjectId(user_id)
    })

    # Actualiza la relación de seguimiento
    if data:
        data["follow_back"] = False
        response = request.app.database['follows'].find_one_and_update(
            {'user1_id': ObjectId(follow_id), "user2_id": ObjectId(user_id)},
            {"$set": data}, return_document=ReturnDocument.AFTER
        )
    else:
        data = request.app.database['follows'].find_one({
            'user2_id': ObjectId(follow_id), "user1_id": ObjectId(user_id)
        })
        data["follow"] = False
        response = request.app.database['follows'].find_one_and_update(
            {'user2_id': ObjectId(follow_id), "user1_id": ObjectId(user_id)},
            {"$set": data}, return_document=ReturnDocument.AFTER
        )

    # Convierte la respuesta en un objeto Follow y lo devuelve
    return Follow(**response)
