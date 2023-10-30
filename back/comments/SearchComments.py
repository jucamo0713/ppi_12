# Importaciones de librerías estándar de Python
import re

from bson import ObjectId
# Importaciones de librerías de terceros
from fastapi import APIRouter, Request, HTTPException

# Importaciones de módulos internos de la aplicación
from db.PaginatedSearch import paginated_search
from comments.BookComment import BookComment

SEARCH_COMMENTS = APIRouter()


@SEARCH_COMMENTS.get("/", response_description="List all comments")
def list_comments(request: Request, book_id: str, reply_to: str = None,
                  limit=15, page=1):
    """
    Recupera una lista de comentarios utilizando paginación y búsqueda.

    Args:
        request (Request): La solicitud HTTP entrante.
        book_id (str): El id del libro al cual está relacionado el comentario
        limit (int, optional): El número máximo de comentarios por página (
        predeterminado: 15).
        page (int, optional): La página deseada (predeterminado: 1).
        search_param (str, optional): Parámetro de búsqueda para el contenido
        o usuario de los comentarios (predeterminado: '').

    Returns:
        dict: Un diccionario que contiene datos y metadatos de la respuesta.

    Respuesta:
        - data (List[Comment]): Una lista de objetos Comment que
        representan los
        comentarios encontrados.
        - metadata (dict): Un diccionario con metadatos de paginación,
        incluyendo total, página actual y total de páginas.
    """
    # Realiza una búsqueda en la base de datos de comentarios utilizando
    # paginación
    query = {
                "book_id": ObjectId(book_id)
            }
    if reply_to is None:
        query["root"] = True
    else:
        query["reply_to"] = ObjectId(reply_to)

    comments = list(request.app.database['comments'].aggregate(
        paginated_search(
            page=int(page), limit=int(limit),
            query=query
        )))

    # Si se encuentran comentarios, se crea una respuesta con los datos y
    # metadatos
    response = comments[0] if len(comments) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'totalPages': 0,
    }}
    response['data'] = list(map(lambda x: BookComment(**x), response["data"]))
    return response
