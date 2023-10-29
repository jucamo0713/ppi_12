# Importaciones de librerías de terceros
from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Header
from pydantic import BaseModel, Field
from pymongo import ReturnDocument

# Importaciones de módulos internos de la aplicación
from back.user_book.UserBook import UserBook
from back.jwt_utils.Guard import validate_token

UPSERT_USER_BOOK = APIRouter()


class UpsertUserBookRequest(BaseModel):
    """
    Modelo de solicitud para la creación o actualización de la relación
    usuario-libro.

    Atributos:
    - reading (bool): Indica si el libro está en proceso de lectura por el
    usuario.
    - favorite (bool): Indica si el libro es uno de los favoritos del usuario.
    - read (bool): Indica si el usuario ha leído el libro.
    """
    reading: bool = Field(...)
    favorite: bool = Field(...)
    read: bool = Field(...)


@UPSERT_USER_BOOK.put("/upsert")
def upsert_user_book(request: Request, book_id: str,
                     body: UpsertUserBookRequest,
                     authentication: str = Header(...)):
    """
    Maneja la creación o actualización de la relación usuario-libro.

    Parameters:
    - request (Request): La solicitud HTTP.
    - book_id (str): El identificador del libro.
    - body (UpsertUserBookRequest): Los datos de la relación usuario-libro.
    - authentication (str): El token de autenticación proporcionado en el
    encabezado.

    Returns:
    - UserBook: El objeto UserBook que representa la relación usuario-libro.

    Raises:
    - HTTPException: Si hay un error durante la creación o actualización.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Actualizar la relación usuario-libro en la base de datos
    data = request.app.database['user_books'].find_one_and_update({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id)
    }, {"$set": {
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id),
        "reading": body.reading,
        "favorite": body.favorite,
        "read": body.read,
    }},
        upsert=True,
        return_document=ReturnDocument.AFTER)

    if data:
        response = UserBook(**data)
    else:
        raise HTTPException(status_code=300, detail='Problema ambiguo')

    return response
