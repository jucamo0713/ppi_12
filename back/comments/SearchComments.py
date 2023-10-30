# Importaciones de librerías estándar de Python
from bson import ObjectId

# Importaciones de librerías de terceros
from fastapi import APIRouter, Request

# Importaciones de módulos internos de la aplicación
from db.PaginatedSearch import paginated_search
from comments.BookComment import BookComment

# Creación de un router para la gestión de comentarios
SEARCH_COMMENTS = APIRouter()


@SEARCH_COMMENTS.get("/search", response_description="List all comments")
def list_comments(
        request: Request,
        book_id: str,
        reply_to: str = None,
        limit: int = 15,
        page: int = 1,
):
    """
    Recupera una lista de comentarios utilizando paginación y búsqueda.

    Args:
        request (Request): La solicitud HTTP entrante.
        book_id (str): El ID del libro al cual está relacionado el comentario.
        reply_to (str, optional): El ID del comentario al que se responde,
            si es None se buscarán los comentarios raíz (predeterminado: None).
        limit (int, optional): El número máximo de comentarios por página
            (predeterminado: 15).
        page (int, optional): La página deseada (predeterminado: 1).

    Returns:
        dict: Un diccionario que contiene datos y metadatos de la respuesta.

        - data (List[BookComment]): Una lista de objetos BookComment que
            representan los comentarios encontrados.
        - metadata (dict): Un diccionario con metadatos de paginación,
            incluyendo total, página actual y total de páginas.

    Exploración:
        La función busca comentarios en la base de datos relacionados con un
        libro específico, permitiendo la paginación y la búsqueda opcional de
        respuestas a comentarios específicos. Los parámetros de búsqueda se
        definen como sigue:

        - book_id: El ID del libro al que pertenecen los comentarios.
        - reply_to: (Opcional) El ID del comentario al que se está
            respondiendo.
        - limit: (Opcional) El número máximo de comentarios por página.
        - page: (Opcional) La página deseada.

    """
    # Realiza una búsqueda en la base de datos de comentarios utilizando
    # paginación
    query = {"book_id": ObjectId(book_id)}
    if reply_to is None:
        query["root"] = True
    else:
        query["responded_to"] = ObjectId(reply_to)

    # Realiza una búsqueda en la base de datos utilizando paginación y
    # proyección
    comments = list(
        request.app.database['book_comments'].aggregate(
            paginated_search(
                page=int(page),
                limit=int(limit),
                query=query,
                sort={
                    'created_date': -1
                },
                project=[
                    {
                        '$lookup': {
                            'from': 'users',
                            'localField': 'user_id',
                            'foreignField': '_id',
                            'as': 'user',
                        },
                    },
                    {
                        '$unwind': {
                            'path': '$user',
                            'preserveNullAndEmptyArrays': False,
                        },
                    },
                    {
                        '$addFields': {
                            'username': '$user.user',
                        },
                    },
                    {
                        '$unset': 'user',
                    },
                ],
            )
        )
    )

    # Si no se encuentran comentarios, se crea una respuesta con los datos y
    # metadatos
    response = comments[0] if len(comments) > 0 else {
        'data': [],
        'metadata': {
            'total': 0,
            'page': 0,
            'total_pages': 0,
        },
    }
    # Convierte los resultados en objetos BookComment
    response['data'] = [BookComment(**x) for x in response["data"]]
    return response
