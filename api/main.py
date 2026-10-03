from fastapi import FastAPI
from pydantic import BaseModel

class Producto(BaseModel):
    id: str
    nombre: str
    categoria: str
    precio: float
    ubicacion: str
    stock: int

app = FastAPI()
inventario = [] 

@app.get("/")
def inicio():
    return {"mensaje": "API de inventario funcionando"}

@app.post("/productos")
def crear_producto(producto: Producto):
    inventario.append(producto)
    return producto

@app.get("/productos")
def listar_productos():
    return inventario