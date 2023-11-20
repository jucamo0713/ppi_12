# Importaciones de librerías de terceros
import re
from datetime import datetime

from bson import ObjectId
from dotenv import dotenv_values
from fastapi import APIRouter, Request, HTTPException, Header
from pydantic import BaseModel
from pydantic import EmailStr
from pymongo import ReturnDocument

from jwt_utils.Guard import validate_token
from jwt_utils.Utils import JwtUtils
from user.User import User

# Configura el enrutador para las actualizaciones de usuarios
UPDATE_USERS = APIRouter()

# Carga la configuración desde un archivo .env
config = dotenv_values(".env")


class UpdateUsersRequest(BaseModel):
    """
    Modelo de datos para registrar un nuevo usuario en la aplicación.

    Atributos:
    - `name`: El nombre del usuario.
    - `burn_date`: La fecha de nacimiento del usuario.
    """
    name: str | None = None
    burn_date: datetime | None = None
    user: str | None = None
    email: EmailStr | None = None


@UPDATE_USERS.put("/update")
def update_users(request: Request, user: UpdateUsersRequest,
                 authentication: str = Header(...)):
    """
    Actualiza la información del usuario.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        user (UpdateUsersRequest): Datos para la actualización del usuario.
        authentication (str): Token de autenticación en la cabecera.

    Returns:
        dict: Información actualizada del usuario y un nuevo token JWT.

    Raises:
        HTTPException: Excepción de FastAPI en caso de un error.

    """
    # Valida el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Inicializa listas y diccionario para la actualización de datos
    query = []
    data_to_update = {}

    # Verifica si se proporcionó un nuevo nombre de usuario
    if user.user is not None:
        query.append({"user": re.compile(f'^{user.user}$', re.IGNORECASE)})
        data_to_update["user"] = user.user

    # Verifica si se proporcionó un nuevo correo electrónico
    if user.email is not None:
        query.append({"email": re.compile(f'^{user.email}$', re.IGNORECASE)})
        data_to_update["email"] = user.email

    # Verifica si el nuevo usuario o correo ya existen
    if len(query) > 0:
        existing_user = request.app.database['users'].find_one({
            "$or": query
        })
        if existing_user:
            raise HTTPException(status_code=400,
                                detail="Usuario o correo electrónico ya "
                                       "existen")

    # Verifica si se proporcionó una nueva fecha de nacimiento
    if user.burn_date is not None:
        data_to_update["burn_date"] = user.burn_date

    # Verifica si se proporcionó un nuevo nombre
    if user.name is not None:
        data_to_update["name"] = user.name

    # Actualiza el usuario en la base de datos
    updated_user = request.app.database['users'].find_one_and_update(
        {
            "_id": ObjectId(user_id)
        }, {"$set": data_to_update},
        return_document=ReturnDocument.AFTER)

    # Crea un nuevo objeto de usuario con los datos actualizados
    new_user = User(**updated_user)

    # Genera un token JWT para el usuario autenticado
    token_data = new_user.to_jsonable()
    del token_data['password']
    jwt_token = JwtUtils.create_jwt_token(token_data,
                                          int(config['SESSION_EXPIRATION']))

    # Devuelve la información actualizada del usuario y el nuevo token JWT
    return {"user": token_data, "token": jwt_token}
