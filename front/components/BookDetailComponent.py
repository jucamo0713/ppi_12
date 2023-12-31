# Importaciones de librerías Nativas
from datetime import datetime
from math import floor

# Importaciones de librerías de terceros
import streamlit as st

from components.CommentsComponent import comments_component
# Importaciones de módulos internos de la aplicación
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils

DEFAULT_COMMENTS_LIMIT = 5


def increment_comments_limit(value: int = None, element='main'):
    """
    Incrementa el límite de comentarios para una sección específica.

    Args:
        value (int): El valor a incrementar (opcional).
        element (str): El nombre de la sección (opcional).

    Ejemplo:
    >>> increment_comments_limit(10, 'example')
    """
    st.session_state[f'limit_{element}_comments'] += (DEFAULT_COMMENTS_LIMIT
                                                      if value is None else
                                                      value)
    if st.session_state[f'limit_{element}_comments'] < DEFAULT_COMMENTS_LIMIT:
        st.session_state[f'limit_{element}_comments'] = DEFAULT_COMMENTS_LIMIT


def crear_comentario(url: str, token: str, book_id: str, content: str,
                     reply_to: str = None):
    """
    Crea un comentario en un libro.

    Args:
        url (str): URL de la API.
        token (str): Token de autenticación del usuario.
        book_id (str): ID del libro.
        content (str): Contenido del comentario.
        reply_to (str): ID del comentario al que se está respondiendo (
            opcional).

    Retorna:
        dict: Datos del comentario creado.

    Ejemplo:
    >>> crear_comentario('https://api.com', 'token123', 'book123',
        'Gran libro')
    """
    if content != '':
        params = {"book_id": book_id, "content": content}
        if reply_to is not None:
            params['responded_to'] = reply_to
        response = HttpUtils.post(f'{url}/comments/create', body=params,
                                  authorization=token)
        if response["success"]:
            if reply_to is None:
                st.session_state.main_comment = ''
                st.session_state.main_comment_success = (
                    'Se creó el comentario correctamente')
            else:
                st.session_state[f'respond_area_{reply_to}'] = ''
                st.session_state[f'{reply_to}_comment_success'] = (
                    'Se creó el comentario correctamente')
            return response["data"]
    else:
        if reply_to is None:
            st.session_state.main_comment_error = (
                'Por favor, escribe un comentario '
                'antes de enviarlo.')
        else:
            st.session_state[
                f'{reply_to}_comment_error'] = (
                'Por favor, escribe un comentario '
                'antes de enviarlo.')


def buscar_comentarios(url: str, limit: int, book_id: str,
                       reply_to: str = None):
    """
    Busca comentarios en un libro.

    Args:
        url (str): URL de la API.
        limit (int): Límite de comentarios a buscar.
        book_id (str): ID del libro.
        reply_to (str): ID del comentario al que se responde (opcional).

    Retorna:
        dict: Datos de los comentarios encontrados.

    Ejemplo:
    >>> buscar_comentarios('https://api.com', 10, 'book123', 'comment456')
    """
    params = {"book_id": book_id, "limit": limit}
    if reply_to is not None:
        params['reply_to'] = reply_to
    response = HttpUtils.get(f'{url}/comments/search', query=params)
    if response['success']:
        return response['data']


def buscar_libro_por_id(id: str, url: str):
    """
    Busca un libro por su ID en la API y devuelve los detalles del libro.

    Args:
        id (str): ID del libro a buscar.
        url (str): URL de la API.

    Retorna:
        dict: Detalles del libro.

    Ejemplo:
    >>> buscar_libro_por_id('book123', 'https://api.com')
    """
    response = HttpUtils.get(f'{url}/books/by-id', query={'id': id})
    if response["success"]:
        return response["data"]


def buscar_detalle_de_libro_por_usuario(token: str, book_id: str, url: str):
    """
    Busca los detalles de un libro por usuario y libro ID en la API.

    Args:
        token (str): Token de autenticación del usuario.
        book_id (str): ID del libro a buscar.
        url (str): URL de la API.

    Retorna:
        dict: Detalles del libro por usuario.

    Ejemplo:
    >>> buscar_detalle_de_libro_por_usuario('token123', 'book123',
    'https://api.com')
    """
    response = HttpUtils.get(f'{url}/user_book', query={"book_id": book_id},
                             headers={"Authentication": f"Bearer {token}"})
    if response["success"]:
        return response["data"]


