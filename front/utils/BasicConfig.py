# Importar librerías necesarias
import requests
import streamlit as st

from front.utils.GetUrl import get_url


def basic_config(url=None):
    """
    Configura la página de Streamlit y muestra elementos como el logo,
    título y pie de página.

    :param url: La URL de la API de backend (opcional).
    :return: True si la API está disponible, False si no lo está.
    """
    # Configuración de la página de Streamlit
    st.set_page_config(
        page_title="LitWave",
        page_icon="https://i.ibb.co/CWhPGm1/logo.png",
        initial_sidebar_state="collapsed",
    )

    # Barra lateral con logo, título y pie de página
    with st.sidebar:
        [logo, title] = st.columns(2)
        with logo:
            st.image("https://i.ibb.co/CWhPGm1/logo.png", width=100)
        with title:
            st.title("LitWave")
        # Pie de página
        st.write("© 2023 LitWave. Todos los derechos reservados.")

    try:
        if url is None:
            url = get_url()
        # Realizar una solicitud a la API para verificar si está disponible
        response = requests.get(url)
        value = response.status_code == 200
    except requests.exceptions.RequestException:
        value = False

    if value:
        # Logo en la esquina superior izquierda
        [logo, title, *_] = st.columns(6)
        with logo:
            st.image("https://i.ibb.co/CWhPGm1/logo.png", width=100)
        with title:
            st.title("LitWave")
    else:
        # Página de advertencia si la API no está disponible
        st.write("""
            # Aplicación no disponible en este momento.
            Lo sentimos, pero la aplicación no está disponible en este 
            momento. Por favor, inténtelo de nuevo más tarde.
        """)

    return value
