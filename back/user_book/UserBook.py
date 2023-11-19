# Importaciones de librerías de terceros
from bson import ObjectId
from pydantic import BaseModel, Field


class UserBook(BaseModel):
    """
    Modelo de datos para representar la relación entre un usuario y un libro.

    Atributos:
    - id (ObjectId): Identificador único de la relación usuario-libro.
    - user_id (ObjectId): Identificador único del usuario.
    - book_id (ObjectId): Identificador único del libro.
    - reading (bool): Indica si el libro está en proceso de lectura por el
    usuario.
    - favorite (bool): Indica si el libro es uno de los favoritos del usuario.
    - read (bool): Indica si el usuario ha leído el libro.

    Args:
        id (ObjectId): Identificador único de la relación usuario-libro.
        user_id (ObjectId): Identificador único del usuario.
        book_id (ObjectId): Identificador único del libro.
        reading (bool): Indica si el libro está en proceso de lectura por el
        usuario.
        favorite (bool): Indica si el libro es uno de los favoritos del
        usuario.
        read (bool): Indica si el usuario ha leído el libro.

    Config:
        Configuración del modelo UserBook.

    Atributos:
    - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios en
    el modelo.
    - json_encoders (dict): Diccionario de codificadores JSON personalizados.

    Args:
        arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios
        en el modelo.
        json_encoders (dict): Diccionario de codificadores JSON personalizados.

    """
    id: ObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
        description="Identificador único de la relación usuario-libro.",
    )
    user_id: ObjectId = Field(
        default_factory=ObjectId,
        description="Identificador único del usuario."
    )
    book_id: ObjectId = Field(
        default_factory=ObjectId,
        description="Identificador único del libro."
    )
    reading: bool = Field(
        ...,
        description="Indica si el libro está en proceso de lectura por el "
                    "usuario."
    )
    favorite: bool = Field(
        ...,
        description="Indica si el libro es uno de los favoritos del usuario."
    )
    read: int = Field(
        ...,
        description="Indica cuantas veces se a leído el usuario el libro."
    )
    rating: float = Field(
        None,
        description="Indica la valoración que el usuario le da al libro"
    )

    class Config:
        """
        Configuración del modelo UserBook.

        Atributos:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios
        en el modelo.
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
