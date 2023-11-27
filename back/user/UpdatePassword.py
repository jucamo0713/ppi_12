# Importar librerías necesarias
import hashlib

from bson import ObjectId
from dotenv import dotenv_values
from fastapi import APIRouter, Request, Header, HTTPException
from pydantic import BaseModel

from jwt_utils.Guard import validate_token

UPDATE_PASSWORD = APIRouter()

# Carga la configuración desde un archivo .env
config = dotenv_values(".env")


class UpdatePasswordRequest(BaseModel):
    """
    Clase para representar la solicitud de actualización de contraseña.

    Atributos:
        current_password (str): La contraseña actual del usuario.
        new_password (str): La nueva contraseña propuesta por el usuario.
    """

    current_password: str
    new_password: str


@UPDATE_PASSWORD.put("/update-password")
def update_password(request: Request, data: UpdatePasswordRequest,
                    authentication: str = Header(...)):
    """
    Actualiza la contraseña del usuario.

    Args:
        request (Request): Objeto Request de FastAPI.
        data (UpdatePasswordRequest): Datos de la solicitud de actualización
        de contraseña.
        authentication (str): Token de autenticación pasado en la cabecera.

    Returns:
        dict: Un diccionario que indica el éxito de la operación.
    Raises:
        HTTPException: Si la contraseña actual proporcionada no coincide con
        la contraseña almacenada.
    """
    # Valida el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Busca al usuario en la base de datos
    user = request.app.database['users'].find_one({
        "_id": ObjectId(user_id)
    })

    # Hash de la contraseña actual
    hashed_password = hashlib.sha256((data.current_password + config[
        "HASHING_SALT"]).encode()).hexdigest()

    # Compara las contraseñas
    if hashed_password != user["password"]:
        # Si la contraseña no coincide, se devuelve un error 401.
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # Hash de la nueva contraseña y actualización en la base de datos
    new_hashed_password = hashlib.sha256((data.new_password + config[
        "HASHING_SALT"]).encode()).hexdigest()
    request.app.database['users'].find_one_and_update({
        "_id": ObjectId(user_id)
    }, {"$set": {"password": new_hashed_password}})

    # Devuelve un diccionario indicando el éxito de la operación
    return {"success": True}
