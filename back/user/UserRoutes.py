# Importaciones de módulos internos de la aplicación
from user.Me import ME
from user.SearchUserById import SEARCH_USER_BY_ID

# Definición de las rutas y controladores
USER_ROUTES = [{'path': '/user',
                'tag': 'User',
                'instance': ME},
               {'path': '/user',
                'tag': 'User',
                'instance': SEARCH_USER_BY_ID}
               ]
