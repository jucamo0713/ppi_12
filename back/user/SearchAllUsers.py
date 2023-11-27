# Importaciones de librerías estándar de Python
import re

from bson import ObjectId
# Importaciones de librerías de terceros
from fastapi import APIRouter, Request, Header

# Importaciones de módulos internos de la aplicación
from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token
from user.User import User

SEARCH_ALL_USERS = APIRouter()


@SEARCH_ALL_USERS.get("/", response_description="List all books")
def list_users(request: Request,
               limit=15,
               page=1,
               search_param='',
               authentication: str = Header(None)):
    """
    Recupera una lista de libros utilizando paginación y búsqueda.

    Args:
        request (Request): La solicitud HTTP entrante.
        limit (int, optional): El número máximo de libros por página (
            predeterminado: 15).
        page (int, optional): La página deseada (predeterminado: 1).
        search_param (str, optional): Parámetro de búsqueda para el título o
            autor de los libros (predeterminado: '').
        authentication (str, optional): Parámetro de validación de la sesión.
    Returns:
        dict: Un diccionario que contiene datos y metadatos de la respuesta.

    Respuesta:
        - data (List[Book]): Una lista de objetos Book que representan los
        libros encontrados.
        - metadata (dict): Un diccionario con metadatos de paginación,
        incluyendo total, página actual y total de páginas.
    """
    query = {
        '$or': [
            {'name': re.compile(f'{search_param}', re.IGNORECASE)},
            {'user': re.compile(f'{search_param}', re.IGNORECASE)},
            {'email': re.compile(f'{search_param}', re.IGNORECASE)},
        ],
    }
    if authentication is not None:
        # Validar el token de autenticación utilizando la función
        # validate_token
        token_data = validate_token(authentication)
        query['_id'] = {'$ne': ObjectId(token_data['id'])}
    # Realiza una búsqueda en la base de datos de libros utilizando paginación
    users = list(request.app.database['users'].aggregate(
        paginated_search(
            page=int(page), limit=int(limit),
            query=query
        )))

    # Si se encuentran usuarios, se crea una respuesta con los datos y
    # metadatos
    response = users[0] if len(users) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'total_pages': 0,
    }}
    response['data'] = list(map(lambda x: User(**x), response["data"]))
    return response
