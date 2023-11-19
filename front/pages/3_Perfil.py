# Importaciones de librerías de terceros
import streamlit as st

from components.BookDetailComponent import book_detail_component
# Importaciones de módulos internos de la aplicación
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GuardSession import guard_session


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
            # Muestra el componente del perfil del usuario
            profile_component()
