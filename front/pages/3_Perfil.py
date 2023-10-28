import streamlit as st
from components.ProfileComponent import profile_component
from utils.BasicConfig import basic_config
from utils.GuardSession import guard_session

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
        # Muestra el componente del perfil del usuario
        profile_component()
