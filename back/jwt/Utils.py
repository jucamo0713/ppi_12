from datetime import datetime, timedelta

import jwt
from dotenv import dotenv_values
from fastapi import HTTPException

config = dotenv_values(".env")


class JwtUtils:
    @classmethod
    def create_jwt_token(cls, data: dict, expiration_minutes: int):
        # Calcular la fecha de expiración basada en el tiempo actual y la
        # duración proporcionada en minutos
        expiration_time = datetime.utcnow() + timedelta(
            minutes=expiration_minutes)

        # Agregar 'exp' (tiempo de expiración) al payload
        data['exp'] = expiration_time
        return jwt.encode(data, config['JWT_SECRET_KEY'])

    @classmethod
    def decode_jwt_token(cls, token: str):
        try:
            payload = jwt.decode(token, config['JWT_SECRET_KEY'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
