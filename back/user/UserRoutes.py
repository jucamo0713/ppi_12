# Importaciones de módulos internos de la aplicación
from back.user.Me import ME


# Definición de las rutas y controladores
USER_ROUTES = [{'path': '/user',
                'tag': 'User',
                'instance': ME}
               ]
