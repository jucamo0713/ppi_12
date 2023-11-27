# Importaciones de librerías de terceros
import streamlit as st

from components.BookDetailComponent import book_detail_component
from components.ListNotificationsComponent import list_notification_component
from components.ListUsersComponent import list_users_component
# Importaciones de módulos internos de la aplicación
from components.ProfileComponent import profile_component
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils
from utils.BasicConfig import basic_config
from utils.GuardSession import guard_session

url = get_url()


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


def search_followers(url: str, page: int,
                     limit: int, token: str,
                     busqueda: str = '', ) -> (dict):
    """
    Busca seguidores en la aplicación según un término de búsqueda.

    Args:
        url (str): URL de la API.
        page (int): Número de página.
        limit (int): Límite de usuarios a recuperar por página.
        token (str): token que valida la sesión.
        busqueda (str): Término de búsqueda para filtrar usuarios (opcional).
    Returns:
        dict: Diccionario con datos de los seguidores recuperados de la API.
    """
    response = HttpUtils.get(f'{url}/follow/followers', {
        'search_param': busqueda,
        'limit': limit,
        'page': page
    }, authorization=token)
    if response['success']:
        return response['data']


def search_following(url: str, page: int,
                     limit: int, token: str,
                     busqueda: str = '', ) -> (dict):
    """
    Busca a los usuarios seguidos en la aplicación según un término de
    búsqueda.

    Args:
        url (str): URL de la API.
        page (int): Número de página.
        limit (int): Límite de usuarios a recuperar por página.
        token (str): token que valida la sesión.
        busqueda (str): Término de búsqueda para filtrar usuarios (opcional).

    Returns:
        dict: Diccionario con datos de los usuarios seguidos recuperados de la
        API.
    """
    response = HttpUtils.get(f'{url}/follow/following', {
        'search_param': busqueda,
        'limit': limit,
        'page': page
    }, authorization=token)
    if response['success']:
        return response['data']


LIMIT = 10

# Configura la aplicación básica
value = basic_config()

if value:
    # Verifica el estado de la sesión
    data = guard_session(allow_only_signed=True)

    if (not data["is_authenticated"]
            and ("closed_session" in st.session_state
                 and st.session_state.closed_session)):
        # Comprueba que la sesión ya se ha cerrado y muestra un mensaje de
        # éxito
        st.success("Sesión cerrada exitosamente. ¡Hasta luego!")
        # Borra la marca de sesión cerrada
        del st.session_state.closed_session

    elif data["is_authenticated"]:
        # Verificar si se proporciona 'book_id' en la URL

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
            tabs = st.tabs(["Perfil",
                            "Seguidores",
                            "Siguiendo",
                            "Notificaciones"])
            with tabs[0]:
                # Muestra el componente del perfil del usuario
                profile_component()
            with tabs[1]:
                list_users_component(
                    lambda x, y: search_followers(url, x, LIMIT,
                                                  data['token'],
                                                  y), "Seguidores")
            with tabs[2]:
                list_users_component(
                    lambda x, y: search_following(url,
                                                  x,
                                                  LIMIT,
                                                  data['token'],
                                                  y),
                    "Seguido")
            with tabs[3]:
                list_notification_component()
