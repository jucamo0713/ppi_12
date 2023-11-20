# Importaciones de librerías de terceros
import pandas as pd
from bson import ObjectId
from fastapi import APIRouter, Request, Header

from book.Book import Book
from jwt_utils.Guard import validate_token
from user_book.UserBook import UserBook

GENERATE_STATISTICS = APIRouter()


@GENERATE_STATISTICS.get("/statistics",
                         response_description="statistics of user")
def generate_statistics(request: Request,
                        user_id: str = None,
                        authentication: str = Header(None)):
    # Validar el token de autenticación utilizando la función validate_token
    if user_id is None:
        token_data = validate_token(authentication)
        user_id = token_data['id']
    query = [
        {
            '$match': {
                'user_id': ObjectId(user_id)
            }
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
        }
    ]
    user_books = list(request.app.database['user_books'].aggregate(query))
    data = pd.DataFrame(user_books)
    top_authors = data['book'].apply(
        lambda x: x['author']).value_counts().head(5)
    reads = data[data['read'] >= 1]
    reading = data[data['reading']]
    favorite = data[data['favorite']]
    top_reads = reads.sort_values(by='read', ascending=False).head(5)
    return {
        "distribution": {
            "reads": len(reads),
            "reading": len(reading),
            "favorite": len(favorite),
        },
        "top_authors": {'authors': top_authors.index.tolist(),
                        'counts': top_authors.tolist()},
        "top_more_reads": {
            'books': top_reads['book'].apply(lambda x: x['title']).tolist(),
            'read_values': top_reads['read'].tolist()
        }
    }
