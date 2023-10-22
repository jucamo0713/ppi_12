from bson import ObjectId
from pydantic import BaseModel, Field

class Book(BaseModel):
    """
    Clase para representar un libro.

    Atributos:
    - id: ObjectId - ID único del libro.
    - title: str - Título del libro.
    - author: str - Autor del libro.
    - image: str - URL de la imagen del libro.
    """

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    image: str = Field(...)

    class Config:
        """
        Configuración de la clase Book.

        Permite tipos arbitrarios y define un codificador JSON personalizado para ObjectId.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
