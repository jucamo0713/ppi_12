# Importar librerías necesarias
import requests
import streamlit as st
from fake_useragent import UserAgent

# Importaciones de módulos internos de la aplicación
from components.BookCard import book_card
from components.BookDetailComponent import book_detail_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url

# Inicialización de UserAgent para generar el User-Agent
ua = UserAgent()

# Obtener la URL base
url = get_url()

# Configuración básica de la aplicación web
value = basic_config(url=url)

# Número máximo de libros a mostrar por página
LIMIT = 15


# Función para volver a la lista de libros
def volver():
    """
    Función que permite volver del detalle al listado.
    """
    del st.experimental_get_query_params()['book_id']
    st.experimental_set_query_params()


# Función para reiniciar los parámetros de paginación
def restart_pagination_params():
    st.session_state.page = 1


# Verifica si 'value' tiene un valor verdadero, lo que significa que la
# configuración básica fue exitosa.
if value:

    # Verificar si se proporciona 'book_id' en la URL
    if "book_id" in st.experimental_get_query_params():

        # Muestra un botón "Volver" que llama a la función 'volver' cuando
        # se hace clic.
        st.button('Volver', key='volver', on_click=volver)

        # Llama al componente 'book_detail_component' con el valor de
        # 'book_id' y la URL.
        book_detail_component(st.experimental_get_query_params()["book_id"][0],
                              url=url)
        # Muestra otro botón "Volver" para proporcionar otra forma de regresar.
        st.button('Volver', key='volver2', on_click=volver)

    else:
        # Si 'book_id' no está en la URL, muestra la lista de libros.
        # Inicializar el estado de la sesión para el paginado
        if 'page' not in st.session_state:
            # Si 'page' no está definido en el estado de sesión,
            # inicialízalo con 1.
            st.session_state.page = 1

        # Título de la página
        st.header("Explora y descubre nuevos autores y libros")

        # Muestra una barra de búsqueda para que los usuarios ingresen
        # términos de búsqueda.
        # Cuando cambia el valor en la barra de búsqueda, se llama a la
        # función 'restart_pagination_params'.
        busqueda = st.text_input("Buscar libro",
                                 on_change=lambda: restart_pagination_params())

        # Realiza una solicitud HTTP GET a la API para obtener una lista de
        # libros.
        # Los parámetros incluyen el término de búsqueda, el límite de
        # resultados y la página actual.
        # La respuesta se almacena en 'response'.
        response = requests.get(f"{url}/books", {
            'search_param': busqueda,
            'limit': LIMIT,
            'page': st.session_state.page
        }).json()

        # Extrae la lista de libros de la respuesta.
        libros = response['data']
        # Extrae los metadatos de la respuesta.
        metadata = response['metadata']

        # Divide la página en 5 columnas para mostrar los libros.
        columnas = st.columns(5)

        # Mapeo de todos los libros
        for i, resultado in enumerate(libros):
            # Recorre todos los libros y sus detalles.

            # Se coloca un separador cada vez que termine una fila
            if i != 0 and i % 5 == 0:
                # Agrega un separador horizontal (línea) después de cada
                # fila de 5 libros.
                st.markdown("---")
                # Crea un nuevo contenedor de 5 columnas para los libros
                # para mantener una estructura uniforme
                columnas = st.columns(5)

            # Alterna entre las 5 columnas para mostrar los libros en cada
            # columna.
            with ((columnas[i % 5])):
                # Llama al componente 'book_card' para mostrar los detalles
                # del libro.
                book_card(resultado)

        # Paginación
        if metadata['total_pages'] > 1:
            # Muestra información de paginación que indica la página actual
            # y el total de páginas.
            st.write(
                f"Mostrando página {st.session_state.page} de "
                f"{int(metadata['total_pages'])}")
            # Proporciona un campo numérico para que los usuarios ingresen
            # el número de página.
            st.number_input("page", key="page", label_visibility='hidden',
                            step=1, min_value=1,
                            max_value=int(metadata['total_pages']))

        st.markdown("---")

        # Mensaje si no hay resultados
        if not libros:
            # Si no se encontraron libros que coincidan con la búsqueda,
            # muestra un mensaje informativo.
            st.info("No se encontraron resultados para la búsqueda.")
