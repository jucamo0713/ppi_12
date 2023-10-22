import hashlib
import re

from dotenv import dotenv_values
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from ..jwt.Utils import JwtUtils
from ..user.User import User

LOGIN = APIRouter()

config = dotenv_values(".env")


class LoginRequest(BaseModel):
    user: str
    password: str


@LOGIN.post("/login", response_description="Login User")
async def login(request: Request, login_data: LoginRequest):
    user_data = request.app.database['users'].find_one({
        "$or": [
            {"user": re.compile(f'^{login_data.user}$', re.IGNORECASE)},
            {"email": re.compile(f'^{login_data.user}$', re.IGNORECASE)}
        ]
    })
    if user_data is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user = User(**user_data)
    hashed_password = hashlib.sha256((login_data.password + config[
        "HASHING_SALT"]).encode()).hexdigest()
    if hashed_password != user_data["password"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Genera un token JWT para el usuario autenticado
    token_data = user.to_jsonable()
    jwt_token = JwtUtils.create_jwt_token(token_data,
                                          int(config['SESSION_EXPIRATION']))

    return {"access_token": jwt_token}
