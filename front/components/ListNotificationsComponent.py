import streamlit as st

from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils

LIMIT = 15


def search_notifications(url: str, limit: int, page: int, authorization: str):
    response = HttpUtils.get(f"{url}/notifications/all",
                             query={
                                 "limit": limit,
                                 "page": page
                             },
                             authorization=authorization)
    if response["success"]:
        return response["data"]
    else:
        return {
            "data": [],
            "metadata": {

            }
        }


def delete_notification(url: str, id: str, authorization: str):
    response = HttpUtils.delete(f"{url}/notifications/delete",
                                authorization=authorization,
                                query={"id": id})
    if response['success']:
        return True
    else:
        return False


def resolve_button(notification: dict):
    if notification['type'] in ["NEW_FOLLOWER",
                                "NEW_FOLLOW_OF_FOLLOWER",
                                "FOLLOWER_UNFOLLOW"]:
        st.button("Ver Usuario",
                  on_click=(lambda x: st.experimental_set_query_params(
                      **st.experimental_get_query_params(),
                      user_id=x)),
                  args=[
                      notification["data_id"]
                  ])


def list_notification_component(key: str = "notifications"):
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
                st.button("Borrar",
                          on_click=delete_notification,
                          args=[url, notification["_id"],
                                st.session_state.token])
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
        st.number_input("page", key=f"{key}-page", label_visibility='hidden',
                        step=1, min_value=1,
                        max_value=int(metadata['total_pages']))
    st.markdown("---")

    # Mensaje si no hay resultados
    if not notifications or len(notifications) < 1:
        # Si no se encontraron usuarios que coincidan con la búsqueda,
        # muestra un mensaje informativo.
        st.info("No se encuentran notificaciones.")
