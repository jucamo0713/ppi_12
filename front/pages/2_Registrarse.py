# Importaciones de módulos internos de la aplicación
from components.RegisterComponent import register_component
from utils.BasicConfig import basic_config
from utils.GetUrl import get_url
from utils.GuardSession import guard_session


# Obtener la URL de la API desde las secrets de Streamlit o desde el archivo
# .env
url = get_url()

# Configura la aplicación básica
value = basic_config(url=url)

if value:
    # Estado de la aplicación
    is_authenticated = guard_session(allow_only_unsigned=True)[
        "is_authenticated"]
    if not is_authenticated:
        # Muestra el componente de registro de usuario
        register_component(url)
