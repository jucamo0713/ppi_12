import numpy as np
from fastapi import FastAPI
from .book.BookRoutes import BookRoutes
from .db.connection import Connection

app = FastAPI()

modules = [Connection]

for i in modules:
    i(app)


@app.get("/")
async def root():
    return {"success": True}


routers = np.array(BookRoutes).flat
for r in routers:
    app.include_router(r['instance'], tags=[r['tag']], prefix=r['path'])
