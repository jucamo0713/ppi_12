from typing import Callable

import streamlit as st


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    st.session_state.page = 1


def list_users_component(callback_to_get_data: Callable[[int, str], dict]):
    # Inicializar el estado de la sesión para el paginado
    if 'page' not in st.session_state:
        # Si 'page' no está definido en el estado de sesión,
        # inicialízalo con 1.
        st.session_state.page = 1

    st.title("Listado de Usuarios")
    busqueda = st.text_input("Buscar usuario",
                             on_change=restart_pagination_params,
                             help="Buca por nombre, usuario o correo")
    response = callback_to_get_data(st.session_state.page, busqueda)
    usuarios = response["data"]
    metadata = response["metadata"]
    # Mostrar la lista de usuarios
    columns = st.columns(3)
    for i, usuario in enumerate(usuarios):

        if i != 0 and i % 3 == 0:
            # Agrega un separador horizontal (línea) después de cada
            # fila de 3 usuarios.
            st.markdown("---")
            # Crea un nuevo contenedor de 5 columnas para los libros
            # para mantener una estructura uniforme
            columns = st.columns(3)
        with columns[i % 3]:
            st.write(f"**Nombre:** {usuario['name']}")
            st.write(f"**Usuario:** {usuario['user']}")
            st.button(f" Ver perfil de {usuario['user']}",
                      on_click=lambda x: st.experimental_set_query_params(
                          user_id=x),
                      args=[usuario["_id"]])

    # Paginación
    if metadata['total_pages'] > 1:
        # Muestra información de paginación que indica la página actual
        # y el total de páginas.
        st.write(
            f"Mostrando página {st.session_state.page} de "
            f"{int(metadata['total_pages'])}")
        # Proporciona un campo numérico para que los usuarios ingresen
        # el número de página.
        st.number_input("page", key="page", label_visibility='hidden',
                        step=1, min_value=1,
                        max_value=int(metadata['total_pages']))

    st.markdown("---")

    # Mensaje si no hay resultados
    if not usuarios or len(usuarios) < 1:
        # Si no se encontraron libros que coincidan con la búsqueda,
        # muestra un mensaje informativo.
        st.info("No se encontraron resultados para la búsqueda.")
