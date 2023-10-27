# Importar librerías
import streamlit as st
from dotenv import dotenv_values

# Cargar la configuración desde el archivo .env
config = dotenv_values(".env")


def get_url():
    """
    Obtiene la URL de la aplicación de backend desde secrets o desde el
    archivo de configuración.

    :return: La URL del backend.
    """
    # Intentamos obtener la URL del backend desde secrets, si están
    # disponibles y la clave 'BACK_URL' está presente.
    if st.secrets and 'BACK_URL' in st.secrets:
        return st.secrets['BACK_URL']
    # En caso contrario, la obtenemos desde el archivo de configuración.
    else:
        return config['BACK_URL']
