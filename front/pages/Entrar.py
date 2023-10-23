import streamlit as st
from streamlit import session_state

# Datos del usuario de prueba
usuario_prueba = {
    "usuario": "hinara",
    "contrasena": "hinara12",
    "nombres_apellidos": "Hinara Pastora Sánchez Mata",
    "email": "hinarasm01212@gmail.com"
}

def redirigir_a_pagina_privada():
    """
    Redirige a la página privada después de iniciar sesión.
    Establece los parámetros de la URL y redirige a la nueva URL.
    Limpia los parámetros de la URL después de redirigir.
    """
    st.experimental_set_query_params(usuario=session_state.usuario["usuario"])
    st.rerun()
    st.experimental_set_query_params()

def verificar_credenciales(usuario_input, contrasena_input):
    """
    Verifica las credenciales del usuario.
    
    Parameters:
        usuario_input (str): Nombre de usuario ingresado por el usuario.
        contrasena_input (str): Contraseña ingresada por el usuario.
    
    Returns:
        dict or None: Si las credenciales son correctas, devuelve el usuario encontrado.
                     Si las credenciales son incorrectas, devuelve None.
    """
    usuario_encontrado = None
    if usuario_prueba["usuario"] == usuario_input and usuario_prueba["contrasena"] == contrasena_input:
        usuario_encontrado = usuario_prueba
        st.success("Inicio de sesión exitoso. ¡Bienvenido, {}!".format(usuario_encontrado["nombres_apellidos"]))
    else:
        st.error("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
    return usuario_encontrado

# Estado de la aplicación
is_authenticated = False

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
        <img src="https://i.ibb.co/CWhPGm1/logo.png" alt="logo" style="max-width: 150px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

if not is_authenticated:
    st.title("Inicia sesión en LitWave")
    usuario_input = st.text_input("Ingrese su nombre de usuario")
    contrasena_input = st.text_input("Ingrese su contraseña", type="password")
    if st.button("Iniciar Sesión"):
        usuario = verificar_credenciales(usuario_input, contrasena_input)
        if usuario:
            session_state.usuario = usuario
            is_authenticated = True
            redirigir_a_pagina_privada()  # Llama a la función de redirección
