# Importaciones de librerías necesarias
import streamlit as st
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils

LIMIT = 15


def search_notifications(url: str, limit: int, page: int,
                         authorization: str) -> dict:
    """
    Busca notificaciones en la URL proporcionada.

    Parameters:
    - url (str): La URL base para la búsqueda de notificaciones.
    - limit (int): El límite de notificaciones a recuperar.
    - page (int): El número de página de notificaciones.
    - authorization (str): Token de autorización para la solicitud.

    Returns:
    - dict: Un diccionario que contiene datos y metadatos de las
    notificaciones.
    """
    response = HttpUtils.get(
        f"{url}/notifications/all",
        query={"limit": limit, "page": page},
        authorization=authorization
    )
    if response["success"]:
        return response["data"]
    else:
        return {"data": [], "metadata": {}}


def delete_notification(url: str, id: str, authorization: str) -> bool:
    """
    Elimina una notificación específica por su ID.

    Parameters:
    - url (str): La URL base para la eliminación de notificaciones.
    - id (str): ID de la notificación a eliminar.
    - authorization (str): Token de autorización para la solicitud.

    Returns:
    - bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    response = HttpUtils.delete(f"{url}/notifications/delete",
                                authorization=authorization,
                                query={"id": id})
    return response['success']


def resolve_button(notification: dict) -> None:
    """
    Crea un botón para resolver una acción específica de notificación.

    Parameters:
    - notification (dict): La notificación para la cual se crea el botón.
    """
    if notification['type'] in [
        "NEW_FOLLOWER", "NEW_FOLLOW_OF_FOLLOWER", "FOLLOWER_UNFOLLOW"
    ]:
        st.button(
            "Ver Usuario",
            on_click=(
                lambda x: st.experimental_set_query_params(
                    **st.experimental_get_query_params(),
                    user_id=x
                )
            ),
            args=[notification["data_id"]],
            key=f"Show_user{notification['_id']}"
        )


def list_notification_component(key: str = "notifications") -> None:
    """
    Muestra una interfaz de usuario para listar y gestionar notificaciones.

    Parameters:
    - key (str): La clave para identificar el componente de notificaciones.
    """
    st.header("Notificaciones")
    url = get_url()
    data = search_notifications(url, LIMIT, 1, st.session_state.token)
    notifications = data['data']
    metadata = data["metadata"]
    for notification in notifications:
        with st.expander(notification["message"]):
            cols = st.columns(2)
            with cols[0]:
                resolve_button(notification)
            with cols[1]:
                st.button(
                    "Borrar", key=f"Borrar-{notification['_id']}",
                    on_click=delete_notification,
                    args=[url, notification["_id"], st.session_state.token]
                )
    # Paginación
    if 'total_pages' in metadata and metadata['total_pages'] > 1:
        # Muestra información de paginación que indica la página actual y el
        # total de páginas.
        st.write(
            f"Mostrando página {st.session_state[f'{key}-page']} de "
            f"{int(metadata['total_pages'])}"
        )
        # Proporciona un campo numérico para que los usuarios ingresen el
        # número de página.
        st.number_input(
            "page", key=f"{key}-page", label_visibility='hidden',
            step=1, min_value=1, max_value=int(metadata['total_pages'])
        )
    st.markdown("---")

    # Mensaje si no hay resultados
    if not notifications or len(notifications) < 1:
        # Si no se encontraron Notificaciones que coincidan con la búsqueda,
        # muestra un mensaje informativo.
        st.info("No se encuentran notificaciones.")
