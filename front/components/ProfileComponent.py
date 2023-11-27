# Importaciones de librerías estándar de Python
from datetime import datetime
import textwrap

# Importaciones de librerías de terceros
import matplotlib.pyplot as plt
import streamlit as st

# Importaciones de módulos internos de la aplicación
from components.ListBooksComponent import list_books_component
from components.ListNotificationsComponent import search_notifications
from utils.GetUrl import get_url
from utils.HttpUtils import HttpUtils

# Establece el rango mínimo para permitir años anteriores a 2013
MIN_FECHA_NACIMIENTO = datetime(1900, 1, 1)


def close_session():
    """
    Cierra la sesión del usuario, eliminando el token de sesión y los datos
    del usuario, y marca la sesión como cerrada.
    """
    # Borra el token de sesión y los datos del usuario
    del st.session_state.token
    del st.session_state.user
    # Marca la sesión como cerrada
    st.session_state.closed_session = True


def search_user_books(url: str, type_list: str, limit: int, page: int,
                      user_token: str, user_id: str = None, search_param: str =
                      ""):
    """
    Busca los libros del usuario según el tipo especificado.

    Args:
        url (str): URL de la API.
        type_list (str): Tipo de lista de libros a buscar (ej. "read",
        "reading", "favorite").
        limit (int): Límite de libros a recuperar.
        page (int): Número de página.
        user_token (str): Token de autenticación del usuario.
        search_param (str): Parámetro de búsqueda (opcional).

    Retorna:
        list: Lista de libros del usuario.

    Ejemplo:
    >>> search_user_books('https://api.com', 'read', 5, 1, 'token123',
    'Python')
    """
    response = HttpUtils.get(f'{url}/user_book/list/{type_list}',
                             query={"limit": limit, "page": page,
                                    "search_param": search_param,
                                    "user_id": user_id},
                             authorization=user_token)
    if response['success']:
        return response['data']
    else:
        return []


def search_statistics(url: str, user_id: str = None, user_token: str = None):
    """
    Obtiene las estadísticas de lectura de un usuario.

    Args:
        url (str): URL de la API.
        user_id (str): ID del usuario para el cual se solicitan las
        estadísticas.
        user_token (str): Token de autenticación del usuario.

    Returns:
        dict or None: Un diccionario con las estadísticas de lectura si la
        solicitud es exitosa, None si hay un error.

    Ejemplo:
    >>> search_statistics('https://api.com', 'user123', 'token123')
    """
    response = HttpUtils.get(f'{url}/user_book/statistics',
                             query={"user_id": user_id},
                             authorization=user_token)
    if response['success']:
        return response['data']
    else:
        return None


def search_user_data(url: str, user_id: str):
    """
    Obtiene los datos de un usuario por su ID.

    Args:
        url (str): URL de la API.
        user_id (str): ID del usuario.

    Returns:
        dict or None: Un diccionario con los datos del usuario si la
        solicitud es exitosa, None si hay un error.

    Ejemplo:
    >>> search_user_data('https://api.com', 'user123')
    """
    response = HttpUtils.get(f'{url}/user/by-id',
                             query={"id": user_id})
    if response['success']:
        return response['data']
    else:
        return None


def update_password(url: str,
                    user_token: str,
                    new_password: str,
                    old_password: str):
    response = HttpUtils.put(f'{url}/user/update-password/',
                             body={
                                 "current_password": old_password,
                                 "new_password": new_password
                             },
                             authorization=user_token)
    if response["success"]:
        st.session_state["updated_password"] = True
    else:
        st.session_state["updated_password"] = False


def update_user_data(url: str, user_token: str, new_data: dict):
    """
    Actualiza los datos del usuario.

    Args:
        url (str): URL de la API.
        user_token (str): Token de autenticación del usuario.
        new_data (dict): Nuevo conjunto de datos del usuario a actualizar.

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario.
    """
    response = HttpUtils.put(f'{url}/user/update/',
                             body=new_data,
                             authorization=user_token)
    if response["success"]:
        st.session_state.user = response["data"]["user"]
        st.session_state.token = response["data"]["token"]
        st.session_state["updated_data"] = True

    else:
        st.session_state["updated_data"] = False


def follow_user(url, token, user_to_follow_id: str):
    """
    Realiza una solicitud para seguir a otro usuario.

    Args:
        url (str): URL de la API.
        token (str): Token de autenticación del usuario que realiza la acción.
        user_to_follow_id (str): ID del usuario al que se desea seguir.
    """
    HttpUtils.post(f"{url}/follow", authorization=token,
                   query={"follow_id": user_to_follow_id})


