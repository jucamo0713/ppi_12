import streamlit as st


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


def profile_component():
    """
    Muestra el componente de perfil de usuario si el usuario está autenticado.

    :return: True si el usuario está autenticado y se muestra el perfil,
    False en caso contrario.
    """
    usuario = st.session_state.user
    if "user" in st.session_state:
        name = usuario["name"]
        st.title(f"Bienvenido, {name}!")
        data = {
            "Nombre": name,
            "Usuario": usuario["user"],
            "Correo": usuario["email"],
            "Fecha de nacimiento": usuario["burn_date"],
            "Fecha de registro": usuario["registered_date"]
        }
        st.table(data)
        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)
        return True
    else:
        return False
