import requests
import streamlit as st


class HttpUtils:
    @classmethod
    def resolve_exceptions(cls, response):
        if response.status_code < 200 or response.status_code >= 300:
            if response.status_code == 401:
                # Eliminar la información del usuario si no está autenticado
                del st.session_state['user']
                del st.session_state['token']
                st.error(
                    "Por favor, vuelva a iniciar sesión")
            try:
                if "detail" in response.json():
                    st.error(response.json()['detail'])
                else:
                    st.error(
                        "Error desconocido, inténtelo de nuevo más tarde")
            except Exception:
                st.error(
                    "Error desconocido, inténtelo de nuevo más tarde")

    @classmethod
    def get(cls, url: str):
        pass

    @classmethod
    def post(cls, url: str,
             body: dict = None,
             headers: dict = None,
             query: dict = None):
        data = {}
        if body is not None:
            data['json'] = body
        if query is not None:
            data['params'] = query
        if headers is not None:
            data['headers'] = headers
        print(data)
        response = requests.post(url, **data)
        cls.resolve_exceptions(response)
        return {"success": True, "data": response.json()}

    @classmethod
    def put(cls):
        pass

    @classmethod
    def delete(cls):
        pass