def guardar_detalle_libro(url: str, book_id: str, token: str,
                          update_rating: bool = False):
    """
    Guarda los detalles de un libro para un usuario en la API.

    Args:
        url (str): URL de la API.
        book_id (str): ID del libro.
        token (str): Token de autenticación del usuario.
    """
    body = {"read": st.session_state.get("read"),
            "reading": st.session_state.get("reading"),
            "favorite": st.session_state.get("favorite") if
            st.session_state.get("read") > 0 else False,
            **({"rating": st.session_state.get("rating")} if
               update_rating else {})}
    HttpUtils.put(f'{url}/user_book/upsert', query={"book_id": book_id},
                  headers={"Authentication": f"Bearer {token}"},
                  body=body)
    if st.session_state.get("read") == 0:
        st.session_state.favorite = False


def book_detail_component(book_id: str, book: dict = None, url: str = None):
    """
    Componente de detalle del libro que muestra información del libro,
    opciones de marcado y comentarios.

    Args:
        book_id (str): ID del libro.
        book (dict): Detalles del libro (opcional).
        url (str): URL de la API (opcional).

    """
    if url is None:
        url = get_url()
    if book is None:
        book = buscar_libro_por_id(book_id, url)
    st.title(book['title'])
    st.image(book['image'])
    stars = "★" * round(book['rating']) + "☆" * (5 - round(book['rating']))
    data = {"Código ISBN": book['isbn_code'],
            "Titulo": book['title'],
            "Autor": book['author'],
            "Portada": book['image'],
            "Calificación": f"{stars} {round(book['rating'], 2)}",
            "Total Calificaciones": book['total_ratings'], }
    st.table(data)
    st.markdown("---")
    data = guard_session()

    if data["is_authenticated"]:
        libro_detalle = buscar_detalle_de_libro_por_usuario(data["token"],
                                                            book_id, url)

        st.session_state.read = libro_detalle['read']
        st.session_state.reading = libro_detalle['reading']
        st.session_state.favorite = libro_detalle['favorite']
        st.session_state.rating = float(libro_detalle['rating']) if (
                libro_detalle['rating'] is not None) else 0.

        columns = st.columns(3)
        with columns[0]:
            st.number_input("\\# de veces leído",
                            key="read",
                            on_change=guardar_detalle_libro,
                            min_value=0,
                            step=1,
                            args=[url, book_id, data["token"]])

        with columns[1]:
            st.checkbox("En proceso de Lectura",
                        value=st.session_state.reading,
                        key="reading",
                        on_change=guardar_detalle_libro,
                        args=[url, book_id, data["token"]])

        with columns[2]:
            st.checkbox("Favoritos",
                        value=st.session_state.favorite,
                        key="favorite",
                        on_change=guardar_detalle_libro,
                        args=[url, book_id, data["token"]],
                        disabled=st.session_state.read == 0)
        if st.session_state.read > 0:
            st.header("Calificación")
            st.caption("Seleccione una calificación:")
            # Widget de calificación con estrellas
            st.slider("Calificación", 0., 5., key="rating",
                      value=st.session_state.get("rating"),
                      on_change=guardar_detalle_libro,
                      label_visibility="hidden",
                      format="%f estrellas", step=0.5,
                      help="Haz clic para calificar el libro.",
                      args=[url, book_id, data["token"], True])
    # Comentarios
    st.header("Comentarios")
    if data["is_authenticated"]:
        st.text_area("Escribe tu comentario:",
                     key='main_comment',
                     value=st.session_state.main_comment if
                     'main_comment' in st.session_state else '')
        st.button("Enviar Comentario", on_click=crear_comentario,
                  args=[url, data['token'], book_id,
                        st.session_state.main_comment],
                  disabled='main_comment' not in st.session_state or
                           st.session_state.main_comment == '')
        if 'main_comment_error' in st.session_state:
            st.warning(st.session_state.main_comment_error)
            del st.session_state.main_comment_error
        if 'main_comment_success' in st.session_state:
            st.success(st.session_state.main_comment_success)
            del st.session_state.main_comment_success
    if "limit_main_comments" not in st.session_state:
        st.session_state.limit_main_comments = DEFAULT_COMMENTS_LIMIT
    response = buscar_comentarios(url,
                                  st.session_state.limit_main_comments,
                                  book_id)
    comentarios_raiz = response['data']
    for i, comment in enumerate(comentarios_raiz):
        with ((st.expander(f"**{comment['username']}**"))):
            comments_component(comment, data['is_authenticated'],
                               data['token'])
    menos, mas = st.columns(2)
    with menos:
        if st.session_state.limit_main_comments > DEFAULT_COMMENTS_LIMIT:
            st.button("Ver menos", on_click=increment_comments_limit,
                      use_container_width=True,
                      args=[-DEFAULT_COMMENTS_LIMIT])
    with mas:
        if response['metadata']['total_pages'] > 1:
            st.button("Ver mas", on_click=increment_comments_limit,
                      use_container_width=True)
