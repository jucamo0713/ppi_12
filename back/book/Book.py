from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(alias="_id")
    titulo: str = Field(...)
    author: str = Field(...)
    imagen: str = Field(...)
