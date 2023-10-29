# Importaciones de librerías de terceros
from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException

# Importaciones de módulos internos de la aplicación
from back.book.Book import Book


SEARCH_BOOK_BY_ID = APIRouter()


@SEARCH_BOOK_BY_ID.get("/by-id")
def by_id(request: Request, id: str):
    """
    Busca un libro por su ID en la base de datos.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        id (str): El ID del libro a buscar.

    Returns:
        Book: Datos del libro si se encuentra.
        HTTPException: Excepción HTTP 404 si el libro no existe.
    """
    # Busca un libro en la base de datos por su ID.
    data = request.app.database['books'].find_one({'_id': ObjectId(id)})

    if data:  # Si se encuentra un libro con el ID proporcionado:
        response = Book(
            **data)  # Construye una respuesta utilizando la clase Book y
        # los datos encontrados.
        return response  # Devuelve la respuesta que contiene los datos del
        # libro encontrado.

    # Si no se encuentra un libro con el ID proporcionado:
    raise HTTPException(status_code=404,
                        detail='Libro No Existe')  # Genera una excepción
    # HTTP 404 con un mensaje de error.
