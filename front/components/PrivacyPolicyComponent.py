import streamlit as st


def privacy_policy_component():
    """
    Muestra el componente de política de privacidad.

    El componente muestra el contenido del archivo 'PrivacyPolicy.html'.

    """
    # Leer y mostrar el contenido del archivo 'PrivacyPolicy.html' de forma
    # segura.
    st.markdown(open('./front/components/PrivacyPolicy.html').read(),
                unsafe_allow_html=True)
