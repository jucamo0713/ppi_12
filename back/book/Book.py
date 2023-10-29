# Importaciones de librerías de terceros
from bson import ObjectId
from pydantic import BaseModel, Field


class Book(BaseModel):
    """
    Clase para representar un libro.

    Atributos:
    - id (ObjectId): ID único del libro.
    - isbn_code (str): Código ISBN del libro.
    - title (str): Título del libro.
    - author (str): Autor del libro.
    - image (str): URL de la imagen del libro.

    Args:
    - id (ObjectId): ID único del libro (generado automáticamente si no se
      proporciona).
    - isbn_code (str): Código ISBN del libro.
    - title (str): Título del libro.
    - author (str): Autor del libro.
    - image (str): URL de la imagen del libro.

    La clase `Book` se utiliza para representar libros con atributos como su
    título, autor, código ISBN y URL de la imagen. El atributo `id` es un ID
    único generado automáticamente si no se proporciona.

    La configuración de la clase permite tipos de datos arbitrarios y define
    un codificador JSON personalizado para ObjectId.

    Ejemplo de uso:
    book = Book(isbn_code="1234567890", title="Ejemplo de Libro",
                author="Autor del Libro",
                image="https://example.com/image.jpg")
    """
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    isbn_code: str = Field(..., description="Código ISBN del libro.")
    title: str = Field(..., description="Título del libro.")
    author: str = Field(..., description="Autor del libro.")
    image: str = Field(..., description="URL de la imagen del libro.")

    class Config:
        """
        Configuración de la clase Book.

        Atributos:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
        - json_encoders (dict): Diccionario de codificadores JSON
        personalizados.

        Args:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios en
          el modelo.
        - json_encoders (dict): Diccionario de codificadores JSON
        personalizados.

        Ejemplo de uso:
        Config.arbitrary_types_allowed = True
        Config.json_encoders = {ObjectId: str}
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
