from fastapi import FastAPI, HTTPException
from modelos import Producto
import servicio

app = FastAPI() 

@app.get("/")
def inicio():
    return {"mensaje": "API de inventario funcionando"}

@app.post("/productos", status_code=201)
def crear_producto(producto: Producto):
    return servicio.crear(producto)

@app.get("/productos")
def listar_productos():
    return servicio.listar()

@app.get("/productos/{id}")
def obtener_producto(id: str):
    return servicio.obtener(id)

@app.put("/productos/{id}")
def actualizar_producto(id: str, producto_nuevo: Producto):
    return servicio.actualizar(id, producto_nuevo)

@app.delete("/productos/{id}")
def eliminar_producto(id: str):
    return servicio.eliminar(id)