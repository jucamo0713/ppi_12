# Importaciones de librerías de terceros
import streamlit as st

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
    """
    Obtiene libros recomendados a través de una solicitud HTTP.

    Args:
        url (str): URL del servicio para obtener libros recomendados.
        token (str): Token de autenticación para la solicitud HTTP.

    Returns:
        dict: Diccionario que contiene la lista de libros recomendados.
    """
    # Realizar una solicitud HTTP GET para obtener libros recomendados
    response = HttpUtils.get(f'{url}/user_book/recomendate-users',
                             authorization=f"Bearer {token}")

    # Verificar si la solicitud fue exitosa
    if response["success"]:
        return response["data"]
    else:
        # En caso de error, devolver una estructura vacía
        return {"based_on_books_read": []}


# Configura la aplicación básica
value = basic_config()

url = get_url()
if value:
    # Verifica el estado de la sesión
    data = guard_session(allow_only_signed=True)

    if data["is_authenticated"]:
        # Comprobar si hay un parámetro "user_id" en la URL
        if "user_id" in st.experimental_get_query_params():
            # Botón para volver atrás
            st.button('Volver', key='volver', on_click=volver,
                      args=["user_id"])
            # Mostrar el componente de perfil para el usuario específico
            profile_component(
                st.experimental_get_query_params()["user_id"][0])
            # Botón adicional para volver atrás
            st.button('Volver', key='volver2', on_click=volver,
                      args=["user_id"])
        # Comprobar si hay un parámetro "book_id" en la URL
        elif "book_id" in st.experimental_get_query_params():
            # Botón para volver atrás
            st.button('Volver', key='volver', on_click=volver,
                      args=["book_id"])
            # Mostrar el detalle del libro para el libro específico
            book_detail_component(
                st.experimental_get_query_params()["book_id"][0])
            # Botón adicional para volver atrás
            st.button('Volver', key='volver2', on_click=volver,
                      args=["book_id"])
        else:
            # Obtener libros recomendados basados en lo que has leído
            recomendate = get_recommended_books(url,
                                                st.session_state.get('token'))
            # Título y encabezado para la sección de usuarios recomendados
            st.title("Usuarios recomendados")
            st.header("Basado en lo que has leído")
            # Crear columnas para mostrar los usuarios recomendados
            columns = st.columns(5)

            # Verificar si hay usuarios recomendados
            if len(recomendate["based_on_books_read"]) > 0:
                # Iterar sobre los usuarios recomendados y mostrar información
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
                                lambda x: st.experimental_set_query_params(
                                    user_id=x
                                )),
                            args=[usuario["_id"]]
                        )
            else:
                # Mensaje si no hay usuarios recomendados
                st.write("Aún no te conocemos lo suficiente ♥")
