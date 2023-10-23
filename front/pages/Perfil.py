import streamlit as st

# Estado de la aplicación: Verifica si el usuario ha iniciado sesión
is_authenticated = "user" in st.session_state

if not is_authenticated:

    if ("closed_session" in st.session_state and
            st.session_state.closed_session):
        # Comprueba si la sesión ya se ha cerrado y muestra un mensaje de éxito
        st.success("Sesión cerrada exitosamente. ¡Hasta luego!")
        del st.session_state.closed_session  # Borra la marca de sesión cerrada

    # Si el usuario no ha iniciado sesión, muestra un mensaje de acceso no
    # autorizado
    st.error("Acceso no autorizado, inicie sesión para poder acceder.")
else:
    # Si el usuario ha iniciado sesión, muestra una bienvenida personalizada
    # y detalles del usuario
    usuario = st.session_state.user
    name = usuario["name"]
    st.title(f"Bienvenido, {name}!")
    st.table(usuario)

    # Botón para cerrar sesión
    if st.button("Cerrar Sesión"):
        # Borra el token de sesión y los datos del usuario
        del st.session_state.token
        del st.session_state.user
        st.session_state.closed_session = True  # Marca la sesión como cerrada
        st.experimental_rerun()  # Reinicia la aplicación para reflejar la
        # sesión cerrada
