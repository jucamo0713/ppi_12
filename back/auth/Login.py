import hashlib
import re
from dotenv import dotenv_values
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from ..jwt.Utils import JwtUtils
from ..user.User import User

# Crea un enrutador para el manejo de la autenticación
LOGIN = APIRouter()

# Carga la configuración desde un archivo .env
config = dotenv_values(".env")


class LoginRequest(BaseModel):
    """
    Clase de modelo para las credenciales de inicio de sesión.

    Atributos:
    - user (str): Nombre de usuario o dirección de correo electrónico.
    - password (str): Contraseña del usuario.

    Args:
    - user (str): Nombre de usuario o dirección de correo electrónico.
    - password (str): Contraseña del usuario.
    """
    user: str
    password: str


@LOGIN.post("/login", response_description="Login User")
async def login(request: Request, login_data: LoginRequest):
    """
    Ruta de inicio de sesión que autentica al usuario y emite un token JWT
    si las credenciales son válidas.

    Args:
    - request (Request): Objeto de solicitud de FastAPI.
    - login_data (LoginRequest): Datos de inicio de sesión.

    Returns:
    - dict: Un diccionario que contiene el token de acceso JWT.
    """
    # Busca al usuario en la base de datos a partir del nombre de usuario o
    # correo electrónico
    user_data = request.app.database['users'].find_one({
        "$or": [
            {"user": re.compile(f'^{login_data.user}$', re.IGNORECASE)},
            {"email": re.compile(f'^{login_data.user}$', re.IGNORECASE)}
        ]
    })

    if user_data is None:
        # Si no se encuentra el usuario, se devuelve un error 401.
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user = User(**user_data)
    # Hash de la contraseña proporcionada con un salt
    hashed_password = hashlib.sha256((login_data.password + config[
        "HASHING_SALT"]).encode()).hexdigest()

    if hashed_password != user_data["password"]:
        # Si la contraseña no coincide, se devuelve un error 401.
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Genera un token JWT para el usuario autenticado
    token_data = user.to_jsonable()
    del token_data['password']
    jwt_token = JwtUtils.create_jwt_token(token_data,
                                          int(config['SESSION_EXPIRATION']))

    return {"access_token": jwt_token}
