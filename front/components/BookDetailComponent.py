# Importaciones de librerías de terceros
from datetime import datetime

import streamlit as st

# Importaciones de módulos internos de la aplicación
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils

DEFAULT_COMMENTS_LIMIT = 5


def increment_comments_limit(value: int = None, element='main'):
    st.session_state[f'limit_{element}_comments'] += (DEFAULT_COMMENTS_LIMIT
                                                      if value is None
                                                      else value)
    if st.session_state[f'limit_{element}_comments'] < DEFAULT_COMMENTS_LIMIT:
        st.session_state[f'limit_{element}_comments'] = DEFAULT_COMMENTS_LIMIT


def crear_comentario(url: str,
                     token: str,
                     book_id: str,
                     content: str,
                     reply_to: str = None):
    # TODO: documentar
    if content != '':
        params = {"book_id": book_id,
                  "content": content}
        if reply_to is not None:
            params['responded_to'] = reply_to
        response = HttpUtils.post(f'{url}/comments/create', body=params,
                                  authorization=token)
        if response["success"]:
            if reply_to is None:
                st.session_state.main_comment = ''
                st.session_state. \
                    main_comment_success = ('Se creó el comentario '
                                            'correctamente')
            else:
                st.session_state[f'respond_area_{reply_to}'] = ''
                st.session_state[
                    f'{reply_to}_comment_success'] = ('Se creó el comentario '
                                                      'correctamente')
            return response["data"]

    else:
        if reply_to is None:
            st.session_state. \
                main_comment_error = ('Por favor, '
                                      'escribe un comentario '
                                      'antes de enviarlo.')
        else:
            st.session_state[
                f'{reply_to}_comment_error'] = ('Por favor, '
                                                'escribe un comentario '
                                                'antes de enviarlo.')


def buscar_comentarios(url: str,
                       limit: int,
                       book_id: str,
                       reply_to: str = None):
    # TODO: documentar
    params = {"book_id": book_id,
              "limit": limit}
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

    Returns:
        dict: Detalles del libro.
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

    Returns:
        dict: Detalles del libro por usuario.
    """
    response = HttpUtils.get(f'{url}/user_book',
                             query={"book_id": book_id},
                             headers={"Authentication": f"Bearer {token}"})
    if response["success"]:
        return response["data"]


def guardar_detalle_libro(url: str, book_id: str, token: str, read: bool,
                          in_process: bool, favorites: bool):
    """
    Guarda los detalles de un libro para un usuario en la API.

    Args:
        url (str): URL de la API.
        book_id (str): ID del libro.
        token (str): Token de autenticación del usuario.
        read (bool): Indica si el libro ha sido leído.
        in_process (bool): Indica si el libro está en proceso de lectura.
        favorites (bool): Indica si el libro está marcado como favorito.
    """
    HttpUtils.put(f'{url}/user_book/upsert',
                  query={"book_id": book_id},
                  headers={"Authentication": f"Bearer {token}"},
                  body={
                      "read": read,
                      "reading": in_process,
                      "favorite": favorites,
                  })


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
    data = {"Código ISBN": book['isbn_code'],
            "Titulo": book['title'],
            "Autor": book['author'],
            "Portada": book['image']}
    st.table(data)
    st.markdown("---")
    data = guard_session()

    if data["is_authenticated"]:
        libro_detalle = buscar_detalle_de_libro_por_usuario(data["token"],
                                                            book_id, url)
        if "read" not in st.session_state:
            st.session_state.read = libro_detalle['read']
        if "reading" not in st.session_state:
            st.session_state.reading = libro_detalle['reading']
        if "favorite" not in st.session_state:
            st.session_state.favorite = libro_detalle['favorite']

        columns = st.columns(3)
        with columns[0]:
            st.checkbox("Leído",
                        value=st.session_state.read,
                        key="read",
                        on_change=guardar_detalle_libro,
                        args=[url, book_id, data["token"],
                              not st.session_state.read,
                              st.session_state.reading,
                              st.session_state.favorite])

        with columns[1]:
            st.checkbox("En proceso de Lectura",
                        value=st.session_state.reading,
                        key="reading",
                        on_change=guardar_detalle_libro,
                        args=[url, book_id, data["token"],
                              st.session_state.read,
                              not st.session_state.reading,
                              st.session_state.favorite])

        with columns[2]:
            st.checkbox("Favoritos",
                        value=st.session_state.favorite,
                        key="favorite",
                        on_change=guardar_detalle_libro,
                        args=[url, book_id, data["token"],
                              st.session_state.read,
                              st.session_state.reading,
                              not st.session_state.favorite])

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
        fecha = datetime.fromisoformat(comment['created_date']).strftime(
            '%Y-%m-%d %H:%M')
        with ((st.expander(f"**{comment['username']}** - *{fecha}*"))):
            st.write(comment['content'])
            if comment['has_responses']:
                if f'limit_{comment["_id"]}_comments' not in st.session_state:
                    st.session_state[
                        f'limit_{comment["_id"]}_comments'] = (
                        DEFAULT_COMMENTS_LIMIT)
                sub_response = buscar_comentarios(
                    url,
                    limit=st.session_state[f'limit_'
                                           f'{comment["_id"]}_comments'],
                    reply_to=comment["_id"], book_id=book_id)
                comment_responses = sub_response['data']
                for res in comment_responses:
                    fecha_res = datetime.fromisoformat(
                        res['created_date']).strftime(
                        '%Y-%m-%d %H:%M')
                    st.markdown(f"- **{res['username']}** - *{fecha_res}*:"
                                f" {res['content']}")
                menos, mas = st.columns(2)
                with menos:
                    if (st.session_state[f'limit_{comment["_id"]}_comments']
                            > DEFAULT_COMMENTS_LIMIT):
                        st.button("Ver menos",
                                  on_click=increment_comments_limit,
                                  use_container_width=True,
                                  args=[-DEFAULT_COMMENTS_LIMIT, comment[
                                      "_id"]])
                with mas:
                    if sub_response['metadata']['total_pages'] > 1:
                        st.button("Ver mas",
                                  on_click=increment_comments_limit,
                                  use_container_width=True,
                                  args=[DEFAULT_COMMENTS_LIMIT, comment[
                                      "_id"]]
                                  )
                # Agregar botón de respuesta para cada comentario raíz
            if data["is_authenticated"]:
                if f'respond_area_{comment["_id"]}' not in st.session_state:
                    st.session_state[f'respond_area_{comment["_id"]}'] = ''
                st.text_area(f"Responder a {comment['username']}",
                             key=f'respond_area_{comment["_id"]}',
                             value=st.session_state[f'respond_area_'
                                                    f'{comment["_id"]}'])
                st.button(
                    "Responder",
                    key = f'comment_button_{comment["_id"]}',
                    on_click=crear_comentario,
                    disabled=(f'respond_area_{comment["_id"]}' not in
                              st.session_state or
                              st.session_state[
                                  f'respond_area_{comment["_id"]}'] == ''),
                    args=[
                        url,
                        data['token'],
                        book_id,
                        st.session_state[f'respond_area_{comment["_id"]}'],
                        comment["_id"]
                    ])
                if f'{comment["_id"]}_comment_error' in st.session_state:
                    st.warning(st.session_state[
                                   f'{comment["_id"]}_comment_error'])
                    del st.session_state[
                        f'{comment["_id"]}_comment_error']
                if f'{comment["_id"]}_comment_success' in st.session_state:
                    st.success(st.session_state[
                                   f'{comment["_id"]}_comment_success'])
                    del st.session_state[
                        f'{comment["_id"]}_comment_success']
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
