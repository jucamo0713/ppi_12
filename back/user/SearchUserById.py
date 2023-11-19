# Importaciones de librerías de terceros
from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException

# Importaciones de módulos internos de la aplicación
from book.Book import Book
from user.User import User

SEARCH_USER_BY_ID = APIRouter()


@SEARCH_USER_BY_ID.get("/by-id")
def by_id(request: Request, id: str):
    """
    Busca un usuario por su ID en la base de datos.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        id (str): El ID del usuario a buscar.

    Returns:
        Book: Datos del libro si se encuentra.
        HTTPException: Excepción HTTP 404 si el usuario no existe.
    """
    # Busca un usuario en la base de datos por su ID.
    data = request.app.database['users'].find_one({'_id': ObjectId(id)})
    # Si se encuentra un usuario con el ID proporcionado:
    if data:
        # Construye una respuesta utilizando la clase Book y los datos
        # encontrados.
        response = User(**data)
        del response.password
        # Devuelve la respuesta que contiene los datos del libro encontrado.
        return response

        # Si no se encuentra un usuario con el ID proporcionado:
    raise HTTPException(status_code=404,
                        detail='Usuario No Existe')
    # HTTP 404 con un mensaje de error.
