# Importaciones de librerías de terceros
import pandas as pd
from bson import ObjectId
from fastapi import APIRouter, Request, Header

from jwt_utils.Guard import validate_token

# Configura el enrutador para generar estadísticas
GENERATE_STATISTICS = APIRouter()


@GENERATE_STATISTICS.get("/statistics",
                         response_description="statistics of user")
def generate_statistics(request: Request,
                        user_id: str = None,
                        authentication: str = Header(None)):
    """
    Genera estadísticas sobre los libros del usuario.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        user_id (str): Identificador del usuario (opcional).
        authentication (str): Token de autenticación en la cabecera.

    Returns:
        dict: Estadísticas generadas sobre los libros del usuario.

    """
    # Valida el token de autenticación utilizando la función validate_token
    if user_id is None:
        token_data = validate_token(authentication)
        user_id = token_data['id']

    # Definir la consulta de agregación para obtener los libros del usuario
    query = [
        {
            '$match': {
                'user_id': ObjectId(user_id)
            }
        }, {
            '$lookup': {
                'from': 'books',
                'localField': 'book_id',
                'foreignField': '_id',
                'as': 'book'
            }
        }, {
            '$unwind': {
                'path': '$book',
                'preserveNullAndEmptyArrays': False
            }
        }
    ]

    # Ejecutar la consulta de agregación en la base de datos
    user_books = list(request.app.database['user_books'].aggregate(query))

    # Verificar si hay libros del usuario
    if len(user_books) > 0:
        # Crear un DataFrame de Pandas para facilitar el análisis
        data = pd.DataFrame(user_books)

        # Obtener los 5 principales autores más leídos
        top_authors = data['book'].apply(lambda x: x[
            'author']).value_counts().head(5)

        # Filtrar los libros leídos, en progreso y favoritos
        reads = data[data['read'] >= 1]
        reading = data[data['reading']]
        favorite = data[data['favorite']]

        # Obtener los 5 libros más leídos
        top_reads = reads.sort_values(by='read', ascending=False).head(5)

        # Devolver las estadísticas generadas
        return {
            "distribution": {
                "reads": len(reads),
                "reading": len(reading),
                "favorite": len(favorite),
            },
            "top_authors": {'authors': top_authors.index.tolist(),
                            'counts': top_authors.tolist()},
            "top_more_reads": {
                'books': top_reads['book'].apply(lambda x: x[
                    'title']).tolist(),
                'read_values': top_reads['read'].tolist()
            }
        }
    else:
        # Devolver cero si no hay libros del usuario
        return {"distribution": {
            "reads": 0,
            "reading": 0,
            "favorite": 0,
        }}
