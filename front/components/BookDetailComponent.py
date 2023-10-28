import streamlit as st
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils


def buscar_libro_por_id(id: str, url: str):
    response = HttpUtils.get(f'{url}/books/by-id', query={'id': id})
    if response["success"]:
        return response["data"]


def buscar_detalle_de_libro_por_usuario(token: str, book_id: str, url: str):
    response = HttpUtils.get(f'{url}/user_book',
                             query={
                                 "book_id": book_id
                             },
                             headers={
                                 "Authentication": f"Bearer {token}"
                             })
    if response["success"]:
        return response["data"]


def guardar_detalle_libro(url: str,
                          book_id: str,
                          token: str,
                          read: bool,
                          in_process: bool,
                          favorites: bool, ):
    HttpUtils.put(f'{url}/user_book/upsert',
                  query={
                      "book_id": book_id
                  },
                  headers={
                      "Authentication": f"Bearer {token}"
                  },
                  body={
                      "read": read,
                      "reading": in_process,
                      "favorite": favorites,
                  })


def book_detail_component(book_id: str, book: dict = None, url: str = None):
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
    # Verificar si el usuario está autenticado
    if data["is_authenticated"]:
        libro_detalle = buscar_detalle_de_libro_por_usuario(data["token"], book_id, url)
        if "read" not in st.session_state:
            st.session_state.read = libro_detalle['read']
        if "reading" not in st.session_state:
            st.session_state.reading = libro_detalle['reading']
        if "favorite" not in st.session_state:
            st.session_state.favorite = libro_detalle['favorite']

        columns = st.columns(3)
        # Mostrar opciones para marcar el libro
        with columns[0]:
            st.checkbox("Leído",
                        value=st.session_state.read,
                        key="read",
                        on_change=guardar_detalle_libro,
                        args=[
                            url,
                            book_id,
                            data["token"],
                            not st.session_state.read,
                            st.session_state.reading,
                            st.session_state.favorite,
                        ])

        with columns[1]:
            st.checkbox(
                "En proceso de Lectura",
                value=st.session_state.reading,
                key="reading",
                on_change=guardar_detalle_libro,
                args=[
                    url,
                    book_id,
                    data["token"],
                    st.session_state.read,
                    not st.session_state.reading,
                    st.session_state.favorite,
                ]
            )

        with columns[2]:
            st.checkbox("Favoritos",
                        value=st.session_state.favorite,
                        key="favorite",
                        on_change=guardar_detalle_libro,
                        args=[
                            url,
                            book_id,
                            data["token"],
                            st.session_state.read,
                            st.session_state.reading,
                            not st.session_state.favorite,
                        ])
