from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

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

@app.get("/productos/{id}")
def obtener_producto(id: str):
    for producto in inventario:
        if producto.id == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/productos/{id}")
def eliminar_producto(id: str):
    for producto in inventario:
        if producto.id == id:
            inventario.remove(producto)
            return {"mensaje": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.put("/productos/{id}")
def actualizar_producto(id: str, producto_nuevo: Producto):
    for i, producto in enumerate(inventario):
        if producto.id == id:
            inventario[i] = producto_nuevo
            return producto_nuevo
    raise HTTPException(status_code=404, detail="Producto no encontrado")