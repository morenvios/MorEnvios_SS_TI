import pytest
from fastapi.testclient import TestClient
from main import app
import servicio

client = TestClient(app)

PRODUCTO = {
    "id": "PROD-001",
    "nombre": "Caja de cartón chica",
    "categoria": "empaque",
    "precio": 12.5,
    "ubicacion": "Almacén A",
    "stock": 100,
}


@pytest.fixture(autouse=True)
def limpiar_inventario():
    servicio.inventario.clear()


def test_inicio():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "API de inventario funcionando"}

def test_crear_producto():
    respuesta = client.post("/productos", json=PRODUCTO)
    assert respuesta.status_code == 201
    assert respuesta.json() == PRODUCTO

def test_crear_producto_con_id_repetido():
    client.post("/productos", json=PRODUCTO)
    respuesta = client.post("/productos", json=PRODUCTO)
    assert respuesta.status_code == 409
    assert len(client.get("/productos").json()) == 1

def test_stock_negativo_se_rechaza():
    respuesta = client.post("/productos", json={**PRODUCTO, "stock": -5})
    assert respuesta.status_code == 422
    assert client.get("/productos").json() == []


def test_precio_negativo_se_rechaza():
    respuesta = client.post("/productos", json={**PRODUCTO, "precio": -10})
    assert respuesta.status_code == 422
    assert client.get("/productos").json() == []


def test_stock_cero_se_acepta():
    respuesta = client.post("/productos", json={**PRODUCTO, "stock": 0})
    assert respuesta.status_code == 201

def test_obtener_producto():
    client.post("/productos", json=PRODUCTO)
    respuesta = client.get("/productos/PROD-001")
    assert respuesta.status_code == 200
    assert respuesta.json() == PRODUCTO


def test_obtener_producto_inexistente():
    respuesta = client.get("/productos/PROD-999")
    assert respuesta.status_code == 404


def test_actualizar_producto():
    client.post("/productos", json=PRODUCTO)
    nuevo = {**PRODUCTO, "stock": 80, "precio": 20.5}
    respuesta = client.put("/productos/PROD-001", json=nuevo)
    assert respuesta.status_code == 200
    assert client.get("/productos/PROD-001").json() == nuevo


def test_actualizar_producto_inexistente():
    respuesta = client.put("/productos/PROD-999", json=PRODUCTO)
    assert respuesta.status_code == 404


def test_eliminar_producto():
    client.post("/productos", json=PRODUCTO)
    respuesta = client.delete("/productos/PROD-001")
    assert respuesta.status_code == 200
    assert client.get("/productos/PROD-001").status_code == 404


def test_eliminar_producto_inexistente():
    respuesta = client.delete("/productos/PROD-999")
    assert respuesta.status_code == 404