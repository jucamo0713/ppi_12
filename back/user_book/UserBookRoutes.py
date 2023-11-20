# Importaciones de módulos internos de la aplicación
from user_book.GenerateStatistics import GENERATE_STATISTICS
from user_book.RecomendateBooks import RECOMENDATE_BOOKS
from user_book.RecomendateUsers import RECOMENDATE_USERS
from user_book.SearchUserBook import SEARCH_USER_BOOK
from user_book.SearchUserBooksListsBooks import SEARCH_ALL_USER_BOOKS
from user_book.UpsertUserBook import UPSERT_USER_BOOK

# Definición de las rutas y controladores
USER_BOOK_ROUTES = [
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': SEARCH_USER_BOOK
    },
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': UPSERT_USER_BOOK
    },
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': SEARCH_ALL_USER_BOOKS
    },
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': GENERATE_STATISTICS
    },
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': RECOMENDATE_BOOKS
    },
    {
        'path': '/user_book',
        'tag': 'User_Book',
        'instance': RECOMENDATE_USERS
    }
]
