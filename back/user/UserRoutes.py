# Importaciones de módulos internos de la aplicación
from user.FollowUser import FOLLOW_USER
from user.Me import ME
from user.SearchAllUsers import SEARCH_ALL_USERS
from user.SearchUserById import SEARCH_USER_BY_ID
from user.UnfollowUser import UNFOLLOW_USER
from user.UpdateUsers import UPDATE_USERS
from user.ValidateFollow import VALIDATE_IF_FOLLOWING

# Definición de las rutas y controladores
USER_ROUTES = [{'path': '/user',
                'tag': 'User',
                'instance': ME},
               {'path': '/user',
                'tag': 'User',
                'instance': SEARCH_USER_BY_ID},
               {'path': '/user',
                'tag': 'User',
                'instance': SEARCH_ALL_USERS},
               {'path': '/user',
                'tag': 'User',
                'instance': UPDATE_USERS},
               {'path': '/follow',
                'tag': 'Follow',
                'instance': FOLLOW_USER},
               {'path': '/unfollow',
                'tag': 'Follow',
                'instance': UNFOLLOW_USER},
               {'path': '/follow',
                'tag': 'Follow',
                'instance': VALIDATE_IF_FOLLOWING}
               ]
