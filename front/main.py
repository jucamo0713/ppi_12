# Importar librerías
import streamlit as st

# Título y autor
st.title("LitWave")
st.markdown("Esta app fue elaborada por\
 Hinara Sánchez y Juan Montoya.")

# Menú lateral
menu = st.sidebar.selectbox("Menú", ["Inicio", "Entrar", "Registrarse"])

# Contenido según la opción seleccionada
if menu == "Inicio":
    st.header("Bienvenido a LitWave")
    st.write("LitWave es una plataforma para los amantes de la lectura,\
        donde puedes descubrir nuevos libros,\
        compartir tus experiencias de lectura \
        y conectarte con otros lectores.")

elif menu == "Entrar":
    st.header("Inicio de Sesión")

elif menu == "Registrarse":
    st.header("Registro")

# Pie de página
st.markdown("---")
st.write("© 2023 LitWave. Todos los derechos reservados.")
