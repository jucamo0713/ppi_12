# Importaciones de librerías de terceros
import streamlit as st


def terms_conditions_component():
    """
    Muestra los Términos y Condiciones de Uso de LitWave en un formato legible
    en Streamlit.

    Este componente utiliza las funciones de Streamlit para presentar de
    manera organizada los términos y condiciones de uso de LitWave.

    Returns:
        None
    """

    # Títulos
    st.title("Términos y Condiciones de Uso de LitWave")
    st.subheader("Fecha de entrada en vigor: 15 de noviembre de 2023")

    # Secciones
    st.header("1. Registro y Cuenta de Usuario")
    st.write(
        "1.1. Para utilizar LitWave, debes registrarte y crear una cuenta de "
        "usuario. "
        "Debes proporcionar información precisa y actualizada durante el "
        "proceso de registro.")
    st.write(
        "1.2. Eres responsable de mantener la confidencialidad de tu "
        "información de inicio de sesión y contraseña. "
        "No compartas tus credenciales de acceso con terceros.")
    st.write(
        "1.3. Debes ser mayor de 13 años para utilizar LitWave. Si eres menor "
        "de 18 años, debes obtener el consentimiento de tus padres o tutores "
        "legales.")

    st.header("2. Contenido y Comunicación")
    st.write(
        "2.1. LitWave es una plataforma para compartir contenido relacionado "
        "con la lectura. Al utilizar la aplicación, aceptas no publicar,"
        " enviar o compartir contenido que sea ilegal, difamatorio, obsceno, "
        "abusivo, ofensivo o de cualquier otra manera inapropiado.")
    st.write(
        "2.2. Respetamos los derechos de autor. No debes publicar contenido "
        "que infrinja los derechos de propiedad intelectual de terceros, a "
        "menos que tengas los derechos legales para hacerlo.")
    st.write(
        "2.3. Fomentamos la discusión y el intercambio de ideas, pero no "
        "toleramos el acoso, el discurso de odio o cualquier forma de "
        "comportamiento perjudicial hacia otros usuarios.")

    st.header("3. Privacidad y Datos Personales")
    st.write(
        "3.1. Respetamos tu privacidad. Consulta nuestra Política de "
        "Privacidad para obtener más información sobre cómo recopilamos, "
        "utilizamos y protegemos tus datos personales.")

    st.header("4. Seguridad y Responsabilidad")
    st.write(
        "4.1. LitWave se esfuerza por proporcionar un entorno seguro, pero no "
        "podemos garantizar la seguridad absoluta. Eres responsable de tu "
        "propia seguridad y debes informar cualquier actividad sospechosa o "
        "violación de seguridad.")
    st.write(
        "4.2. No somos responsables de los daños o pérdidas resultantes del "
        "uso de LitWave.")

    st.header("5. Terminación de la Cuenta")
    st.write(
        "5.1. Nos reservamos el derecho de suspender o cerrar tu cuenta si "
        "incumples estos términos y condiciones.")

    st.header("6. Modificaciones de los Términos y Condiciones")
    st.write(
        "6.1. Nos reservamos el derecho de modificar estos términos y "
        "condiciones en cualquier momento. Te notificaremos de cualquier "
        "cambio y te recomendamos revisarlos regularmente.")

    st.header("7. Contacto")
    st.write(
        "7.1. Si tienes preguntas o comentarios sobre estos términos y "
        "condiciones, puedes contactarnos por medio de hisanchezm@unal.edu.co "
        "o jumontoyame@unal.edu.co.")
