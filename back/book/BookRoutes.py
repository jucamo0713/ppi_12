# Importaciones de módulos internos de la aplicación
from back.book.SearchAllBooks import SEARCH_ALL_BOOKS
from back.book.SearchBookById import SEARCH_BOOK_BY_ID


# Definición de las rutas y controladores
BookRoutes = [{'path': '/books',
               'tag': 'Books',
               'instance': SEARCH_ALL_BOOKS},
              {'path': '/books',
               'tag': 'Books',
               'instance': SEARCH_BOOK_BY_ID}
              ]
