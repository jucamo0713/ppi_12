from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.params import Header
from user_book.UserBook import UserBook
from jwt_utils.Guard import validate_token

SEARCH_USER_BOOK = APIRouter()


@SEARCH_USER_BOOK.get("/")
def search_user_book(request: Request, book_id: str,
                     authentication: str = Header(...)):
    """
    Obtiene o crea una relación usuario-libro y la devuelve.

    Parameters:
    - request (Request): La solicitud HTTP.
    - book_id (str): El identificador del libro.
    - authentication (str): El token de autenticación proporcionado en el
    encabezado.

    Returns:
    - UserBook: El objeto UserBook que representa la relación usuario-libro.

    Raises:
    - HTTPException: Si hay un error durante la búsqueda o creación de la
    relación.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Buscar la relación usuario-libro en la base de datos
    data = request.app.database['user_books'].find_one({'user_id': ObjectId(
        user_id), 'book_id': ObjectId(book_id)})

    print(data)
    if data:
        response = UserBook(**data)
    else:
        # Si no se encuentra la relación, se crea una nueva
        response = UserBook(user_id=ObjectId(user_id),
                            book_id=ObjectId(book_id),
                            reading=False,
                            favorite=False,
                            read=False)

    return response
