import streamlit as st
from components.BookCard import book_card
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils


def close_session():
    """
    Cierra la sesión del usuario, eliminando el token de sesión y los datos
    del usuario, y marca la sesión como cerrada.
    """
    # Borra el token de sesión y los datos del usuario
    del st.session_state.token
    del st.session_state.user
    # Marca la sesión como cerrada
    st.session_state.closed_session = True


def search_user_books(url: str, type_list: str, limit: int, page: int,
                      user_token: str, search_param: str = ""):
    """
    Busca los libros del usuario según el tipo especificado.

    Args:
        url (str): URL de la API.
        type_list (str): Tipo de lista de libros a buscar (ej. "read",
        "reading", "favorite").
        limit (int): Límite de libros a recuperar.
        page (int): Número de página.
        user_token (str): Token de autenticación del usuario.
        search_param (str): Parámetro de búsqueda (opcional).

    Retorna:
        list: Lista de libros del usuario.

    Ejemplo:
    >>> search_user_books('https://api.com', 'read', 5, 1, 'token123',
    'Python')
    """
    response = HttpUtils.get(f'{url}/user_book/list/{type_list}',
                             query={"limit": limit, "page": page,
                                    "search_param": search_param},
                             authorization=user_token)
    if response['success']:
        return response['data']
    else:
        return []


def profile_component():
    """
    Muestra el componente de perfil de usuario si el usuario está autenticado.

    Retorna:
        bool: True si el usuario está autenticado y se muestra el perfil,
        False en caso contrario.

    Ejemplo:
    >>> profile_component()
    """
    url = get_url()
    usuario = st.session_state.user
    if "user" in st.session_state:
        name = usuario["name"]
        st.title(f"Bienvenido, {name}!")
        data = {
            "Nombre": name,
            "Usuario": usuario["user"],
            "Correo": usuario["email"],
            "Fecha de nacimiento": usuario["burn_date"],
            "Fecha de registro": usuario["registered_date"]
        }
        st.table(data)
        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)
        st.title("Mis Libros")
        my_books_tabs = ["Leídos", "En Proceso de Lectura", "Favoritos"]
        read, reading, favorite = st.tabs(my_books_tabs)
        with read:
            read_books = \
                search_user_books(url, "read", 5, 1, st.session_state.token)[
                    "data"]
            read_columns = st.columns(5)
            for index, data in enumerate(read_books):
                with read_columns[index]:
                    book_card(data, "read")
        with reading:
            reading_books = \
                search_user_books(url, "reading", 5, 1,
                                  st.session_state.token)[
                    "data"]
            reading_columns = st.columns(5)
            for index, data in enumerate(reading_books):
                with reading_columns[index]:
                    book_card(data, "reading")
        with favorite:
            favorite_books = \
                search_user_books(url, "favorite", 5, 1,
                                  st.session_state.token)[
                    "data"]
            favorite_columns = st.columns(5)
            for index, data in enumerate(favorite_books):
                with favorite_columns[index]:
                    book_card(data, "favorites")
        return True
    else:
        return False
