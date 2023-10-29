# Importaciones de librerías de terceros
from fastapi import APIRouter, Request, Header
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

# Importaciones de módulos internos de la aplicación
from comments.BookComment import BookComment
from jwt_utils.Guard import validate_token


# Define un enrutador para los comentarios de libros
CREATE_COMMENT = APIRouter()


# Modelo de solicitud para crear un comentario de libro
class CreateBookCommentRequest(BaseModel):
    book_id: str
    content: str
    responded_to: str = None  # Este campo es opcional


# Controlador para crear un comentario de libro
@CREATE_COMMENT.post("/comments/")
def create_book_comment(request: Request, body: CreateBookCommentRequest,
                        authentication: str = Header(...)):
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']
    data = dict(
        user_id=ObjectId(user_id),
        book_id=ObjectId(body.book_id),
        content=body.content,
        root=True if not body.responded_to else False,
        created_date=datetime.now()
    )
    if body.responded_to:
        data['responded_to'] = ObjectId(body.responded_to)
    id = request.app.database['book_comments'].insert_one(data).inserted_id
    new_comment_data = request.app.database['book_comments'].find_one({"_id": id})
    new_comment = BookComment(**new_comment_data)
    return new_comment
