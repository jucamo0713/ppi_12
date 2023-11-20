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
    """
    Modelo de datos para la creación de un comentario en un libro.

    Atributos:
    - `book_id` (str): Identificador del libro al que se agrega el comentario.
    - `content` (str): Contenido del comentario.
    - `responded_to` (str, opcional): Identificador del comentario al que se
    está respondiendo, si es una respuesta.
      Por defecto, es `None`.

    """
    book_id: str
    content: str
    responded_to: str = None


# Controlador para crear un comentario de libro
@CREATE_COMMENT.post("/create",
                     summary="Crea un comentario de libro")
def create_book_comment(request: Request, body: CreateBookCommentRequest,
                        authentication: str = Header(...)):
    """
    Crea un comentario de libro.

    Args:
        request (Request): La solicitud HTTP entrante.
        body (CreateBookCommentRequest): Datos del comentario a crear.
        authentication (str): Token de autenticación en la cabecera.

    Returns:
        BookComment: El comentario de libro creado.
    """
    # Validar el token de autenticación utilizando la función validate_token
    token_data = validate_token(authentication)
    user_id = token_data['id']

    # Creación de un nuevo comentario con los datos proporcionados
    data = {
        # ID del usuario que realizó el comentario
        "user_id": ObjectId(user_id),
        # ID del libro al que se refiere el comentario
        "book_id": ObjectId(body.book_id),
        # Contenido del comentario
        "content": body.content,
        # Indica si es un comentario raíz o una respuesta
        "root": not body.responded_to,
        # Fecha y hora de creación del comentario
        "created_date": datetime.now(),
        # Inicialmente no tiene respuestas
        "has_responses": False
    }

    # Si se está respondiendo a un comentario existente, se registra la
    # respuesta.
    if body.responded_to:
        data['responded_to'] = ObjectId(body.responded_to)

    # Inserta el nuevo comentario en la base de datos y obtiene su ID
    id = request.app.database['book_comments'].insert_one(data).inserted_id

    # Busca los datos del nuevo comentario en la base de datos
    new_comment_data = request.app.database['book_comments'].find_one(
        {"_id": id})

    # Crea un objeto BookComment a partir de los datos del comentario
    new_comment = BookComment(**new_comment_data)

    # Si el nuevo comentario es una respuesta a otro comentario,
    # se actualiza el estado de "has_responses" del comentario original
    if new_comment.responded_to is not None:
        request.app.database['book_comments'].find_one_and_update(
            {
                "_id": new_comment.responded_to
            },
            {
                "$set":
                    {
                        "has_responses": True
                    }
            })

    # Retorna el nuevo comentario creado
    return new_comment
