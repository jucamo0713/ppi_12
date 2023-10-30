import requests
import streamlit as st
from fake_useragent import UserAgent


# TODO: documentar
class HttpUtils:

    @classmethod
    def generate_default_headers(cls, ) -> dict:
        return {
            "User-Agent": UserAgent().random
        }

    @classmethod
    def resolve_exceptions(cls, response):
        """
        Maneja excepciones comunes al realizar solicitudes HTTP.

        :param response: La respuesta de la solicitud HTTP.
        """
        if response.status_code < 200 or response.status_code >= 300:
            if response.status_code == 401:
                # Eliminar la información del usuario si no está autenticado
                del st.session_state['user']
                del st.session_state['token']
                st.error("Por favor, vuelva a iniciar sesión")
            try:
                if "detail" in response.json():
                    st.error(response.json()['detail'])
                else:
                    st.error("Error desconocido, inténtelo de nuevo más tarde")
            except Exception:
                st.error("Error desconocido, inténtelo de nuevo más tarde")

    @classmethod
    def get(cls, url: str, query: dict = None, headers: dict = None):
        """
        Realiza una solicitud HTTP GET.

        :param url: La URL de destino.
        :param query: Los query params de la solicitud
        :param headers: Los encabezados de la solicitud
        """
        data = {}
        if query is not None:
            data['params'] = query
        data["headers"] = cls.generate_default_headers()
        if headers is not None:
            data["headers"] = {**data["headers"], **headers}
        response = requests.get(url, **data)
        cls.resolve_exceptions(response)
        return {"success": True, "data": response.json()}

    @classmethod
    def post(cls, url: str, body: dict = None, headers: dict = None,
             query: dict = None):
        """
        Realiza una solicitud HTTP POST.

        :param url: La URL de destino.
        :param body: Datos del cuerpo de la solicitud (opcional).
        :param headers: Encabezados de la solicitud (opcional).
        :param query: Parámetros de consulta (opcional).
        :return: Un diccionario con el resultado de la solicitud.
        """
        data = {}
        if body is not None:
            data['json'] = body
        data["headers"] = cls.generate_default_headers()
        if headers is not None:
            data["headers"] = {**data["headers"], **headers}
        if query is not None:
            data["params"] = query
        response = requests.post(url, **data)
        cls.resolve_exceptions(response)
        return {"success": True, "data": response.json()}

    @classmethod
    def put(cls, url: str, body: dict = None, headers: dict = None, query: dict = None):
        """
        Realiza una solicitud HTTP PUT (por implementar).

        :param url: La URL de destino.
        :param body: Datos del cuerpo de la solicitud (opcional).
        :param headers: Encabezados de la solicitud (opcional).
        :param query: Parámetros de consulta (opcional).
        :return: Un diccionario con el resultado de la solicitud.
        """
        data = {}
        if body is not None:
            data['json'] = body
        data["headers"] = cls.generate_default_headers()
        if headers is not None:
            data["headers"] = {**data["headers"], **headers}
        if query is not None:
            data["params"] = query
        response = requests.put(url, **data)
        cls.resolve_exceptions(response)
        return {"success": True, "data": response.json()}

    @classmethod
    def delete(cls):
        """
        Realiza una solicitud HTTP DELETE (por implementar).
        """
        pass
