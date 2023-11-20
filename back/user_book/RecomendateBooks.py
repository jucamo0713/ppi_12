import pandas as pd
from bson import ObjectId
from fastapi import APIRouter, Request, Header

from book.Book import Book
from user_book.ConsolidatedAggergatte import consolidated_aggregate

import networkx as nx

RECOMENDATE_BOOKS = APIRouter()


@RECOMENDATE_BOOKS.get('/recomendate-books')
def recomendate_books(request: Request, user_id: str):
    data = list(request.app.database['user_books'].aggregate(
        consolidated_aggregate))[0]
    user_id = ObjectId(user_id)
    # Crear un grafo dirigido
    g = nx.DiGraph()
    # Agregar nodos y aristas al grafo
    authors = set()
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
    user_books = set(g.successors(user_id))  # Libros que el usuario ha leído
    recommended_books = set()
    other_users = set()
    for successor in user_books:
        # Obtener los sucesores de los sucesores del usuario (libros que
        # otros usuarios han leído)
        other_users.update(g.successors(successor))
    for user in (set(other_users) - {user_id}):
        recommended_books.update(g.successors(user))
    # Filtrar libros ya leídos por el usuario
    recommended_books -= user_books
    # Ordenar libros por la cantidad de usuarios que los han leído
    recommended_books = sorted(recommended_books, key=lambda x: g.in_degree(x),
                               reverse=True)
    recommended_books_by_author = list(request.app.database[
        'user_books'].aggregate(
        [
            {
                '$match': {
                    'user_id': ObjectId('65361222941cb8884687fefb')
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
                        '$push': 'book_id'
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
                    'book._id': {
                        '$ne': {
                            '$in': '$books'
                        }
                    }
                }
            },
            {
                '$project': {
                    'points': {
                        '$sum': [
                            '$conteo', {
                                '$multiply': [
                                    '$conteo', '$book.rating',
                                    '$book.total_ratings'
                                ]
                            }
                        ]
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
        "based_on_others_users": [Book(**g.nodes[recommended]["book"]) for
                                  recommended in recommended_books[:5]],
        "based_on_author": [Book(**recommended) for recommended in
                            recommended_books_by_author]
    }
