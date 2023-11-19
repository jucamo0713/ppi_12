# Importaciones de librerías de terceros
from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Header
from pydantic import BaseModel, Field
from pymongo import ReturnDocument

from book.Book import Book
# Importaciones de módulos internos de la aplicación
from user_book.UserBook import UserBook
from jwt_utils.Guard import validate_token

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
    read: int = Field(...)
    rating: float = Field(...)


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
    rating = body.rating if body.read > 0 else None

    before_data = request.app.database['user_books'].find_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id)
    })
    book = request.app.database['books'].find_one({
        '_id': ObjectId(book_id)
    })
    book = Book(**book)
    if before_data:
        before_data = UserBook(**before_data)
        if rating is not None:
            if before_data.rating is None:
                request.app.database['books'].find_one_and_update({
                    '_id': ObjectId(book_id)
                }, {"$inc": {"total_ratings": 1},
                    "$set": {
                        "rating": ((book.rating * book.total_ratings)
                                   + rating) / (book.total_ratings + 1)
                    }})
            elif before_data.rating != rating:
                request.app.database['books'].find_one_and_update({
                    '_id': ObjectId(book_id)
                }, {
                    "$set": {
                        "rating": ((book.rating * book.total_ratings)
                                   + (rating - before_data.rating)) / (
                                      book.total_ratings)
                    }})
        elif before_data.rating is not None:
            request.app.database['books'].find_one_and_update({
                '_id': ObjectId(book_id)
            }, {"$inc": {"total_ratings": -1},
                "$set": {
                    "rating": ((book.rating * book.total_ratings)
                               - before_data.rating) / (
                                      book.total_ratings - 1)
                } if book.total_ratings - 1 > 0 else {},
                "$unset": {} if book.total_ratings - 1 > 0 else {
                    "rating": True}})

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
        **({"rating": rating} if rating is not None else {})
    }, "$unset": {"rating": True} if rating is None else {}},
        upsert=True,
        return_document=ReturnDocument.AFTER)

    if data:
        response = UserBook(**data)
    else:
        raise HTTPException(status_code=300, detail='Problema ambiguo')

    return response
