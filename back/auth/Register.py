# Importaciones de librerías estándar de Python
import hashlib
import re
from datetime import datetime

# Importaciones de librerías de terceros
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr

# Importaciones de módulos internos de la aplicación
from user.User import User


REGISTER = APIRouter()

config = dotenv_values(".env")


class RegisterRequest(BaseModel):
    """
    Modelo de datos para registrar un nuevo usuario en la aplicación.

    Atributos:
    - `name`: El nombre del usuario.
    - `user`: El nombre de usuario del usuario.
    - `password`: La contraseña del usuario.
    - `email`: La dirección de correo electrónico del usuario.
    - `burn_date`: La fecha de nacimiento del usuario.
    """
    name: str
    user: str
    password: str
    email: EmailStr
    burn_date: datetime


@REGISTER.post("/register", response_description="Register User")
async def register(request: Request, user: RegisterRequest):
    """
    Registra un nuevo usuario en la base de datos.

    Parámetros:
    - `request`: La solicitud HTTP recibida.
    - `user`: Un objeto de la clase `RegisterRequest` que contiene los datos
    del usuario a registrar.

    Retorna:
    - Un objeto de la clase `User` que representa al usuario registrado.

    Si el usuario o el correo electrónico ya existen en la base de datos,
    se devuelve un error HTTP 400. De lo contrario,
    se almacenan los datos del nuevo usuario en la base de datos después de
    hashear la contraseña con SHA-256.

    Esta función se expone en la ruta `/register` de la API para permitir el
    registro de nuevos usuarios.
    """
    existing_user = request.app.database['users'].find_one({
        "$or": [
            {"user": re.compile(f'^{user.user}$', re.IGNORECASE)},
            {"email": re.compile(f'^{user.email}$', re.IGNORECASE)}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="Usuario o correo electrónico ya existen")

    hashed_password = hashlib.sha256((user.password + config[
        "HASHING_SALT"]).encode()).hexdigest()

    id = request.app.database['users'].insert_one({"name": user.name,
                                                   "user": user.user,
                                                   "email": user.email,
                                                   "burn_date": user.burn_date,
                                                   "password":
                                                       hashed_password,
                                                   "registered_date":
                                                       datetime.now()})
    data = request.app.database['users'].find_one({'_id': id.inserted_id})
    response: User = User(**data)
    return response
