# Importaciones de librerías estándar de Python
from typing import Callable

# Importaciones de librerías de terceros
import streamlit as st


# Función para reiniciar los parámetros de paginación
def restart_pagination_params(key: str):
    """
    Función para reiniciar los parámetros de paginación en la sesión de
    Streamlit.
    """
    st.session_state[f"{key}-page"] = 1


def list_users_component(callback_to_get_data: Callable[[int, str], dict],
                         key: str = ""):
    """
    Componente de Streamlit que muestra un listado de usuarios con
    paginación y búsqueda.

    Args:
        callback_to_get_data (Callable): Función de retorno de llamada para
        obtener los datos de los usuarios.

    Ejemplo:
    ```python
    list_users_component(lambda page, busqueda: search_users(url, page,
    LIMIT, busqueda))
    ```

    """
    # Inicializar el estado de la sesión para el paginado
    if f"{key}-page" not in st.session_state:
        # Si 'page' no está definido en el estado de sesión,
        # inicialízalo con 1.
        st.session_state[f"{key}-page"] = 1

    st.title("Listado de Usuarios")

    # Cuadro de búsqueda para buscar usuarios por nombre, usuario o correo.
    busqueda = st.text_input("Buscar usuario",
                             on_change=restart_pagination_params,
                             key=f"{key}-BuscarUsuarios",
                             help="Busca por nombre, usuario o correo",
                             args=[f"{key}-page"])
    # Llamar a la función de retorno de llamada para obtener datos de usuarios.
    response = callback_to_get_data(st.session_state.get(f"{key}-page"),
                                    busqueda)
    usuarios = response["data"]
    metadata = response["metadata"]

    # Mostrar la lista de usuarios en columnas
    columns = st.columns(3)
    for i, usuario in enumerate(usuarios):
        if i != 0 and i % 3 == 0:
            # Agrega un separador horizontal (línea) después de cada fila de
            # 3 usuarios.
            st.markdown("---")
            # Crea un nuevo contenedor de 5 columnas para los usuarios para
            # mantener una estructura uniforme
            columns = st.columns(3)

        with columns[i % 3]:
            # Muestra la imagen del usuario
            st.image("https://cdn-icons-png.flaticon.com/512/1974/1974050.png",
                     use_column_width=True)
            st.write(f"**Nombre:** {usuario['name']}")
            st.write(f"**Usuario:** {usuario['user']}")
            # Botón para ver el perfil del usuario
            user_id = usuario["_id"]
            st.button(
                f" Ver perfil de {usuario['user']}",
                on_click=lambda x: st.experimental_set_query_params(user_id=x),
                key=f"{key}-{user_id}",
                args=[user_id]
            )

    # Paginación
    if metadata['total_pages'] > 1:
        # Muestra información de paginación que indica la página actual y el
        # total de páginas.
        st.write(
            f"Mostrando página {st.session_state.page} de "
            f"{int(metadata['total_pages'])}"
        )
        # Proporciona un campo numérico para que los usuarios ingresen el
        # número de página.
        st.number_input("page", key=f"{key}-page", label_visibility='hidden',
                        step=1, min_value=1,
                        max_value=int(metadata['total_pages']))
    st.markdown("---")

    # Mensaje si no hay resultados
    if not usuarios or len(usuarios) < 1:
        # Si no se encontraron usuarios que coincidan con la búsqueda,
        # muestra un mensaje informativo.
        st.info("No se encontraron resultados para la búsqueda.")
