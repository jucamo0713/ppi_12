from fastapi import FastAPI
from .db.connection import Connection

app = FastAPI()

modules = [Connection]

for i in modules:
    i(app)


@app.get("/")
async def root():
    return {"succes": True}
