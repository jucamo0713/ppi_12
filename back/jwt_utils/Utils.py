# Importaciones de librerías estándar de Python
from datetime import datetime, timedelta

# Importaciones de librerías de terceros
from dotenv import dotenv_values
from fastapi import HTTPException

# Importaciones de paquetes de la propia aplicación
import jwt


config = dotenv_values(".env")


class JwtUtils:
    """
    Clase de utilidad para trabajar con tokens JWT en FastAPI.

    Métodos:
    - create_jwt_token(data: dict, expiration_minutes: int) -> str: Crea un
      token JWT con los datos proporcionados y una duración en minutos.
    - decode_jwt_token(token: str) -> dict: Decodifica un token JWT y
      verifica su validez.

    Atributos:
    - No tiene atributos de clase.

    Args:
        No toma argumentos en el constructor de la clase.
    """

    @classmethod
    def create_jwt_token(cls, data: dict, expiration_minutes: int):
        """
        Crea un token JWT.

        Args:
            data (dict): Datos a incluir en el token.
            expiration_minutes (int): Duración en minutos del token.

        Returns:
            str: Token JWT.

        Raises:
            No genera excepciones.
        """
        # Calcular la fecha de expiración basada en el tiempo actual y la
        # duración proporcionada en minutos
        expiration_time = datetime.utcnow() + timedelta(
            minutes=expiration_minutes)

        # Agregar 'exp' (tiempo de expiración) al payload
        data['exp'] = expiration_time
        return jwt.encode(data, config['JWT_SECRET_KEY'])

    @classmethod
    def decode_jwt_token(cls, token: str):
        """
        Decodifica un token JWT y verifica su validez.

        Args:
            token (str): Token JWT a decodificar.

        Returns:
            dict: Payload del token JWT decodificado.

        Raises:
            HTTPException: Si el token ha expirado o es inválido.
        """
        try:
            payload = jwt.decode(token, config['JWT_SECRET_KEY'],
                                       algorithms=['HS256', 'HS384'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
