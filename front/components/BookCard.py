# Importaciones de la biblioteca estándar
import textwrap
from io import BytesIO

# Importaciones de bibliotecas relacionadas con terceros
import numpy as np
import requests
import skimage
import streamlit as st

# Importaciones de módulos y paquetes locales
from fake_useragent import UserAgent

ua = UserAgent()

# Constantes con letras mayúsculas
MAX_SIZE_TEXT = 30


# Definición de la función book_card
def book_card(book, key: str = None):
    """
    Crea una tarjeta que muestra información de un libro,
    incluyendo su título, autor y portada.

    Parámetros:
    book (dict): Un diccionario que contiene información del 
    libro, incluyendo "title" (título del libro), "author"
    (autor del libro) y "image" (URL de la imagen de la portada
    del libro).
    key (str, opcional): Clave única que se utiliza para
    identificar la tarjeta. Puede ser útil en una aplicación
    de Streamlit para controlar la interacción con la tarjeta.

    Uso:
    Para utilizar esta función, se pasa un diccionario 'book'
    que contiene la información del libro que se desea mostrar.
    La función mostrará la portada del libro, el título y el
    autor. Si el título o el autor son muy largos, se
    truncarán para que no excedan un límite predefinido.
    También se proporciona un botón de "Detalle" que se puede
    utilizar para realizar acciones adicionales en una aplicación
    de Streamlit, como mostrar más información sobre el libro.

    Ejemplo:
    book_data = {
        "title": "Título del Libro",
        "author": "Autor del Libro",
        "image": "URL_de_la_portada_del_libro.jpg"
    }
    book_card(book_data, key="book_card_1")
    """

    # Se crea un objeto UserAgent para generar un User-Agent
    # aleatorio
    user_agent = ua.random
    data_image = requests.get(book["image"], headers={
        "User-Agent": user_agent
    })
    if data_image.status_code == 200:
        # Se descarga y muestra la imagen de la portada del libro
        img_file = BytesIO(data_image.content)
        try:
            # Lee la imagen utilizando 'skimage.io.imread' y
            # ajusta su tamaño si es necesario
            image = skimage.io.imread(img_file)
            desired_height = image.shape[1] * 3 / 2
            crop_top = int((image.shape[0] - desired_height) // 2)
            if crop_top >= 0:
                crop_bottom = int(image.shape[0] - crop_top)
                image = image[crop_top:crop_bottom, :]
            else:
                black_part = np.zeros((-crop_top, image.shape[
                    1], 3), dtype=np.uint8)
                image = np.vstack([black_part, image, black_part])
        except Exception:
            # En caso de error al leer la imagen, se muestra una 
            # imagen predeterminada
            image = ("https://islandpress.org/sites/default/files"
                     "/default_book_cover_2015.jpg")
    else:
        # Si no se pudo descargar la imagen, se muestra una imagen 
        # predeterminada
        image = ("https://islandpress.org/sites/default/files"
                 "/default_book_cover_2015.jpg")
    # Muestra la imagen de la portada del libro
    st.image(image,
             use_column_width=True, )
    stars = "★" * round(book['rating']) + "☆" * (5 - round(book['rating']))
    # Muestra el título y el autor del libro
    st.write("**Título:**", textwrap.shorten(book["title"], MAX_SIZE_TEXT))
    st.write("**Autor:**", textwrap.shorten(book["title"], MAX_SIZE_TEXT))
    st.write("**Calificación:**",
             textwrap.shorten(
                 f"{stars} ({round(book['rating'], 2)}/5.0)", MAX_SIZE_TEXT))

    # Botón de "Detalle" que muestra el detalle del libro
    st.button('Detalle',
              key=book["_id"] if key is None else key + book["_id"],
              on_click=(lambda x: st.experimental_set_query_params(
                  book_id=x)),
              args=[book["_id"]])
