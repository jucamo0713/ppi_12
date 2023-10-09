import re
from typing import List

from fastapi import APIRouter, Request

from .Book import Book
from ..db.PaginatedSearch import paginated_search

SearchAllBooks = APIRouter()


# class SearchBooksResponse(PaginatedSearchResponse):
#     data: List[Book]


@SearchAllBooks.get("/", response_description="List all books")
def list_books(request: Request, limit=15, page=1, search_param=''):
    books = list(request.app.database['books'].aggregate(paginated_search(
        page=int(page), limit=int(limit),
        query={
            '$or': [
                {'titulo': re.compile(f'{search_param}', re.IGNORECASE)},
                {'autor': re.compile(f'{search_param}', re.IGNORECASE)}
            ]})))
    response = books[0] if len(books) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'totalPages': 0, }}
    return response
