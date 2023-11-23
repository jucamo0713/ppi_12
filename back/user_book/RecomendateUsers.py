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
    token_data = validate_token(authentication)
    user_id = token_data['id']
    followings = search_following(request, authentication, None, None)
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
        succesors = g.successors(user_id)
    except nx.exception.NetworkXError:
        succesors = []
    user_books = set(succesors)
    other_users = set()
    for successor in user_books:
        # Obtener los sucesores de los sucesores del usuario
        other_users.update(g.successors(successor))
    other_users -= {user_id, *[follow.id for follow in followings["data"]]}
    # Ordenar libros por la cantidad de usuarios que los han leído
    other_users = sorted(other_users, key=lambda x: g.in_degree(x),
                         reverse=True)
    other_users = other_users if len(other_users) > 0 else []
    return {
        "based_on_books_read": [User(**g.nodes[recommended]["user"]) for
                                recommended in other_users[:5]],
    }
