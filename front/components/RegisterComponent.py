from datetime import datetime
from typing import Literal

import streamlit as st

from front.components.PrivacyPolicyComponent import privacy_policy_component
from front.utils.HttpUtils import HttpUtils

# Establece el rango mínimo para permitir años anteriores a 2013
MIN_FECHA_NACIMIENTO = datetime(1900, 1, 1)


def validar_contrasena() -> bool:
    value = st.session_state.password == st.session_state.confirm_password
    st.session_state.valid_password = value
    return value


def validar_campos() -> bool:
    if 'name' not in st.session_state or st.session_state.name == '':
        st.error("Porfavor llene el campo de nombre")
        return False
    if 'username' not in st.session_state or st.session_state.username == '':
        st.error("Porfavor llene el campo de username")
        return False
    if 'password' not in st.session_state or st.session_state.password == '':
        st.error("Porfavor llene el campo de contraseña")
        return False
    if ('confirm_password' not in st.session_state or
            st.session_state.confirm_password == ''):
        st.error("Porfavor llene el campo de confirmar contraseña")
        return False
    if 'email' not in st.session_state or st.session_state.email == '':
        st.error("Porfavor llene el campo de correo electrónico")
        return False
    return True


def registrar(url: str):
    if validar_campos():
        burn = datetime(st.session_state.burn_date.year,
                        st.session_state.burn_date.month,
                        st.session_state.burn_date.day).isoformat() + "Z"
        print(burn)
        response = HttpUtils.post(f"{url}/auth/register", body={
            "name": st.session_state.name,
            "user": st.session_state.username,
            "password": st.session_state.password,
            "email": st.session_state.email,
            "burn_date": burn
        })
        if response['success']:
            st.success(
                "Registro exitoso. Ya te puedes dirigir al login para "
                "ingrersar a la plataforma")


def exciter(read: Literal["read_privacy", "read_terms"], default: dict = None):
    if default is not None:
        for key in default:
            st.session_state[key] = default[key]

    if read == "read_privacy":
        def helper():
            st.session_state.show_privacy = False
            st.session_state.read_privacy = True
    else:
        def helper():
            st.session_state.show_terms = False
            st.session_state.read_terms = True
    return helper


def register_component(url: str):
    # Establece el rango máximo para  no permitir menores de 13 años
    current_date = datetime.now()
    max_fecha_nacimiento = datetime(current_date.year - 13,
                                    current_date.month, current_date.day)
    if 'show_privacy' in st.session_state and st.session_state.show_privacy:
        privacy_policy_component()
        st.button('Salir',
                  on_click=exciter("read_privacy",
                                   default=st.session_state.to_dict()))
    elif 'show_terms' in st.session_state and st.session_state.show_terms:
        st.button('Salir',
                  on_click=exciter('read_terms', st.session_state.to_dict()))
    else:
        if 'read_terms' not in st.session_state:
            st.session_state.read_terms = False
        if 'read_privacy' not in st.session_state:
            st.session_state.read_privacy = False
        if 'name' not in st.session_state:
            st.session_state.name = ''
        if 'username' not in st.session_state:
            st.session_state.username = ''
        if 'password' not in st.session_state:
            st.session_state.password = ''
        if 'confirm_password' not in st.session_state:
            st.session_state.confirm_password = ''
        if 'email' not in st.session_state:
            st.session_state.email = ''
        if 'burn_date' not in st.session_state:
            st.session_state.burn_date = max_fecha_nacimiento
        if 'allow_privacy' not in st.session_state:
            st.session_state.allow_privacy = False
        if 'allow_terms' not in st.session_state:
            st.session_state.allow_terms = False
        st.title("Regístrate en LitWave")
        # Campos de entrada para el registro
        st.text_input("Nombres y Apellidos",
                      key='name',
                      value=st.session_state.name)
        st.text_input("Usuario",
                      key='username',
                      value=st.session_state.username)
        st.text_input("Contraseña",
                      type="password",
                      key="password",
                      on_change=validar_contrasena,
                      value=st.session_state.password)
        st.text_input("Confirmar Contraseña",
                      key='confirm_password',
                      type="password",
                      on_change=validar_contrasena,
                      value=st.session_state.confirm_password)
        if (st.session_state.confirm_password != '' and 'valid_password' in
                st.session_state and not st.session_state.valid_password):
            st.error("contraseñas no coinciden")
        st.text_input("Correo Electrónico", key='email',
                      value=st.session_state.email)
        st.date_input(
            "Fecha de Nacimiento",
            min_value=MIN_FECHA_NACIMIENTO,
            max_value=max_fecha_nacimiento,
            key='burn_date',
            value=st.session_state.burn_date)
        # Casillas de verificación para términos y condiciones, y política de
        # privacidads
        terminos, privacidad = st.columns(2)
        with terminos:
            st.checkbox(
                "Al marcar esta casilla, acepto los términos y condiciones "
                "del servicio.",
                key="allow_terms",
                disabled=not st.session_state.read_terms,
                value=st.session_state.allow_terms)
        with privacidad:
            st.checkbox(
                "Al marcar esta casilla, confirmo que he leído y aceptado la "
                "política de privacidad de la aplicación.",
                key="allow_privacy",
                disabled=not st.session_state.read_privacy,
                value=st.session_state.allow_privacy)
        terminos, privacidad = st.columns(2)
        with terminos:
            st.button("Terminos y condiciones",
                      use_container_width=True,
                      on_click=(lambda: st.session_state.update(
                          show_terms=True)))
        with privacidad:
            st.button("Politica de Privacidad",
                      use_container_width=True,
                      on_click=(lambda: st.session_state.update(
                          show_privacy=True)))
        # Botón para registrar al usuario
        st.button("Registrarse",
                  disabled=(not (st.session_state.allow_privacy and
                                 st.session_state.allow_terms)),
                  on_click=registrar, args=[url])
