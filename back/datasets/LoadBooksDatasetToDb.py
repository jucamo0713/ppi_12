import pandas as pd
from fastapi import APIRouter, Request

# Define una ruta para cargar el conjunto de datos de libros en la base de
# datos.
LOAD_BOOKS_DATASET_TO_DB = APIRouter()


@LOAD_BOOKS_DATASET_TO_DB.post("/books")
def load_dataset(request: Request):
    """
    Carga un conjunto de datos de libros desde una hoja de cálculo en línea
    y lo almacena en una base de datos.

    Args:
    - request (Request): La solicitud HTTP recibida.

    Returns:
    - bool: True si la carga de datos se realizó correctamente.

    El conjunto de datos se lee desde una hoja de cálculo en línea y se itera
    a través de las filas para obtener la información de cada libro. Si un
    libro ya existe en la base de datos, se actualizan sus detalles. Si no
    existe, se inserta en la base de datos.

    La carga de datos se realiza a través de una solicitud POST a esta ruta.

    Ejemplo de uso:
    POST a api/datasets/books para cargar el conjunto de datos en la base de
    datos.
    """
    dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX'
                          '-1vQswyZDh8WqwD_33LwqY57Iiqlk3NaZ0GkJ5pznOVUQE'
                          '2wl_VY30x2mKE-jGLkzUsUZ7Ypvk1TkNvoU/pub?gid='
                          '665845743&single=true&output=csv')

    # Itera a través de las filas del conjunto de datos.
    for position in range(dataset.shape[0]):
        book = dataset.loc[position]
        request.app.database['books'].find_one_and_update({
            "isbn_code": str(book['ISBN'])
        }, {"$set": {
            "isbn_code": str(book['ISBN']),
            "title": str(book["Book-Title"]),
            "author": str(book["Book-Author"]),
            "image": str(book["Image-URL-L"])
        }}, upsert=True)
    # Devuelve True par indicar que la carga de datos se realizó con éxito.
    return True
