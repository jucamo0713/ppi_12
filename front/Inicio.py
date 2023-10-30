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

from components.BookCard import book_card
from components.BookDetailComponent import book_detail_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url

ua = UserAgent()
url = get_url()
value = basic_config(url=url)

LIMIT = 15


# TODO: comentar más


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
        st.button('Volver', key='volver', on_click=volver)
        book_detail_component(st.experimental_get_query_params()["book_id"][0],
                              url=url)
        st.button('Volver', key='volver2', on_click=volver)
    else:
        # Inicializar el estado de la sesión para el paginado
        if 'page' not in st.session_state:
            st.session_state.page = 1

        # Título de la página
        st.header("Explora y descubre nuevos autores y libros")

        # Barra de búsqueda
        busqueda = st.text_input("Buscar libro",
                                 on_change=lambda: restart_pagination_params())

        # Realizar una solicitud a la API para obtener una lista de libros
        response = requests.get(f"{url}/books", {
            'search_param': busqueda,
            'limit': LIMIT,
            'page': st.session_state.page
        }).json()
        # Lista de libros
        libros = response['data']
        # Metadatos
        metadata = response['metadata']

        columnas = st.columns(5)

        # Mapeo de todos los libros
        for i, resultado in enumerate(libros):
            # Se coloca un separador cada vez que termine una fila
            if i != 0 and i % 5 == 0:
                st.markdown("---")
                columnas = st.columns(5)

            # Alternar entre las 5 columnas
            with ((columnas[i % 5])):
                book_card(resultado)
        # Paginación
        if metadata['total_pages'] > 1:
            st.write(
                f"Mostrando página {st.session_state.page} de "
                f"{int(metadata['total_pages'])}")
            st.number_input("page",
                            key="page",
                            label_visibility='hidden',
                            step=1, min_value=1,
                            max_value=int(metadata['total_pages']))
        st.markdown("---")

        # Mensaje si no hay resultados
        if not libros:
            st.info("No se encontraron resultados para la búsqueda.")
