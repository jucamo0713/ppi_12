# Importaciones de librerías estándar de Python
import re
from typing import Literal
from bson import ObjectId

# Importaciones de librerías de terceros
from fastapi import APIRouter, Request, Header

# Importaciones de módulos internos de la aplicación
from book.Book import Book
from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token

# Define un enrutador para listar los libros del usuario
SEARCH_ALL_USER_BOOKS = APIRouter()


@SEARCH_ALL_USER_BOOKS.get("/list/{type_of_list}",
                           response_description="List all user books")
def list_user_books(request: Request,
                    type_of_list: Literal['reading', 'favorite', 'read'],
                    limit: int = 15,
                    page: int = 1,
                    search_param: str = '',
                    user_id: str = None,
                    authentication: str = Header(None)):
    """
    Lista los libros del usuario según el tipo especificado (leyendo,
    favorito, leído).

    Args:
        request (Request): La solicitud HTTP entrante.
        type_of_list (Literal['reading', 'favorite', 'read']): El tipo de
            lista de libros a mostrar.
        limit (int, optional): El número máximo de libros por página (
            predeterminado: 15).
        page (int, optional): La página deseada (predeterminado: 1).
        search_param (str, optional): Parámetro de búsqueda para título o
            autor de libros (predeterminado: '').
        authentication (str): Token de autenticación en la cabecera.

    Returns:
        dict: Un diccionario que contiene datos y metadatos de la respuesta.

        - data (List[Book]): Una lista de objetos Book que representan los
            libros encontrados-
        - metadata (dict): Un diccionario con metadatos de paginación,
            incluyendo total, página actual y total de páginas.
    """
    # Validar el token de autenticación utilizando la función validate_token
    if user_id is None:
        token_data = validate_token(authentication)
        user_id = token_data['id']
    match = {
        type_of_list: True,
        'user_id': ObjectId(user_id)
    } if type_of_list != 'read' else {
        type_of_list: {'$gte': 1},
        'user_id': ObjectId(user_id)
    }
    # Definir la consulta para la búsqueda con paginación y filtro
    query = paginated_search(
        page=int(page),
        limit=int(limit),
        query={
            "$or": [
                {'title': re.compile(f'{search_param}', re.IGNORECASE)},
                {'author': re.compile(f'{search_param}', re.IGNORECASE)}
            ],
        },
        pre_query=[
            {
                '$match': match
            }, {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': '_id',
                    'as': 'book'
                }
            }, {
                '$unwind': {
                    'path': '$book',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    '_id': '$book._id',
                    'isbn_code': '$book.isbn_code',
                    'title': '$book.title',
                    'author': '$book.author',
                    'image': '$book.image'
                }
            }
        ]
    )

    # Realiza una búsqueda en la base de datos de libros utilizando paginación
    books = list(request.app.database['user_books'].aggregate(query))

    # Si se encuentran libros, se crea una respuesta con los datos y metadatos
    response = books[0] if len(books) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'total_pages': 0,
    }}
    response['data'] = list(map(lambda x: Book(**x), response["data"]))
    return response