def unfollow_user(url, token, user_to_unfollow_id: str):
    """
    Realiza una solicitud para dejar de seguir a otro usuario.

    Args:
        url (str): URL de la API.
        token (str): Token de autenticación del usuario que realiza la acción.
        user_to_unfollow_id (str): ID del usuario al que se desea dejar de
        seguir.
    """
    HttpUtils.put(f"{url}/unfollow", authorization=token, query={
        "follow_id": user_to_unfollow_id})


def validate_follow_user(url, token, user_to_follow_id: str):
    """
    Realiza una solicitud para dejar de seguir a otro usuario.

    Args:
        url (str): URL de la API.
        token (str): Token de autenticación del usuario que realiza la acción.
        user_to_follow_id (str): ID del usuario al que se desea validar si
        ya se sigue
    """
    response = HttpUtils.get(f"{url}/follow/validate-following",
                             authorization=token,
                             query={"follow_id": user_to_follow_id})

    return response["data"]


def profile_component(user_id: str = None):
    """
    Muestra el componente de perfil de usuario si el usuario está autenticado.

    Retorna:
        bool: True si el usuario está autenticado y se muestra el perfil,
        False en caso contrario.

    Ejemplo:
    >>> profile_component()
    """
    url = get_url()
    my_profile = not (user_id is not None and ("user" not in st.session_state
                                               or user_id !=
                                               st.session_state.user["id"]))

    # Verifica si el perfil es propio o de otro usuario
    if not my_profile:
        # Si no es el perfil propio, obtén los datos del usuario mediante la
        # función search_user_data
        usuario = search_user_data(url, user_id)

        # Muestra un mensaje de bienvenida y los detalles del usuario
        user = usuario["user"]
        st.title(f"Bienvenido!")
        st.title(f"Soy {user}!")
        data = {
            "Usuario": user,
            "Fecha de registro": usuario["registered_date"]
        }
        st.table(data)
        if ("token" in st.session_state):
            validated = validate_follow_user(url, st.session_state.token,
                                             user_id)
            if not validated:
                if st.button("Seguir a este usuario", on_click=follow_user,
                             args=[url, st.session_state.token, user_id]):
                    st.success(f"Ahora sigues a {usuario['user']}")
            else:
                if st.button("Dejar de Seguir", on_click=unfollow_user,
                             args=[url, st.session_state.token, user_id]):
                    st.success(f"Has dejado de seguir a este usuario.")
    else:
        # Si es el perfil propio, obtén los datos del usuario de la sesión
        usuario = st.session_state.user
        name = usuario["name"]
        user_id = usuario["id"]

        # Muestra un mensaje de bienvenida y los detalles del usuario
        st.title(f"Bienvenido, {name}!")
        data = search_notifications(url, 15, 1, st.session_state.token)
        notifications = data['data']
        if len(notifications) >= 1:
            st.info("Tienes nuevas notificaciones, dirigete a la pestaña "
                    "Notificaciones si deseas verlas.")
        data = {
            "Nombre": name,
            "Usuario": usuario["user"],
            "Correo": usuario["email"],
            "Fecha de nacimiento": usuario["burn_date"],
            "Fecha de registro": usuario["registered_date"]
        }
        st.table(data)

        # Expande la sección para actualizar datos del usuario
        with (st.expander("Actualizar datos")):
            # Crear campos de entrada para la modificación de datos
            new_user = st.text_input("Nuevo user:", usuario["user"])
            new_name = st.text_input("Nuevo nombre:", usuario["name"])
            new_email = st.text_input("Nuevo correo:", usuario["email"])

            # Establece el rango máximo para no permitir menores de 13 años
            current_date = datetime.now()
            max_fecha_nacimiento = datetime(current_date.year - 13,
                                            current_date.month,
                                            current_date.day)
            new_burn_date = st.date_input("Fecha de Nacimiento",
                                          min_value=MIN_FECHA_NACIMIENTO,
                                          max_value=max_fecha_nacimiento,
                                          value=datetime.fromisoformat(
                                              usuario["burn_date"]))
            burn = datetime(new_burn_date.year,
                            new_burn_date.month,
                            new_burn_date.day).isoformat() + "Z"

            # Verifica si se han realizado cambios y muestra el botón para
            # guardar
            if new_name != "" and new_email != "" and new_user != "" and (
                    new_email != usuario["email"] or new_name != name or
                    new_user != usuario["user"] or burn != usuario[
                        "burn_date"]):
                # Botón para guardar cambios
                data = {
                    "name": new_name if new_name != name else None,
                    "email": new_email if new_email != usuario[
                        "email"] else None,
                    "burn_date": burn if burn != usuario[
                        "burn_date"] else None,
                    "user": new_user if new_user != usuario["user"] else None
                }
                if st.button("Guardar Cambios", on_click=update_user_data,
                             args=[url, st.session_state.token, data]):

                    # Verifica si los datos se han actualizado con éxito
                    if st.session_state["updated_data"]:
                        st.session_state["updated_data"] = False
                        st.success("¡Datos actualizados con éxito!")
        with (st.expander("Cambiar Contraseña")):
            password = st.text_input("Ingrese su contraseña actual",
                                     type="password", )
            new_password = st.text_input("Ingrese la nueva contraseña",
                                         type="password", )
            confirmate_new_password = st.text_input(
                "Confirme la nueva contraseña",
                type="password", )
            if new_password != "" and new_password != confirmate_new_password:
                st.error("Las contraseñas no coinciden")
            st.button(
                "Cambiar contraseña",
                disabled=not (password != "" and
                              new_password != "" and
                              confirmate_new_password != "" and
                              new_password == confirmate_new_password
                              ),
                on_click=update_password,
                args=(
                    url,
                    st.session_state.token,
                    new_password, password)
            )
            if (("updated_password" in st.session_state) and
                    st.session_state.get("updated_password")):
                st.success("Contraseña actualizada con éxito")
        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)
    st.markdown("---")
    # Título indicando que se mostrarán los libros del usuario
    st.title("Mis Libros")

    # Opciones de pestañas para los tipos de libros: Leídos, En Proceso de
    # Lectura, Favoritos
    my_books_tabs = ["Leídos", "En Proceso de Lectura", "Favoritos"]

    # Crear pestañas utilizando st.tabs y asignarlas a las variables read,
    # reading, favorite
    read, reading, favorite = st.tabs(my_books_tabs)

    # Obtener el token de la sesión del usuario, si existe
    token = st.session_state.token if "token" in st.session_state else None

    # Mostrar los libros leídos en la pestaña "Leídos"
    with read:
        list_books_component(
            lambda page, search:
            search_user_books(url,
                              "read",
                              5,
                              page,
                              token,
                              user_id,
                              search),
            "read-list")

    # Mostrar los libros en proceso de lectura en la pestaña "En Proceso de
    # Lectura"
    with reading:
        list_books_component(
            lambda page, search:
            search_user_books(url,
                              "reading",
                              5,
                              page,
                              token,
                              user_id,
                              search),
            "reading-list")

    # Mostrar los libros favoritos en la pestaña "Favoritos"
    with favorite:
        list_books_component(
            lambda page, search:
            search_user_books(url,
                              "favorite",
                              5,
                              page,
                              token,
                              user_id,
                              search),
            "favorite")

    # Estadísticos de lectura
    st.title("Mis estadísticos de lectura")
    estadisticos = search_statistics(url, user_id, token)

    # Crear un gráfico de torta
    fig, ax = plt.subplots()

    total_leidos = estadisticos["distribution"]["reads"]
    total_progreso = estadisticos["distribution"]["reading"]
    total_favoritos = estadisticos["distribution"]["favorite"]

    if total_leidos != 0 or total_favoritos != 0 or total_progreso != 0:
        # Datos para el gráfico de torta
        datos_torta = [total_leidos,
                       total_favoritos,
                       total_progreso,
                       ]
        etiquetas = [f'Leídos\n({total_leidos} libros)',
                     f'Favoritos\n({total_favoritos} libros)',
                     f'En Progreso\n({total_progreso} libros)']

        # Crear el gráfico de torta
        ax.pie(datos_torta, labels=etiquetas, autopct='%1.1f%%', startangle=90,
               counterclock=False)

        # Equal aspect ratio asegura que el gráfico de torta sea circular.
        ax.axis('equal')
        ax.set_title('Distribución de libros por categoría \n')

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Crear un gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(estadisticos["top_authors"]["authors"],
               estadisticos["top_authors"]["counts"])
        ax.set_xlabel('Autores \n')
        ax.set_ylabel('Número de Libros')
        ax.set_title('Top 5 autores más leídos')
        # Establecer el formato de los ticks del eje y para asegurar números
        # enteros
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.xticks(rotation=25, ha="right")
        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Crear un gráfico de barras
        fig, ax = plt.subplots()
        ax.barh(
            [textwrap.shorten(x, 25) for x in estadisticos["top_more_reads"][
                "books"]],
            estadisticos["top_more_reads"]["read_values"])
        ax.set_ylabel('Libros')
        ax.set_xlabel('Número de lecturas')
        ax.set_title('Top libros más veces leídos')
        # Establecer el formato de los ticks del eje y para asegurar números
        # enteros
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    else:
        st.warning("No ha leído ni está leyendo ningún libro hasta el "
                   "momento.")
