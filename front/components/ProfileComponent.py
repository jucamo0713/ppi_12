import streamlit as st


def close_session():
    # Borra el token de sesión y los datos del usuario
    del st.session_state.token
    del st.session_state.user
    # Marca la sesión como cerrada
    st.session_state.closed_session = True


def profile_component():
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
        st.table(data, )

        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)
        return True
    else:
        return False
