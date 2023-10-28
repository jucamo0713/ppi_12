import re
from fastapi import APIRouter, Request

from book.Book import Book
from db.PaginatedSearch import paginated_search

SEARCH_ALL_BOOKS = APIRouter()


@SEARCH_ALL_BOOKS.get("/", response_description="List all books")
def list_books(request: Request, limit=15, page=1, search_param=''):
    """
    Recupera una lista de libros utilizando paginación y búsqueda.

    Args:
        request (Request): La solicitud HTTP entrante.
        limit (int, optional): El número máximo de libros por página (
        predeterminado: 15).
        page (int, optional): La página deseada (predeterminado: 1).
        search_param (str, optional): Parámetro de búsqueda para el título o
        autor de los libros (predeterminado: '').

    Returns:
        dict: Un diccionario que contiene datos y metadatos de la respuesta.

    Respuesta:
        - data (List[Book]): Una lista de objetos Book que representan los
        libros encontrados.
        - metadata (dict): Un diccionario con metadatos de paginación,
        incluyendo total, página actual y total de páginas.
    """
    # Realiza una búsqueda en la base de datos de libros utilizando paginación
    books = list(request.app.database['books'].aggregate(
        paginated_search(
            page=int(page), limit=int(limit),
            query={
                '$or': [
                    {'title': re.compile(f'{search_param}', re.IGNORECASE)},
                    {'author': re.compile(f'{search_param}', re.IGNORECASE)}
                ]
            }
        )))

    # Si se encuentran libros, se crea una respuesta con los datos y metadatos
    response = books[0] if len(books) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'totalPages': 0,
    }}
    response['data'] = list(map(lambda x: Book(**x), response["data"]))
    return response
