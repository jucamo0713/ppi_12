from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")


class Connection:
    def __init__(self, app):
        @app.on_event("startup")
        def startup_db_client():
            app.mongodb_client = MongoClient(config["ATLAS_URI"])
            app.database = app.mongodb_client[config["DB_NAME"]]
            print("Connected to the MongoDB database!")

        @app.on_event("shutdown")
        def shutdown_db_client():
            app.mongodb_client.close()
