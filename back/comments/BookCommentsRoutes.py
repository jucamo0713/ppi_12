from comments.CreateComment import CREATE_COMMENT

# Definición de las rutas y controladores
BOOK_COMMENTS_ROUTES = [{'path': '/comments',
                         'tag': 'Comments',
                         'instance': CREATE_COMMENT}
                        ]
