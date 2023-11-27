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
    current_password: str
    new_password: str


@UPDATE_PASSWORD.put("/update-password")
def update_users(request: Request, data: UpdatePasswordRequest,
                 authentication: str = Header(...)):
    # Valida el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']
    user = request.app.database['users'].find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    hashed_password = hashlib.sha256((data.current_password + config[
        "HASHING_SALT"]).encode()).hexdigest()

    if hashed_password != user["password"]:
        # Si la contraseña no coincide, se devuelve un error 401.
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    new_hashed_password = hashlib.sha256((data.new_password + config[
        "HASHING_SALT"]).encode()).hexdigest()
    request.app.database['users'].find_one_and_update({
        "_id": ObjectId(user_id)
    }, {
        "$set": {
            "password": new_hashed_password
        }
    })
    return {"success": True}
