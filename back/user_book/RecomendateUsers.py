from bson import ObjectId
from fastapi import APIRouter, Request, Header

from jwt_utils.Guard import validate_token
from user.SearchFollowing import search_following
from user.User import User
from user_book.ConsolidatedAggergatte import consolidated_aggregate

import networkx as nx

RECOMENDATE_USERS = APIRouter()


@RECOMENDATE_USERS.get('/recomendate-users')
def recomendate_users(request: Request,
                      authentication: str = Header(None)):
    """
    Endpoint para recomendar usuarios basados en libros leídos por el usuario autenticado.

    Args:
        request (Request): Objeto Request de FastAPI.
        authentication (str): Token de autenticación pasado en la cabecera.

    Returns:
        dict: Diccionario que contiene la lista de usuarios recomendados.
    """
    # Validar el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Obtener usuarios seguidos por el usuario autenticado
    followings = search_following(request, authentication, None, None)

    # Obtener datos consolidados de la base de datos
    data = list(request.app.database['user_books'].aggregate(
        consolidated_aggregate))[0]
    user_id = ObjectId(user_id)

    # Crear un grafo dirigido
    g = nx.DiGraph()

    # Agregar nodos y aristas al grafo
    for user in data["users"]:
        g.add_node(user["_id"], type="user", user=user)
    for book in data["books"]:
        g.add_node(book["_id"], type="book")
    for relation in data["relations"]:
        if relation["read"] > 0:
            g.add_edge(relation["user_id"], relation["book_id"],
                       read=relation["read"])
            g.add_edge(relation["book_id"], relation["user_id"],
                       read=relation["read"])

    # Libros que el usuario ha leído
    try:
        successors = g.successors(user_id)
    except nx.exception.NetworkXError:
        successors = []
    user_books = set(successors)

    other_users = set()

    for successor in user_books:
        # Obtener los sucesores de los sucesores del usuario
        other_users.update(g.successors(successor))

    # Filtrar usuarios ya seguidos por el usuario
    other_users -= {user_id, *[follow.id for follow in followings["data"]]}

    # Ordenar usuarios por la cantidad de libros que han leído
    other_users = sorted(other_users, key=lambda x: g.in_degree(x),
                         reverse=True)

    other_users = other_users if len(other_users) > 0 else []

    return {
        "based_on_books_read": [User(**g.nodes[recommended]["user"]) for
                                recommended in other_users[:5]],
    }
