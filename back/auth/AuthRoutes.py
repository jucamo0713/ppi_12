from .Login import LOGIN
from .Register import REGISTER

# Definición de las rutas y controladores
AuthRoutes = [{'path': '/auth',
               'tag': 'Auth',
               'instance': REGISTER},
              {'path': '/auth',
               'tag': 'Auth',
               'instance': LOGIN}
              ]
