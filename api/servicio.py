from fastapi import HTTPException
from modelos import Producto

inventario = []


def listar():
    return inventario


def crear(producto: Producto):
    for existente in inventario:
        if existente.id == producto.id:
            raise HTTPException(status_code=409, detail="Ya existe un producto con ese id")
    inventario.append(producto)
    return producto

def obtener(id: str):
    for producto in inventario:
        if producto.id == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


def actualizar(id: str, producto_nuevo: Producto):
    for i, producto in enumerate(inventario):
        if producto.id == id:
            inventario[i] = producto_nuevo
            return producto_nuevo
    raise HTTPException(status_code=404, detail="Producto no encontrado")


def eliminar(id: str):
    for producto in inventario:
        if producto.id == id:
            inventario.remove(producto)
            return {"mensaje": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")