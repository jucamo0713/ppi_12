# Importaciones de librerías estándar de Python
from datetime import datetime

# Importaciones de librerías de terceros
from bson import ObjectId
from pydantic import BaseModel, Field


class BookComment(BaseModel):
    """
    Modelo de datos para representar un comentario de libro.

    Atributos:
    - id (ObjectId): Identificador único del comentario.
    - user_id (ObjectId): Identificador único del usuario que realizó el
        comentario.
    - book_id (ObjectId): Identificador único del libro al que se refiere el
        comentario.
    - responded_to (ObjectId | None): Identificador único del comentario al
        que se responde (opcional).
    - content (str): Contenido del comentario.
    - has_responses (bool): Booleano que indica si el comentario tiene
        respuestas.
    - root (bool): Booleano que indica si es un comentario raíz.
    - created_date (datetime): Fecha de creación del comentario en formato
        ISODate (AAAA-MM-DDTHH:MM:SS).
    - username (str): El usuario que comentó (opcional).

    Args:
        id (ObjectId): Identificador único del comentario.
        user_id (ObjectId): Identificador único del usuario que realizó el
            comentario.
        book_id (ObjectId): Identificador único del libro al que se refiere
            el comentario.
        responded_to (ObjectId | None): Identificador único del comentario
            al que se responde (opcional).
        content (str): Contenido del comentario.
        has_responses (bool): Booleano que indica si el comentario tiene
            respuestas.
        root (bool): Booleano que indica si es un comentario raíz.
        created_date (datetime): Fecha de creación del comentario.

    """
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectId = Field(
        description="Identificador único del usuario que realizó el "
                    "comentario.")
    book_id: ObjectId = Field(
        description="Identificador único del libro al que se refiere el "
                    "comentario.")
    responded_to: ObjectId | None = Field(
        default=None,
        description="Identificador único del comentario al que se responde ("
                    "opcional).")
    content: str = Field(..., description="Contenido del comentario.")
    has_responses: bool = Field(
        default=False,
        description="Booleano que dice si el comentario tiene respuestas")
    root: bool = Field(
        ...,
        description="Booleano que indica si es un comentario raíz.")
    created_date: datetime = Field(
        default=datetime.now(),
        description="Fecha de creación del comentario en formato ISODate ("
                    "AAAA-MM-DDTHH:MM:SS).")
    username: str = Field(default=None,
                          description="El usuario que comentó (opcional).")

    class Config:
        """
        Configuración del modelo `BookComment`.

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
        Convierte el objeto `BookComment` a un diccionario JSON.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Un diccionario JSON que representa el objeto `BookComment`.
        """
        comment_dict = self.model_dump(**kwargs)
        comment_dict['id'] = str(comment_dict['id'])
        comment_dict['user_id'] = str(comment_dict['user_id'])
        comment_dict['book_id'] = str(comment_dict['book_id'])
        comment_dict['created_date'] = self.created_date.isoformat()
        return comment_dict
