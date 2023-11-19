import textwrap

import streamlit as st

from components.BookCard import book_card
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils

import matplotlib.pyplot as plt
from collections import Counter  # TODO: Quitar


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
                      user_token: str, user_id: str = None, search_param: str =
                      ""):
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
                                    "search_param": search_param,
                                    "user_id": user_id},
                             authorization=user_token)
    if response['success']:
        return response['data']
    else:
        return []


def search_statistics(url: str, user_id: str = None, user_token: str = None):
    response = HttpUtils.get(f'{url}/user_book/statistics',
                             query={
                                 "user_id": user_id},
                             authorization=user_token)
    if response['success']:
        return response['data']
    else:
        return None


def search_user_data(url: str, user_id: str):
    response = HttpUtils.get(f'{url}/user/by-id',
                             query={"id": user_id})
    if response['success']:
        return response['data']
    else:
        return None


def profile_component(user_id: str = None):
    """
    Muestra el componente de perfil de usuario si el usuario está autenticado.

    Retorna:
        bool: True si el usuario está autenticado y se muestra el perfil,
        False en caso contrario.

    Ejemplo:
    >>> profile_component()
    """
    url = get_url()
    if user_id is not None:
        usuario = search_user_data(url, user_id)
        name = usuario["name"]
        st.title(f"Bienvenido!")
        st.title(f"Soy {name}!")
        data = {
            "Nombre": name,
            "Usuario": usuario["user"],
            "Correo": usuario["email"],
            "Fecha de nacimiento": usuario["burn_date"],
            "Fecha de registro": usuario["registered_date"]
        }
    else:
        usuario = st.session_state.user
        name = usuario["name"]
        st.title(f"Bienvenido, {name}!")
        data = {
            "Nombre": name,
            "Usuario": usuario["user"],
            "Correo": usuario["email"],
            "Fecha de nacimiento": usuario["burn_date"],
            "Fecha de registro": usuario["registered_date"]
        }
        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)

    st.table(data)
    st.title("Mis Libros")
    my_books_tabs = ["Leídos", "En Proceso de Lectura", "Favoritos"]
    read, reading, favorite = st.tabs(my_books_tabs)
    token = st.session_state.token if "token" in st.session_state else None
    with read:
        read_books = \
            search_user_books(url, "read", 5, 1,
                              token, user_id)["data"]
        read_columns = st.columns(5)
        for index, data in enumerate(read_books):
            with read_columns[index]:
                book_card(data, "read")
    with reading:
        reading_books = \
            search_user_books(url, "reading", 5, 1,
                              token, user_id)["data"]
        reading_columns = st.columns(5)
        for index, data in enumerate(reading_books):
            with reading_columns[index]:
                book_card(data, "reading")
    with favorite:
        favorite_books = \
            search_user_books(url, "favorite", 5, 1,
                              token, user_id)["data"]
        favorite_columns = st.columns(5)
        for index, data in enumerate(favorite_books):
            with favorite_columns[index]:
                book_card(data, "favorites")

    # Estadísticos de lectura
    st.title("Mis estadísticos de lectura")
    estadisticos = search_statistics(url, user_id, token)

    # Crear un gráfico de torta
    fig, ax = plt.subplots()

    total_leidos = estadisticos["distribution"]["reads"]
    total_favoritos = estadisticos["distribution"]["reading"]
    total_progreso = estadisticos["distribution"]["favorite"]
    # Datos para el gráfico de torta
    datos_torta = [total_leidos,
                   total_favoritos,
                   total_progreso,
                   ]
    etiquetas = [f'Leídos\n({total_leidos} libros)',
                 f'Favoritos\n({total_favoritos} libros)',
                 f'En Progreso\n({total_progreso} libros)']

    # Crear el gráfico de torta
    ax.pie(datos_torta, labels=etiquetas, autopct='%1.1f%%', startangle=90,
           counterclock=False)

    # Equal aspect ratio asegura que el gráfico de torta sea circular.
    ax.axis('equal')
    ax.set_title('Distribución de Libros por Categoría')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Crear un gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(estadisticos["top_authors"]["authors"],
           estadisticos["top_authors"]["counts"])
    ax.set_xlabel('Autores')
    ax.set_ylabel('Número de Libros')
    ax.set_title('Top 5 Autores Más Leídos')
    plt.xticks(rotation=-15)
    # Establecer el formato de los ticks del eje y para asegurar números
    # enteros
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Crear un gráfico de barras
    fig, ax = plt.subplots()
    ax.barh([textwrap.shorten(x, 25) for x in estadisticos["top_more_reads"][
        "books"]],
            estadisticos["top_more_reads"]["read_values"])
    ax.set_ylabel('Libros')
    ax.set_xlabel('Número de Lecturas')
    ax.set_title('Top Libros mas veces leído')
    # Establecer el formato de los ticks del eje y para asegurar números
    # enteros
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
