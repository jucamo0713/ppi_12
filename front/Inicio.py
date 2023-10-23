# Importar librerías necesarias
import requests  # Para hacer solicitudes HTTP
import streamlit as st  # Para crear la aplicación web
from dotenv import dotenv_values  # Para cargar variables de entorno desde


# un archivo .env


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    st.session_state.page = 1


# Cargar la configuración desde el archivo .env
config = dotenv_values(".env")

# Inicializar el estado de la sesión para el paginado
if 'page' not in st.session_state:
    st.session_state.page = 1

# Definir los parámetros de paginación (LIMIT y page) basados en el estado
# de la sesión
pagination = {
    'LIMIT': 15,
    'page': st.session_state.page + 1
    if 'next_page' in st.session_state and st.session_state.next_page
    else st.session_state.page - 1
    if 'prev_page' in st.session_state and st.session_state.prev_page
    else st.session_state.page
}
st.session_state.page = pagination['page']

# Cargar la URL de la API desde las secrets de Streamlit o desde el archivo
# .env
url = st.secrets['BACK_URL'] if st.secrets and 'BACK_URL' in st.secrets else\
    config['BACK_URL']

try:
    # Realizar una solicitud a la API para verificar si está disponible
    value = requests.get(url).json()['success']
except requests.exceptions.RequestException:
    value = False

if value:
    # Configurar la página de Streamlit
    st.set_page_config(
        page_title="LitWave",
        page_icon="https://i.ibb.co/CWhPGm1/logo.png",
        initial_sidebar_state="collapsed",
    )

    # Logo en la esquina superior derecha
    st.markdown(
        """
        <style>
        .logo-container {
            position: fixed;
            top: 46px;
            right: 10px;
        }
        </style>
        <div class="logo-container">
            <img src="https://i.ibb.co/CWhPGm1/logo.png" alt="logo" 
            style="max-width: 150px; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Título de la página
    st.header("Explora y descubre nuevos autores y libros")

    # Barra de búsqueda
    busqueda = st.text_input("Buscar libro",
                             on_change=lambda: restart_pagination_params())

    # Realizar una solicitud a la API para obtener una lista de libros
    response = requests.get(f"{url}/books", {
        'search_param': busqueda,
        'limit': pagination['LIMIT'],
        'page': pagination['page']
    }).json()
    libros = response['data']  # Lista de libros
    metadata = response['metadata']  # Metadatos

    # Filtrar y mostrar los libros en dos columnas
    columnas = st.columns(5)
    for i, resultado in enumerate(libros):
        with columnas[i % 5]:  # Alternar entre las dos columnas
            st.image(resultado["image"], caption=resultado["title"],
                     use_column_width=True)
            st.write("**Título:**", resultado["title"])
            st.write("**Autor:**", resultado["author"])
            st.markdown("---")

    # Paginación
    if metadata['totalPages'] > 1:
        st.write(
            f"Mostrando página {pagination['page']} de "
            f"{int(metadata['totalPages'])}")
        if pagination['page'] > 1:
            st.button("Anterior", key="prev_page")

        if pagination['page'] < metadata['totalPages']:
            st.button("Siguiente", key="next_page")

        # Selector de página
        st.number_input("page", value=st.session_state.page, key="page",
                        step=1, min_value=1,
                        max_value=int(metadata['totalPages']))

    st.markdown("---")

    # Mensaje si no hay resultados
    if not libros:
        st.info("No se encontraron resultados para la búsqueda.")
else:
    # Página de advertencia si la API no está disponible
    st.write("""
                # Aplicación no disponible en este momento.
                Lo sentimos, pero la aplicación no está disponible en este 
                momento. Por favor, inténtelo de nuevo más tarde.
            """)
