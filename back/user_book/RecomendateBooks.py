# Importaciones de librerías necesarias
import numpy as np
from bson import ObjectId
from fastapi import APIRouter, Request, Header

from book.Book import Book
from jwt_utils.Guard import validate_token
from user_book.ConsolidatedAggergatte import consolidated_aggregate

import networkx as nx

# Crear un router para la ruta /recomendate-books
RECOMENDATE_BOOKS = APIRouter()


@RECOMENDATE_BOOKS.get('/recomendate-books')
def recomendate_books(request: Request, authentication: str = Header(...)):
    """
    Endpoint para recomendar libros al usuario autenticado.

    Args:
        request (Request): Objeto Request de FastAPI.
        authentication (str): Token de autenticación pasado en la cabecera.

    Returns:
        dict: Diccionario que contiene listas de libros recomendados.
    """
    # Validar el token de autenticación
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Obtener datos consolidados de la base de datos
    data = list(request.app.database['user_books'].aggregate(
        consolidated_aggregate))[0]
    user_id = ObjectId(user_id)

    # Crear un grafo dirigido
    g = nx.DiGraph()

    # Agregar nodos y aristas al grafo
    for user in data["users"]:
        g.add_node(user["_id"], type="user", name=user["name"])
    for book in data["books"]:
        g.add_node(book["_id"], type="book", book=book)
    for relation in data["relations"]:
        if relation["read"] > 0:
            g.add_edge(relation["user_id"], relation["book_id"],
                       read=relation["read"])
            g.add_edge(relation["book_id"], relation["user_id"],
                       read=relation["read"])

    try:
        successors = g.successors(user_id)
    except nx.exception.NetworkXError:
        successors = []

    # Libros que el usuario ha leído
    user_books = set(successors)
    recommended_books = set()
    other_users = set()

    for successor in user_books:
        # Obtener los sucesores de los sucesores del usuario (libros que
        # otros usuarios han leído)
        other_users.update(g.successors(successor))

    for other_user in (set(other_users) - {user_id}):
        recommended_books.update(g.successors(other_user))

    # Filtrar libros ya leídos por el usuario
    recommended_books -= user_books

    # Ordenar libros por la cantidad de usuarios que los han leído
    recommended_books = np.array(sorted(recommended_books,
                                        key=(lambda x: g.in_degree(x)),
                                        reverse=True)[:10])
    np.random.shuffle(recommended_books)
    print(g.nodes[recommended_books[0]]["book"])
    # Obtener libros recomendados basados en otros usuarios
    recommended_books_based_on_others = [Book(**g.nodes[recommended]["book"])
                                         for
                                         recommended in recommended_books][:5]
    # Obtener libros recomendados basados en el autor de los libros leídos
    # por el usuario
    recommended_books_by_author = list(request.app.database[
        'user_books'].aggregate(
        [
            {
                '$match': {
                    'user_id': ObjectId(user_id)
                }
            },
            {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': '_id',
                    'as': 'book'
                }
            },
            {
                '$unwind': {
                    'path': '$book'
                }
            },
            {
                '$group': {
                    '_id': '$book.author',
                    'conteo': {
                        '$sum': 1
                    },
                    'books': {
                        '$push': '$book_id'
                    }
                }
            },
            {
                '$lookup': {
                    'from': 'books',
                    'localField': '_id',
                    'foreignField': 'author',
                    'as': 'book'
                }
            },
            {
                '$unwind': {
                    'path': '$book'
                }
            },
            {
                '$match': {
                    '$expr': {
                        '$not': {
                            '$in': [
                                '$book._id', '$books'
                            ]
                        }
                    }
                }
            },
            {
                '$project': {
                    'points': {
                        '$multiply': [
                            {
                                '$sum': [
                                    '$conteo', {
                                        '$multiply': [
                                            '$conteo', '$book.rating',
                                            '$book.total_ratings'
                                        ]
                                    }
                                ]
                            },
                            {
                                '$rand': {}
                            }]
                    },
                    '_id': '$book._id',
                    'isbn_code': '$book.isbn_code',
                    'title': '$book.title',
                    'author': '$book.author',
                    'image': '$book.image',
                    'rating': '$book.rating',
                    'total_ratings': '$book.total_ratings'
                }
            },
            {
                '$sort': {
                    'points': -1,
                    'rating': -1,
                    'total_ratings': -1
                }
            },
            {
                '$limit': 5
            }
        ]))

    return {
        "based_on_others_users": recommended_books_based_on_others,
        "based_on_author": [Book(**recommended) for recommended in
                            recommended_books_by_author]
    }
