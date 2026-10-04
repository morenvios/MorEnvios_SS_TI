from pydantic import BaseModel, Field


class Producto(BaseModel):
    id: str
    nombre: str
    categoria: str
    precio: float = Field(ge=0)
    ubicacion: str
    stock: int = Field(ge=0)