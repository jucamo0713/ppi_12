# Importar librerías
import requests
import streamlit as st
from dotenv import dotenv_values
from pages import Sobre_nosotros, Registrarse

config = dotenv_values(".env")
# Inicializar el estado de la sesión para el paginado
if 'page' not in st.session_state:
    st.session_state.page = 1

pagination = {
    'LIMIT': 2,
    'page': st.session_state.page + 1 if 'next_page' in st
    .session_state and st.session_state.next_page else
    st.session_state.page - 1 if 'prev_page' in st
    .session_state and st.session_state.prev_page else
    st.session_state.page
}
st.session_state.page = pagination['page']
url = st.secrets['BACK_URL'] if st.secrets and 'BACK_URL' in st.secrets else\
    config['BACK_URL']
try:
    value = requests.get(url).json()['success']
except requests.exceptions.RequestException:
    value = False

if value:
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
            <img src="https://i.ibb.co/CWhPGm1/logo.png" 
            alt="logo"style="max-width: 150px; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Lista de libros con datos de prueba (título, autor y URL de la imagen)

    st.header("Explora y descubre nuevos autores y libros")
    # Barra de búsqueda
    busqueda = st.text_input("Buscar libro")
    response = requests.get(f"{url}/books",
                            {
                                'search_param': busqueda,
                                'limit': pagination['LIMIT'],
                                'page': pagination['page']
                            }).json()
    libros = response['data']
    metadata = response['metadata']
    # Filtra los libros según el término de búsqueda
    # Muestra los resultados en dos columnas
    columnas = st.columns(2)
    for i, resultado in enumerate(libros):
        with columnas[i % 2]:  # Alternar entre las dos columnas
            st.image(resultado["image"], caption=resultado["title"],
                     use_column_width=True)
            st.write("**Título:**", resultado["title"])
            st.write("**Autor:**", resultado["author"])

    # Paginado
    if metadata['totalPages'] > 1:
        st.write(f"Mostrando página {pagination['page']} de"
                 f" {int(metadata['totalPages'])}")
        if pagination['page'] > 1:
            st.button("Anterior", key="prev_page")

        if pagination['page'] < metadata['totalPages']:
            st.button("Siguiente", key="next_page")
    st.markdown("---")

    # Mensaje si no hay resultados
    if not libros:
        st.info("No se encontraron resultados para la búsqueda.")
else:
    # Configurar la página para ocupar toda la pantalla
    st.set_page_config(
        page_title="Aplicación no disponible",
        page_icon=":x:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # Crear la vista de la página
    st.write("""
                # Aplicación no disponible en este momento.
                Lo sentimos, pero la aplicación no está disponible en este 
                momento.
                Por favor, inténtelo de nuevo más tarde.
            """)
