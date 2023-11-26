import streamlit as st


def guard_session(allow_only_signed=False, allow_only_unsigned=False):
    """
    Gestiona la sesión del usuario y proporciona opciones de autenticación.

    :param allow_only_signed: Permite acceso solo a usuarios autenticados (
    predeterminado: False).
    :param allow_only_unsigned: Permite acceso solo a usuarios no
    autenticados (predeterminado: False).
    :return: Un diccionario con el estado de autenticación, el usuario y el token (si
    está autenticado).
    """
    # Estado de la aplicación
    is_authenticated = "user" in st.session_state

    if allow_only_signed and not is_authenticated:
        st.info("Autenticación es requerida")
    elif allow_only_unsigned and is_authenticated:
        st.info("Ya estás autenticado")

    return {
        "is_authenticated": is_authenticated,
        "user": st.session_state['user'] if is_authenticated else None,
        "token": st.session_state['token'] if is_authenticated else None,
    }
