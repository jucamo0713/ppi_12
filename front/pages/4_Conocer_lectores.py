# Importaciones de librerías de terceros
import streamlit as st

from components.ListUsersComponent import list_users_component
# Importaciones de módulos internos de la aplicación
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils
from components.BookDetailComponent import book_detail_component

# Obtener la URL base
url = get_url()

LIMIT = 15


# Función para volver a la lista de libros
def volver(key: str):
    """
    Función que permite volver.
    """
    params = {
        **st.experimental_get_query_params()
    }
    del params[key]
    st.experimental_set_query_params(**params)


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    st.session_state.page = 1


def search_users(url: str, page: int, limit: int, busqueda: str = '') -> dict:
    response = HttpUtils.get(f'{url}/user', {
        'search_param': busqueda,
        'limit': limit,
        'page': page
    })
    if response['success']:
        return response['data']


# Configura la aplicación básica
value = basic_config(url)

if value:
    # Verifica el estado de la sesión
    data = guard_session(allow_only_signed=True)
    if data["is_authenticated"]:

        if "user_id" in st.experimental_get_query_params():
            st.button('Volver', key='volver', on_click=volver,
                      args=["user_id"])
            profile_component(
                st.experimental_get_query_params()["user_id"][0])
            st.button('Volver', key='volver2', on_click=volver,
                      args=["user_id"])
        elif "book_id" in st.experimental_get_query_params():
            st.button('Volver', key='volver', on_click=volver,
                      args=["book_id"])
            book_detail_component(
                st.experimental_get_query_params()["book_id"][0])
            st.button('Volver', key='volver2', on_click=volver,
                      args=["book_id"])
        else:
            list_users_component(lambda page, busqueda: search_users(url, page,
                                                                     LIMIT,
                                                                     busqueda))
