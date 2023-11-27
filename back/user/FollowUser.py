from datetime import datetime

# Importaciones de librerías de terceros
from bson import ObjectId
from dotenv import dotenv_values
from fastapi import APIRouter, Request, Header
from pymongo import ReturnDocument

from jwt_utils.Guard import validate_token
from user.Follow import Follow
from user.SearchFollowers import search_following

# Configura el enrutador para las actualizaciones de usuarios
FOLLOW_USER = APIRouter()

# Carga la configuración desde un archivo .env
config = dotenv_values(".env")


# Define la ruta para la acción de seguir a otro usuario
@FOLLOW_USER.post("")
def follow_user(request: Request, follow_id: str,
                authentication: str = Header(...)):
    """
    Sigue a otro usuario.

    Args:
        request (Request): Objeto Request de FastAPI.
        follow_id (str): ID del usuario a seguir.
        authentication (str): Token de autenticación en el encabezado.

    Returns:
        Follow: Objeto Follow que representa la relación de seguimiento.

    Raises:
        HTTPException: Excepción HTTP en caso de error.

    Esta función maneja las solicitudes para seguir a otro usuario.
    Utiliza la información del token de autenticación para identificar al
    usuario que realiza la acción.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Busca la relación de seguimiento
    data = request.app.database['follows'].find_one({
        'user1_id': ObjectId(follow_id), "user2_id": ObjectId(user_id)
    })

    # Actualiza o crea la relación de seguimiento
    if data:
        data["follow_back"] = True
        response = request.app.database['follows'].find_one_and_update(
            {'user1_id': ObjectId(follow_id), "user2_id": ObjectId(user_id)},
            {"$set": data}, return_document=ReturnDocument.AFTER
        )
    else:
        data = {"user1_id": ObjectId(user_id),
                "user2_id": ObjectId(follow_id),
                "follow": True,
                "follow_back": False}
        response = request.app.database['follows'].find_one_and_update(
            {'user2_id': ObjectId(follow_id), "user1_id": ObjectId(user_id)},
            {"$set": data}, return_document=ReturnDocument.AFTER, upsert=True)

    # Envia la notificación de al usuario de que lo empezaron a seguir
    followers = search_following(request, authentication, None, None)["data"]
    data = [{
        "message": f"El usuario {token_data['user']} te empezó a seguir",
        "user_id": ObjectId(follow_id),
        "type": "NEW_FOLLOWER",
        "created_at": datetime.now(),
        "data_id": ObjectId(user_id),
    }]
    for follower in followers:
        data.append({
            "message": f"El usuario {token_data['user']} a quien sigues "
                       f"empezó a seguir a alguien mas.",
            "user_id": follower['_id'],
            "type": "NEW_FOLLOW_OF_FOLLOWER",
            "created_at": datetime.now(),
            "data_id": ObjectId(user_id),
        })
    request.app.database['notifications'].insert_many(data)
    # Convierte la respuesta en un objeto Follow y lo devuelve
    return Follow(**response)
