from notifications.DeleteNotification import DELETE_NOTIFICATION
from notifications.SearchAllNotifications import SEARCH_ALL_NOTIFICATIONS

# Definición de las rutas y controladores
NOTIFICATIONS_ROUTES = [
    {
        'path': '/notifications',
        'tag': 'Notification',
        'instance': SEARCH_ALL_NOTIFICATIONS
    },
    {
        'path': '/notifications',
        'tag': 'Notification',
        'instance': DELETE_NOTIFICATION
    }
]
