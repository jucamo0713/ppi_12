# Importaciones de módulos internos de la aplicación
from auth.Login import LOGIN
from auth.Register import REGISTER

# Definición de las rutas y controladores
AuthRoutes = [{'path': '/auth',
               'tag': 'Auth',
               'instance': REGISTER},
              {'path': '/auth',
               'tag': 'Auth',
               'instance': LOGIN}
              ]
