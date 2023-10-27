import requests
import streamlit as st
from datetime import datetime

from front.components.RegisterComponent import register_component
from front.utils.BasicConfig import basic_config
from front.utils.GetUrl import get_url
from front.utils.GuardSession import guard_session

# Obtener la URL de la API desde las secrets de Streamlit o desde el archivo
# .env
url = get_url()

value = basic_config(url=url)

if value:
    # Estado de la aplicación
    is_authenticated = guard_session(allow_only_unsigned=True)[
        "is_authenticated"]
    if not is_authenticated:
        register_component(url)
