# Importaciones de librerías de terceros
import streamlit as st


def sobre_nosotros_component():
    st.markdown("## Bienvenido a la red social de los lectores")
    st.markdown("### LitWave es una plataforma para los amantes de la "
                "lectura, donde podrás:")
    st.write("- Descubrir nuevos libros recomendados especialmente para ti.")
    st.write("- Conectar, interactuar y compartir tu pasión por los libros.")
    st.write("- Comentar tus opiniones sobre libros y autores.")
    st.write("- Crear tus propias listas de lectura para enriquecer tu "
             "experiencia literaria.")
    st.write("- Seguir a otros lectores, dar me gusta y comentarles.")

    # Información de contacto y redes sociales en el pie de página
    st.markdown("---")
    st.markdown("### Contactos")
    st.write("Para consultas y soporte, contáctanos en:")
    st.write("Hinara Pastora Sánchez Mata. Correo electrónico: "
             "hisanchezm@unal.edu.co")
    st.write("Juan Camilo Montoya Mejía. Correo electrónico: "
             "jumontoyame@unal.edu.co")

    # Pie de página
    st.write("© 2023 LitWave. Todos los derechos reservados.")
