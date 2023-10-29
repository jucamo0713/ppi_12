# Importaciones de módulos internos de la aplicación
from back.auth.Login import LOGIN
from back.auth.Register import REGISTER

# Definición de las rutas y controladores
AuthRoutes = [{'path': '/auth',
               'tag': 'Auth',
               'instance': REGISTER},
              {'path': '/auth',
               'tag': 'Auth',
               'instance': LOGIN}
              ]
