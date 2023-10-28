# Importar librerías necesarias
import numpy as np
# Para manipular imagenes
import skimage.io
# Para hacer solicitudes HTTP
import requests
# Para crear la aplicación web
import streamlit as st
from io import BytesIO
from fake_useragent import UserAgent

from components.BookDetailComponent import book_detail_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url

ua = UserAgent()
url = get_url()
value = basic_config(url=url)

LIMIT = 15


# Función para volver a la lista de libros
def volver():
    """
    Función que permite volver del detalle al listado.
    """
    del st.experimental_get_query_params()['book_id']
    st.experimental_set_query_params()


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    st.session_state.page = 1


if value:
    # Verificar si se proporciona 'book_id' en la URL
    if "book_id" in st.experimental_get_query_params():
        book_detail_component(st.experimental_get_query_params()["book_id"][0], url=url)
        book = {}
        st.button('Volver', key='volver', on_click=volver)
    else:
        # Inicializar el estado de la sesión para el paginado
        if 'page' not in st.session_state:
            st.session_state.page = 1

        # Definir los parámetros de paginación (limit y page) basados en el
        # estado de la sesión
        pagination = {
            'limit': LIMIT,
            'page': st.session_state.page
        }
        # Título de la página
        st.header("Explora y descubre nuevos autores y libros")

        # Barra de búsqueda
        busqueda = st.text_input("Buscar libro",
                                 on_change=lambda: restart_pagination_params())

        # Realizar una solicitud a la API para obtener una lista de libros
        response = requests.get(f"{url}/books", {
            'search_param': busqueda,
            'limit': pagination['limit'],
            'page': pagination['page']
        }).json()
        # Lista de libros
        libros = response['data']
        # Metadatos
        metadata = response['metadata']

        columnas = st.columns(5)

        # Mspeo de todos los libros
        for i, resultado in enumerate(libros):
            # Se coloca un separador cada vez que termine una fila
            if i != 0 and i % 5 == 0:
                st.markdown("---")
                columnas = st.columns(5)

            # Alternar entre las 5 columnas
            with ((columnas[i % 5])):
                user_agent = ua.random
                data_image = requests.get(resultado["image"], headers={
                    "User-Agent": user_agent
                })
                if data_image.status_code == 200:
                    # Se crea BytesIO object para que actue como un archivo
                    # falso
                    img_file = BytesIO(data_image.content)
                    try:
                        # Read the image using 'skimage.io.imread'
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
                        image = ("https://islandpress.org/sites/default/files"
                                 "/default_book_cover_2015.jpg")
                else:
                    image = ("https://islandpress.org/sites/default/files"
                             "/default_book_cover_2015.jpg")
                st.image(image,
                         use_column_width=True, )
                if len(resultado["title"]) > 30:
                    resultado["title"] = resultado["title"][:30] + "..."

                if len(resultado["author"]) > 30:
                    resultado["author"] = resultado["author"][:30] + "..."
                st.write("**Título:**", resultado["title"])
                st.write("**Autor:**", resultado["author"])
                st.button('Detalle', key=f'detail{i}',
                          on_click=(lambda x: st.experimental_set_query_params(
                              book_id=x)), args=[resultado["_id"]])
        # Paginación
        if metadata['totalPages'] > 1:
            st.write(
                f"Mostrando página {pagination['page']} de "
                f"{int(metadata['totalPages'])}")
            st.number_input("page",
                            key="page",
                            label_visibility='hidden',
                            step=1, min_value=1,
                            max_value=int(metadata['totalPages']))
        st.markdown("---")

        # Mensaje si no hay resultados
        if not libros:
            st.info("No se encontraron resultados para la búsqueda.")
