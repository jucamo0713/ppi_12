# Importar librerías necesarias
import requests
import streamlit as st
from fake_useragent import UserAgent

# Importaciones de módulos internos de la aplicación
from components.BookCard import book_card
from components.BookDetailComponent import book_detail_component
from components.ListBooksComponent import list_books_component
from components.ListUsersComponent import restart_pagination_params
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    """
    Función para reiniciar los parámetros de paginación en la sesión de
    Streamlit.
    """
    st.session_state["page"] = 1


# Inicialización de UserAgent para generar el User-Agent
ua = UserAgent()

# Obtener la URL base
url = get_url()

# Configuración básica de la aplicación web
value = basic_config(url=url)

# Número máximo de libros a mostrar por página
LIMIT = 15


def search_all_books(url: str, page: int, limit: int, busqueda: str = ""):
    service_response = HttpUtils.get(f"{url}/books", query={
        'search_param': busqueda,
        'limit': limit,
        'page': page
    })
    if service_response['success']:
        return service_response["data"]
    else:
        return {
            "data": [],
            "metadata": {}
        }


# Función para volver a la lista de libros
def volver(value: str):
    """
    Función que permite volver.
    """
    params = {
        **st.experimental_get_query_params()
    }
    del params[value]
    st.experimental_set_query_params(**params)


# Verifica si 'value' tiene un valor verdadero, lo que significa que la
# configuración básica fue exitosa.
if value:

    if 'user_id' in st.experimental_get_query_params():
        st.button('Volver', key='volver', on_click=volver, args=['user_id'])
        profile_component(st.experimental_get_query_params()['user_id'][0])
        st.button('Volver', key='volver2', on_click=volver, args=['user_id'])
    # Verificar si se proporciona 'book_id' en la URL
    elif "book_id" in st.experimental_get_query_params():

        # Muestra un botón "Volver" que llama a la función 'volver' cuando
        # se hace clic.
        st.button('Volver', key='volver', on_click=volver, args=['book_id'])

        # Llama al componente 'book_detail_component' con el valor de
        # 'book_id' y la URL.
        book_detail_component(st.experimental_get_query_params()["book_id"][0],
                              url=url)
        # Muestra otro botón "Volver" para proporcionar otra forma de regresar.
        st.button('Volver', key='volver2', on_click=volver, args=['book_id'])

    else:
        # Si 'book_id' no está en la URL, muestra la lista de libros.
        # Título de la página
        st.header("Explora y descubre nuevos autores y libros")
        # Listado
        list_books_component(
            lambda page, search:
            search_all_books(url,
                             page,
                             LIMIT,
                             search),
            "general")
