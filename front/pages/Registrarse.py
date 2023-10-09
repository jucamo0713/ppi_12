import streamlit as st
from datetime import datetime

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
        <img src="https://i.ibb.co/CWhPGm1/logo.png" alt="logo"style="max-width: 150px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Regístrate en LitWave")

# Campos de entrada para el registro
nombres_apellidos = st.text_input("Nombres y Apellidos")
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")
confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
correo_electronico = st.text_input("Correo Electrónico")
# Establece el rango mínimo para permitir años anteriores a 2013
min_fecha_nacimiento = datetime(1900, 1, 1)
fecha_nacimiento = st.date_input("Fecha de Nacimiento", min_value=min_fecha_nacimiento, max_value=datetime.now())


# Casillas de verificación para términos y condiciones, y política de privacidad
aceptar_terminos = st.checkbox("Al marcar esta casilla, acepto los términos y condiciones del servicio.")
aceptar_privacidad = st.checkbox("Al marcar esta casilla, confirmo que he leído y aceptado la política de privacidad de la aplicación.")

# Botón para registrar al usuario
if st.button("Registrarse"):
    
    # Verificar si las contraseñas coinciden y las casillas de verificación están marcadas
    if contrasena == confirmar_contrasena and aceptar_terminos and aceptar_privacidad:
        
        # Guardar el usuario en la base de datos o realizar otras acciones necesarias
        st.success("Registro exitoso. ¡Bienvenido, {}!".format(nombres_apellidos))
    elif contrasena != confirmar_contrasena:
        st.error("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
    else:
        st.error("Debes aceptar los términos y condiciones y la política de privacidad para registrarte.")
