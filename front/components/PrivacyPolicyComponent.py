import streamlit as st


def privacy_policy_component():
    st.markdown(open('./front/components/PrivacyPolicy.html').read(),
                unsafe_allow_html=True)
