import requests
import streamlit as st
from fake_useragent import UserAgent


# Clase de utilidades HTTP
class HttpUtils:
    @classmethod
    def generate_default_headers(cls) -> dict:
        """
        Genera un diccionario de encabezados HTTP con un User-Agent aleatorio.

        Returns:
            dict: Un diccionario de encabezados HTTP con User-Agent aleatorio.
        """
        return {
            "User-Agent": UserAgent().random
        }

    @classmethod
    def resolve_exceptions(cls, response):
        """
        Maneja excepciones comunes al realizar solicitudes HTTP.

        Args:
            response: La respuesta de la solicitud HTTP.
        """
        if response.status_code < 200 or response.status_code >= 300:
            if response.status_code == 401:
                # Elimina la información del usuario si no está autenticado
                del st.session_state['user']
                del st.session_state['token']
                st.error("Por favor, vuelva a iniciar sesión")
                return False
            try:
                if "detail" in response.json():
                    st.error(response.json()['detail'])
                else:
                    st.error("Error desconocido, inténtelo de nuevo más tarde")
                return False
            except Exception:
                st.error("Error desconocido, inténtelo de nuevo más tarde")
                return False
        return True

    @classmethod
    def get(cls, url: str, query: dict = None, headers: dict = None,
            authorization: str = None):
        """
        Realiza una solicitud HTTP GET.

        Args:
            url (str): La URL de destino.
            query (dict, optional): Los parámetros de consulta (query params).
            headers (dict, optional): Los encabezados de la solicitud.
            authorization (str, optional): El token de autorización.

        Returns:
            dict: Un diccionario con el resultado de la solicitud.

        - success (bool): Un indicador de éxito.
        - data (dict): Los datos de la respuesta de la solicitud.
        """
        data = {}
        if query is not None:
            data['params'] = query
        data["headers"] = cls.generate_default_headers()
        if headers is not None:
            data["headers"] = {**data["headers"], **headers}
        if authorization is not None:
            data["headers"]['authentication'] = f'Bearer {authorization}'
        response = requests.get(url, **data)
        if cls.resolve_exceptions(response):
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    @classmethod
    def post(cls, url: str, body: dict = None, headers: dict = None,
             query: dict = None, authorization: str = None):
        """
        Realiza una solicitud HTTP POST.

        Args:
            url (str): La URL de destino.
            body (dict, optional): Datos del cuerpo de la solicitud.
            headers (dict, optional): Los encabezados de la solicitud.
            query (dict, optional): Parámetros de consulta.
            authorization (str, optional): El token de autorización.

        Returns:
            dict: Un diccionario con el resultado de la solicitud.

        - success (bool): Un indicador de éxito.
        - data (dict): Los datos de la respuesta de la solicitud.
        """
        data = {}
        if body is not None:
            data['json'] = body
        data["headers"] = cls.generate_default_headers()
        if headers is not None:
            data["headers"] = {**data["headers"], **headers}
        if authorization is not None:
            data["headers"]['authentication'] = f'Bearer {authorization}'
        if query is not None:
            data["params"] = query
        response = requests.post(url, **data)
        if cls.resolve_exceptions(response):
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    @classmethod
    def put(cls, url: str, body: dict = None, headers: dict = None,
            query: dict = None):
        """
        Realiza una solicitud HTTP PUT.

        Args:
            url (str): La URL de destino.
            body (dict, optional): Datos del cuerpo de la solicitud.
            headers (dict, optional): Los encabezados de la solicitud.
            query (dict, optional): Parámetros de consulta.

        Returns:
            dict: Un diccionario con el resultado de la solicitud.

        - success (bool): Un indicador de éxito.
        - data (dict): Los datos de la respuesta de la solicitud.
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
        if cls.resolve_exceptions(response):
            return {"success": True, "data": response.json()}
        else:
            return {"success": False}

    @classmethod
    def delete(cls):
        """
        Realiza una solicitud HTTP DELETE (por implementar).
        """
        pass
