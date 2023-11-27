# Importaciones de librerías de terceros
import streamlit as st

# Importaciones de módulos internos de la aplicación
from components.ListUsersComponent import list_users_component
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils
from components.BookDetailComponent import book_detail_component

# Obtener la URL base
url = get_url()

# Límite de elementos a mostrar por página
LIMIT = 15


# Función para volver a la lista de libros
def volver(key: str):
    """
    Función que permite volver.

    Args:
        key (str): La clave que se eliminará de los parámetros de la URL.
    """
    params = {
        **st.experimental_get_query_params()
    }
    del params[key]
    st.experimental_set_query_params(**params)


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    """
    Función para reiniciar los parámetros de paginación en la sesión de
    Streamlit.
    """
    st.session_state.page = 1


# Función para buscar usuarios en la aplicación
def search_users(url: str,
                 page: int,
                 limit: int,
                 busqueda: str = '',
                 authentication: str = None) -> dict:
    """
    Busca usuarios en la aplicación según un término de búsqueda.

    Args:
        url (str): URL de la API.
        page (int): Número de página.
        limit (int): Límite de usuarios a recuperar por página.
        busqueda (str): Término de búsqueda para filtrar usuarios (opcional).

    Returns:
        dict: Diccionario con datos de usuarios recuperados de la API.
    """
    response = HttpUtils.get(f'{url}/user', {
        'search_param': busqueda,
        'limit': limit,
        'page': page
    }, authorization=authentication)
    if response['success']:
        return response['data']


# Configura la aplicación básica
value = basic_config(url)

if value:
    # Comprueba si se está visualizando el perfil de un usuario específico
    if "user_id" in st.experimental_get_query_params():
        # Botón para volver a la lista de usuarios
        st.button('Volver', key='volver', on_click=volver,
                  args=["user_id"])
        # Muestra el componente de perfil del usuario
        profile_component(
            st.experimental_get_query_params()["user_id"][0])
        # Botón adicional para volver a la lista de usuarios
        st.button('Volver', key='volver2', on_click=volver,
                  args=["user_id"])
    # Comprueba si se está visualizando los detalles de un libro específico
    elif "book_id" in st.experimental_get_query_params():
        # Botón para volver a la lista de libros
        st.button('Volver', key='volver', on_click=volver,
                  args=["book_id"])
        # Muestra el componente de detalles del libro
        book_detail_component(
            st.experimental_get_query_params()["book_id"][0])
        # Botón adicional para volver a la lista de libros
        st.button('Volver', key='volver2', on_click=volver,
                  args=["book_id"])
    else:
        # Muestra el componente de lista de usuarios
        list_users_component(
            lambda page, busqueda: search_users(url,
                                                page,
                                                LIMIT,
                                                busqueda,
                                                st.session_state.get(
                                                    'token',
                                                    None)))
