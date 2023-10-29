# Importaciones de librerías de terceros
from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")


class Connection:
    """
    Clase para gestionar la conexión a una base de datos MongoDB.

    Esta clase se encarga de establecer la conexión a la base de datos MongoDB
    al iniciar la aplicación y de cerrar la conexión al detener la aplicación.

    Métodos:
    - __init__(self, app): Constructor de la clase que recibe una instancia
    de FastAPI (app).
    - startup_db_client(): Método para iniciar la conexión a la base de
    datos al arrancar la aplicación.
    - shutdown_db_client(): Método para cerrar la conexión a la base de
    datos al detener la aplicación.
    """

    def __init__(self, app):
        """
        Constructor de la clase Connection.

        Parámetros:
        - app: Instancia de FastAPI.
        """
        @app.on_event("startup")
        def startup_db_client():
            """
            Inicia la conexión a la base de datos al arrancar la aplicación.
            """
            app.mongodb_client = MongoClient(config["ATLAS_URI"])
            app.database = app.mongodb_client[config["DB_NAME"]]
            print("Connected to the MongoDB database!")

        @app.on_event("shutdown")
        def shutdown_db_client():
            """
            Cierra la conexión a la base de datos al detener la aplicación.
            """
            app.mongodb_client.close()
