from fastapi import HTTPException

# Importa la clase JwtUtils del módulo Utils
from .Utils import JwtUtils


def validate_token(authorization):
    """
    Valida y decodifica un token JWT proporcionado en el encabezado de
    autorización.

    Args:
    - authorization (str): El encabezado de autorización que debe contener un
      token JWT precedido por "Bearer ".

    Returns:
    - dict: Un diccionario con los datos contenidos en el token JWT si es
      válido.

    Raises:
    - HTTPException: Se genera una excepción HTTP con el código de estado 401
      y un mensaje de error en caso de que no se proporcione un token válido o
      no se siga el formato "Bearer ".
    """
    if not authorization or not authorization.startswith("Bearer "):
        # Si no hay autorización o no comienza con "Bearer ", se genera una
        # excepción HTTP con un mensaje de error.
        raise HTTPException(status_code=401, detail="Invalid token type")

    # Obtiene el token eliminando "Bearer " del encabezado.
    token = authorization.split("Bearer ")[-1]

    # Utiliza JwtUtils para decodificar el token JWT y devuelve los datos.
    return JwtUtils.decode_jwt_token(token)
