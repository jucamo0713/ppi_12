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
    token_data = validate_token(authentication)
    user_id = token_data['id']
    query = []
    data_to_update = {}
    if user.user is not None:
        query.append({"user": re.compile(f'^{user.user}$', re.IGNORECASE)})
        data_to_update["user"] = user.user
    if user.email is not None:
        query.append({"email": re.compile(f'^{user.email}$', re.IGNORECASE)})
        data_to_update["email"] = user.email
    if len(query) > 0:
        existing_user = request.app.database['users'].find_one({
            "$or": query
        })
        if existing_user:
            raise HTTPException(status_code=400,
                                detail="Usuario o correo electrónico ya "
                                       "existen")

    if user.burn_date is not None:
        data_to_update["burn_date"] = user.burn_date

    if user.name is not None:
        data_to_update["name"] = user.name

    updated_user = request.app.database['users'].find_one_and_update(
        {
            "_id": ObjectId(user_id)
        }, {"$set": data_to_update},
        return_document=ReturnDocument.AFTER)

    new_user = User(**updated_user)
    # Genera un token JWT para el usuario autenticado
    token_data = new_user.to_jsonable()
    del token_data['password']
    jwt_token = JwtUtils.create_jwt_token(token_data,
                                          int(config['SESSION_EXPIRATION']))

    return {"user": token_data, "token": jwt_token}
