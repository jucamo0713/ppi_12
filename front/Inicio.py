# Importar librerías necesarias
from io import BytesIO

import numpy as np
# Para manipular imagenes
import skimage.io
# Para hacer solicitudes HTTP
import requests
# Para crear la aplicación web
import streamlit as st
from fake_useragent import UserAgent
from front.utils.BasicConfig import basic_config
from front.utils.GetUrl import get_url

ua = UserAgent()
url = get_url()
value = basic_config(url=url)
if value:
    # Verificar si se proporciona 'book_id' en la URL
    if "book_id" in st.experimental_get_query_params():
        # Realizar una solicitud a la API para obtener detalles del libro
        response = requests.get(f"{url}/books/by-id", params={
            "id": st.experimental_get_query_params()["book_id"]})

        # Comprobar el estado de la respuesta
        if response.status_code != 200:
            try:
                if "detail" in response.json():
                    st.error(response.json()['detail'])
                else:
                    st.error(
                        "Error desconocido, inténtelo de nuevo más tarde")
            except Exception:
                st.error(
                    "Error desconocido, inténtelo de nuevo más tarde")
        else:
            # Mostrar los detalles del libro
            book = response.json()
            st.title(book['title'])
            st.image(book['image'])
            st.table(book)

            # Verificar si el usuario está autenticado
            if 'user' in st.session_state:
                # Realizar una solicitud para obtener los datos del usuario
                # para el libro
                response = requests.get(f"{url}/user_book", headers={
                    "Authentication": f"Bearer {st.session_state.token}"},
                                        params={
                                            "book_id": book['_id']})

                if 200 <= response.status_code < 300:
                    data = response.json()
                    columns = st.columns(3)

                    # Mostrar opciones para marcar el libro
                    with columns[0]:
                        read = st.checkbox("Leído", value=data['read'],
                                           key="read")

                    with columns[1]:
                        in_process = st.checkbox(
                            "En proceso de Lectura",
                            value=data['reading'], key="reding")

                    with columns[2]:
                        favorites = st.checkbox("Favoritos",
                                                value=data['favorite'],
                                                key="favorite")

                    if st.button('Guardar'):
                        # Realizar una solicitud para guardar los cambios
                        response = requests.put(
                            f"{url}/user_book/upsert",
                            headers={
                                "Authentication": f"Bearer "
                                                  f"{st.session_state.token}"},
                            params={"book_id": book['_id']},
                            json={
                                "read": read,
                                "reading": in_process,
                                "favorite": favorites,
                            })

                        # Comprobar el estado de la respuesta
                        if 200 <= response.status_code < 300:
                            st.success(
                                "Datos guardados satisfactoriamente")
                        else:
                            if response.status_code == 401:
                                # Eliminar la información del usuario si no
                                # está autenticado
                                del st.session_state['user']
                                del st.session_state['token']
                                st.error(
                                    "Por favor, vuelve a iniciar sesión")
                            elif (
                                    response.json() and 'detail' in
                                    response.json()):
                                st.error(response.json()['detail'])
                            else:
                                st.error("Error desconocido")
                else:
                    if response.status_code == 401:
                        # Eliminar la información del usuario si no
                        # está autenticado
                        del st.session_state['user']
                        del st.session_state['token']
                        st.error(
                            "Por favor, vuelva a iniciar sesión")
                    elif (response.json() and 'detail' in
                          response.json()):
                        st.error(response.json()['detail'])
                    else:
                        st.error("Error desconocido")

        # Función para volver a la lista de libros
        def volver():
            """
            Función que permite volver del detalle al listado.
            """
            del st.experimental_get_query_params()['book_id']
            st.experimental_set_query_params()


        st.button('Volver', key='volver', on_click=volver)
    else:
        # Función para reiniciar los parámetros de paginación
        def restart_pagination_params():
            st.session_state.page = 1


        # Inicializar el estado de la sesión para el paginado
        if 'page' not in st.session_state:
            st.session_state.page = 1

        # Definir los parámetros de paginación (LIMIT y page) basados en el
        # estado de la sesión
        pagination = {
            'LIMIT': 15,
            'page': st.session_state.page + 1
            if 'next_page' in st.session_state and st.session_state.next_page
            else st.session_state.page - 1
            if 'prev_page' in st.session_state and st.session_state.prev_page
            else st.session_state.page
        }
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
        # Lista de libros
        libros = response['data']
        # Metadatos
        metadata = response['metadata']

        columnas = st.columns(5)

        # Mspeo de todos los libros
        for i, resultado in enumerate(libros):
            # Se coloca un separador cada vez que termine una fila
            if i != 0 and i % 5 == 0:
                st.markdown("---")
                columnas = st.columns(5)

            # Alternar entre las 5 columnas
            with ((columnas[i % 5])):
                user_agent = ua.random
                data_image = requests.get(resultado["image"], headers={
                    "User-Agent": user_agent
                })
                if data_image.status_code == 200:
                    # Se crea BytesIO object para que actue como un archivo
                    # falso
                    img_file = BytesIO(data_image.content)
                    try:
                        # Read the image using 'skimage.io.imread'
                        image = skimage.io.imread(img_file)
                        desired_height = image.shape[1] * 3 / 2
                        crop_top = int((image.shape[0] - desired_height) // 2)
                        if crop_top >= 0:
                            crop_bottom = int(image.shape[0] - crop_top)
                            image = image[crop_top:crop_bottom, :]
                        else:
                            black_part = np.zeros((-crop_top, image.shape[
                                1], 3), dtype=np.uint8)
                            image = np.vstack([black_part, image, black_part])
                    except Exception:
                        image = ("https://islandpress.org/sites/default/files"
                                 "/default_book_cover_2015.jpg")
                else:
                    image = ("https://islandpress.org/sites/default/files"
                             "/default_book_cover_2015.jpg")
                st.image(image,
                         use_column_width=True, )
                if len(resultado["title"]) > 30:
                    resultado["title"] = resultado["title"][:30] + "..."

                if len(resultado["author"]) > 30:
                    resultado["author"] = resultado["author"][:30] + "..."
                st.write("**Título:**", resultado["title"])
                st.write("**Autor:**", resultado["author"])
                st.button('Detalle', key=f'detail{i}',
                          on_click=(lambda x: st.experimental_set_query_params(
                              book_id=x)), args=[resultado["_id"]])
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
            st.number_input("page",
                            key="page",
                            step=1, min_value=1,
                            max_value=int(metadata['totalPages']))

        st.markdown("---")

        # Mensaje si no hay resultados
        if not libros:
            st.info("No se encontraron resultados para la búsqueda.")
