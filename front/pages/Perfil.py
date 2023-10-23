import streamlit as st
from streamlit import session_state

# Obtener el nombre de usuario de la URL
if 'usuario' in st.experimental_get_query_params():
    usuario = st.experimental_get_query_params()['usuario'][0]

    # Verificar si el usuario está autenticado y autorizado
    if hasattr(session_state, 'usuario') and session_state.usuario["usuario"] == usuario:
        st.title(f"Bienvenido, {usuario}!")

        # Obtener y mostrar los datos actuales del usuario
        nombre_actual = session_state.usuario.get("nombres_apellidos", "")
        email_actual = session_state.usuario.get("email", "")
        contrasena_actual = session_state.usuario.get("contrasena", "")

        # Campo de entrada para la contraseña actual
        contrasena_anterior = st.text_input("Contraseña Actual", type="password")

        # Verificar la contraseña anterior antes de permitir cambios
        if contrasena_anterior == contrasena_actual:
            # Iniciar el formulario
            with st.form(key='cambiar_datos_form'):
                # Campo de entrada para el nuevo nombre
                nuevo_nombre = st.text_input("Nuevo Nombre", nombre_actual)

                # Campo de entrada para el nuevo correo electrónico
                nuevo_email = st.text_input("Nuevo Correo Electrónico", email_actual)

                # Campo de entrada para cambiar la contraseña
                nueva_contrasena = st.text_input("Nueva Contraseña", type="password")
                confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")

                # Botón para guardar los cambios
                if st.form_submit_button("Guardar Cambios"):
                    if nueva_contrasena == confirmar_contrasena:
                        # Lógica para cambiar los datos y la contraseña (reemplaza esto con tu propia lógica)
                        session_state.usuario["nombres_apellidos"] = nuevo_nombre
                        session_state.usuario["email"] = nuevo_email
                        session_state.usuario["contrasena"] = nueva_contrasena
                        st.success("Cambios guardados exitosamente.")
                    else:
                        st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
        elif contrasena_anterior and contrasena_anterior != contrasena_actual:
            st.error("Contraseña incorrecta. Inténtalo de nuevo.")
            
        # Botón para cerrar sesión
        if st.button("Cerrar Sesión"):
            del session_state.usuario
            st.success("Sesión cerrada exitosamente. ¡Hasta luego!")
    else:
        st.error("Acceso no autorizado, inicie sesión para poder acceder.")
