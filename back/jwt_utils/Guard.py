# Importaciones de librerías de terceros
from fastapi import HTTPException

from back.jwt_utils.Utils import JwtUtils



def validate_token(authorization):
    """
    Valida y decodifica un token JWT proporcionado en el encabezado de
    autorización.

    Args:
        authorization (str): El encabezado de autorización que debe contener un
        token JWT precedido por "Bearer ".

    Returns:
        dict: Un diccionario con los datos contenidos en el token JWT si es
        válido.

    Raises:
        HTTPException: Se genera una excepción HTTP con el código de estado 401
        y un mensaje de error en caso de que no se proporcione un token
        válido o
        no se siga el formato "Bearer ".

    Example:
        Para validar un token JWT en tu aplicación, puedes utilizar esta
        función de la
        siguiente manera:

        ```python
        from fastapi import Header

        # Obtén el token JWT del encabezado de autorización
        authorization_header = Header(...)

        # Llama a la función validate_token para validar y decodificar el token
        token_data = validate_token(authorization_header)

        # token_data ahora contiene los datos del token decodificado
        user_id = token_data['user_id']
        ```

    Esta función verifica si el encabezado de autorización comienza con
    "Bearer " y luego utiliza la clase `JwtUtils` para decodificar el token
    JWT. Si el token no es válido o no sigue el formato adecuado, se genera
    una excepción HTTP con el código de estado 401 y un mensaje de error.
    """
    if not authorization or not authorization.startswith("Bearer "):
        # Si no hay autorización o no comienza con "Bearer ", se genera una
        # excepción HTTP con un mensaje de error.
        raise HTTPException(status_code=401, detail="Invalid token type")

    # Obtiene el token eliminando "Bearer " del encabezado.
    token = authorization.split("Bearer ")[-1]

    # Utiliza JwtUtils para decodificar el token JWT y devuelve los datos.
    response = JwtUtils.decode_jwt_token(token)
    del response['exp']
    return response
