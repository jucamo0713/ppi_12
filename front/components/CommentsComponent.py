from datetime import datetime
import streamlit as st

from utils.GetUrl import get_url
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


def comments_component(comment: dict,
                       is_authenticated: bool,
                       token: str = None,
                       default_comments_limit: int = DEFAULT_COMMENTS_LIMIT,
                       show_author: bool = False,
                       ):
    url = get_url()
    book_id = comment["book_id"]
    fecha = datetime.fromisoformat(comment['created_date']).strftime(
        '%Y-%m-%d %H:%M')
    user_id = comment['user_id']
    comment_id = comment['_id']
    if show_author:
        st.header(f"Autor: {comment['author']}")
    st.button(
        "Ver Perfil",
        key=f'Ver Perfil${comment_id}',
        on_click=(lambda x: st.experimental_set_query_params(
            **st.experimental_get_query_params(),
            user_id=x)),
        args=[user_id]
    )
    st.write(f"{fecha}: {comment['content']}")
    if comment['has_responses']:
        if f'limit_{comment_id}_comments' not in st.session_state:
            st.session_state[
                f'limit_{comment_id}_comments'] = (
                default_comments_limit)
        sub_response = buscar_comentarios(
            url,
            limit=st.session_state[f'limit_{comment_id}_comments'],
            reply_to=comment_id,
            book_id=book_id
        )
        comment_responses = sub_response['data'][::-1]
        for res in comment_responses:
            fecha_res = datetime.fromisoformat(
                res['created_date']
            ).strftime('%Y-%m-%d %H:%M')
            st.markdown(f"- **{res['username']}** - *{fecha_res}*:"
                        f" {res['content']}")
            st.button(
                "Ver Perfil",
                key=f'Ver Perfil${res["_id"]}',
                on_click=(
                    lambda x: st.experimental_set_query_params(
                        **st.experimental_get_query_params(),
                        user_id=x
                    )
                ),
                args=[res["user_id"]]
            )
        menos, mas = st.columns(2)
        with menos:
            if (st.session_state[f'limit_{comment_id}_comments']
                    > default_comments_limit):
                st.button("Ver menos",
                          on_click=increment_comments_limit,
                          use_container_width=True,
                          args=[-default_comments_limit, comment_id])
        with mas:
            if sub_response['metadata']['total_pages'] > 1:
                st.button("Ver mas",
                          on_click=increment_comments_limit,
                          use_container_width=True,
                          args=[default_comments_limit, comment[
                              "_id"]]
                          )
        # Agregar botón de respuesta para cada comentario raíz
    if is_authenticated:
        if f'respond_area_{comment_id}' not in st.session_state:
            st.session_state[f'respond_area_{comment_id}'] = ''
        st.text_area(f"Responder a {comment['username']}",
                     key=f'respond_area_{comment_id}',
                     value=st.session_state[f'respond_area_'
                                            f'{comment_id}'])
        st.button(
            "Responder",
            key=f'comment_button_{comment_id}',
            on_click=crear_comentario,
            disabled=(f'respond_area_{comment_id}' not in
                      st.session_state or
                      st.session_state[
                          f'respond_area_{comment_id}'] == ''),
            args=[
                url,
                token,
                book_id,
                st.session_state[f'respond_area_{comment_id}'],
                comment_id
            ])
        if f'{comment_id}_comment_error' in st.session_state:
            st.warning(st.session_state[
                           f'{comment_id}_comment_error'])
            del st.session_state[
                f'{comment_id}_comment_error']
        if f'{comment_id}_comment_success' in st.session_state:
            st.success(st.session_state[
                           f'{comment_id}_comment_success'])
            del st.session_state[
                f'{comment_id}_comment_success']
