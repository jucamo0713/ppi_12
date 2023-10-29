# Importaciones de librerías estándar de Python
from datetime import datetime

# Importaciones de librerías de terceros
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    """
    Modelo de datos para representar un usuario.

    Atributos:
    - id (str): Identificador único del usuario.
    - name (str): Nombre completo del usuario.
    - user (str): Nombre de usuario (nombre de inicio de sesión).
    - password (str): Contraseña del usuario.
    - email (str): Dirección de correo electrónico del usuario.
    - burn_date (datetime): Fecha de nacimiento del usuario en formato
    ISODate (AAAA-MM-DDTHH:MM:SS).

    Args:
        id (str): Identificador único del usuario.
        name (str): Nombre completo del usuario.
        user (str): Nombre de usuario (nombre de inicio de sesión).
        password (str): Contraseña del usuario.
        email (str): Dirección de correo electrónico del usuario.
        burn_date (datetime): Fecha de nacimiento del usuario.
        registered_date (datetime): Fecha de registro del usuario.
    """

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(..., description="Nombre completo del usuario.")
    user: str = Field(...,
                      description="Nombre de usuario (nombre de inicio de "
                                  "sesión).")
    password: str = Field(..., description="Contraseña del usuario.")
    email: EmailStr = Field(..., description="Dirección de correo "
                                             "electrónico del usuario.")
    burn_date: datetime = Field(
        description="Fecha de nacimiento del usuario en formato ISODate ("
                    "AAAA-MM-DDTHH:MM:SS).")
    registered_date: datetime = Field(
        description="Fecha de registro del usuario en la plataforma")

    class Config:
        """
        Configuración del modelo `User`.

        Atributos:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
        - json_encoders (dict): Diccionario de codificadores JSON
        personalizados.

        Args:
            arbitrary_types_allowed (bool): Permite tipos de datos
            arbitrarios en el modelo.
            json_encoders (dict): Diccionario de codificadores JSON
            personalizados.

        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_jsonable(self, **kwargs):
        """
        Convierte el objeto `User` a un diccionario JSON.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Un diccionario JSON que representa el objeto `User`.
        """
        user_dict = self.model_dump(**kwargs)
        user_dict['id'] = str(user_dict['id'])
        user_dict['burn_date'] = self.burn_date.isoformat()
        user_dict['registered_date'] = self.registered_date.isoformat()
        return user_dict
