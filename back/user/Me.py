from dotenv import dotenv_values
from fastapi import APIRouter, Depends
from fastapi.params import Header

from ..jwt.Guard import validate_token

ME = APIRouter()

# Cargar la configuración desde el archivo .env
config = dotenv_values(".env")


@ME.get("/me", response_description="Obtener datos del usuario autenticado")
def me(authentication: str = Header(...)):
    """
    Obtiene los datos del usuario autenticado a partir del token de
    autenticación.

    Args:
        authentication (str): Token de autenticación enviado en la cabecera
        de la solicitud.

    Returns:
        dict: Datos del usuario autenticado.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    return token_data
