# Importaciones de librerías de terceros
import streamlit as st

from components.BookCard import book_card
from components.BookDetailComponent import book_detail_component
# Importaciones de módulos internos de la aplicación
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url
from utils.GuardSession import guard_session
from utils.HttpUtils import HttpUtils


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


def get_recommended_books(url: str, token: str):
    response = HttpUtils.get(f'{url}/user_book/recomendate-users',
                             authorization=f"Bearer {token}")
    if response["success"]:
        return response["data"]
    else:
        return {"based_on_books_read": []}


# Configura la aplicación básica
value = basic_config()

url = get_url()
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
            recomendate = get_recommended_books(url, st.session_state.get(
                'token'))
            st.title("Usuarios recomendados")
            st.header("Basado en lo que has leído")
            columns = st.columns(5)
            if len(recomendate["based_on_books_read"]) > 0:
                for i, usuario in enumerate(
                        recomendate["based_on_books_read"]):
                    with columns[i % 5]:
                        # Muestra la imagen del usuario
                        st.image(
                            "https://cdn-icons-png.flaticon.com/512/1974/"
                            "1974050.png",
                            use_column_width=True)
                        st.write(f"**Nombre:** {usuario['name']}")
                        st.write(f"**Usuario:** {usuario['user']}")
                        # Botón para ver el perfil del usuario
                        st.button(
                            f" Ver perfil de {usuario['user']}",
                            on_click=(
                                lambda x:
                                st.experimental_set_query_params(
                                    user_id=x
                                )),
                            args=[usuario["_id"]]
                        )
            else:
                st.write("Aún no te conocemos lo suficiente ♥")
