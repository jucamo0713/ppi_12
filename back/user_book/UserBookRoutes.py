# Importaciones de módulos internos de la aplicación
from back.user_book.SearchUserBook import SEARCH_USER_BOOK
from back.user_book.UpsertUserBook import UPSERT_USER_BOOK


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
    }
]
