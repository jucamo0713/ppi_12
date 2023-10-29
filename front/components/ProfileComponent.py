# Importaciones de librerías de terceros
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
        if st.button("Ver mis listas de libros"):
            # Opción de selección para elegir la lista a mostrar
            categoria_seleccionada = st.selectbox("Selecciona una categoría",
                                                  ["Leídos",
                                                   "En Proceso de Lectura",
                                                   "Favoritos"])

            st.title("Mis Libros")

            # datos prueba
            libros_leidos = [{
                "titulo": "No sé cómo mostrar dónde me duele",
                "autor": "Amalia Andrade",
                "imagen": "https://planetadelibrosco2.cdnstatics.com/usuaris/libros/fotos/386/original/portada_no-se-como-mostrar-donde-me-duele_amalia-andrade_202307311626.png"
            }]
            libros_leyendo = [{
                "titulo": "El Alquimista",
                "autor": "Paulo Coelho",
                "imagen": "https://planetadelibrosco2.cdnstatics.com/usuaris/libros/fotos/384/original/portada_el-alquimista_paulo-coelho_202306160135.jpg"
            }]
            libros_favoritos = []

            # Mostrar la lista seleccionada
            if categoria_seleccionada == "Leídos":
                if libros_leidos:
                    st.header("Leídos")
                    st.table(libros_leidos)
                else:
                    st.info("No hay libros leídos en tu lista.")
            elif categoria_seleccionada == "En Proceso de Lectura":
                if libros_leyendo:
                    st.header("En Proceso de Lectura")
                    st.table(libros_leyendo)
                else:
                    st.info("No hay libros en proceso de lectura en tu lista.")
            elif categoria_seleccionada == "Favoritos":
                if libros_favoritos:
                    st.header("Favoritos")
                    st.table(libros_favoritos)
                else:
                    st.info("No hay libros favoritos en tu lista.")
        # Botón para cerrar sesión
        st.button("Cerrar Sesión", on_click=close_session)
        return True
    else:
        return False
