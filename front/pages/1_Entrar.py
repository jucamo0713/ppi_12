# Importaciones de librerías de terceros
import requests
import streamlit as st

# Importaciones de módulos internos de la aplicación
from utils.GetUrl import get_url


# Obtener la URL de la API desde las secrets de Streamlit o el archivo .env
url = get_url()


def verificar_credenciales(usuario_input, contrasena_input):
    """
    Verifica las credenciales del usuario.

    Parameters:
        usuario_input (str): Nombre de usuario ingresado por el usuario.
        contrasena_input (str): Contraseña ingresada por el usuario.

    Returns:
        dict or None: Si las credenciales son correctas, devuelve el
        usuario encontrado.
        Si las credenciales son incorrectas, devuelve None.
    """
    # Realiza una solicitud POST a la API para verificar las credenciales
    # del usuario
    response = requests.post(f"{url}/auth/login", json={
        "user": usuario_input,
        "password": contrasena_input,
    })

    # Comprueba el código de estado de la respuesta
    if response.status_code < 200 or response.status_code >= 300:
        # Muestra un error en caso de problemas
        st.error(response.json()['detail'])
        return None
    else:
        # Muestra un mensaje de éxito
        st.success("Inicio de sesión exitoso. ¡Bienvenido!")
        # Devuelve el token de acceso
        return response.json()["access_token"]


# Estado de la aplicación
is_authenticated = False

if "token" in st.session_state:
    # Si se ha almacenado un token en el estado de la sesión, intenta
    # obtener el perfil del usuario
    response = requests.get(f"{url}/user/me", headers={
        "Authentication": f"Bearer {st.session_state.token}"})
    if 200 <= response.status_code < 300:
        is_authenticated = True
        # Almacena el perfil del usuario en el estado de la sesión
        st.session_state.user = response.json()

# Logo en la esquina superior derecha
st.markdown(
    """
    <style>
    .logo-container {
        position: fixed;
        top: 50px;
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

if not is_authenticated:
    # Si el usuario no está autenticado
    st.title("Inicia sesión en LitWave")
    # Campo de entrada para el nombre de usuario
    usuario_input = st.text_input("Ingrese su nombre de usuario",
                                  disabled=is_authenticated)
    # Campo de entrada para la contraseña
    contrasena_input = st.text_input("Ingrese su contraseña",
                                     type="password",
                                     disabled=is_authenticated)
    # Botón para iniciar sesión
    if st.button("Iniciar Sesión"):
        token = verificar_credenciales(usuario_input, contrasena_input)
        # Verifica las credenciales
        if token:
            # Almacena el token en el estado de la sesión
            st.session_state.token = token
            is_authenticated = True
            # Reinicia la aplicación para mostrar la página autenticada
            st.rerun()
else:
    # Muestra un mensaje si el usuario ya está autenticado
    st.success("Ya has iniciado sesión")
