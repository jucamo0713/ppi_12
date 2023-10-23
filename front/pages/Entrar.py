import requests
import streamlit as st
from streamlit import session_state
from dotenv import dotenv_values

config = dotenv_values(".env")

url = st.secrets['BACK_URL'] if st.secrets and 'BACK_URL' in st.secrets else \
    config['BACK_URL']


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
    response = requests.post(f"{url}/auth/login", json={
        "user": usuario_input,
        "password": contrasena_input,
    })
    if response.status_code < 200 or response.status_code >= 300:
        st.error(response.json()['detail'])
    else:
        st.success(
            "Inicio de sesión exitoso. ¡Bienvenido!")
    return response.json()["access_token"]


# Estado de la aplicación
is_authenticated = False if not ("token" in st.session_state) else True

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
    st.title("Inicia sesión en LitWave")
    usuario_input = st.text_input("Ingrese su nombre de usuario")
    contrasena_input = st.text_input("Ingrese su contraseña", type="password")
    if st.button("Iniciar Sesión"):
        token = verificar_credenciales(usuario_input, contrasena_input)
        if token:
            session_state.token = token
            is_authenticated = True
            # redirigir_a_pagina_privada()  # Llama a la función de redirección
else:
    st.write("Ya estás loggueado")