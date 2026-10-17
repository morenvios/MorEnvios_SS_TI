import sqlite3

import pytest
from fastapi.testclient import TestClient

from almacen import app
from db import RUTA_DB
from migrar import migrar

client = TestClient(app)

SALIDA = {"producto_id": 6, "ubicacion_id": 1, "tipo": "salida", "cantidad": 5}


@pytest.fixture(autouse=True)
def base_limpia():
    migrar()


def contar_movimientos(producto_id):
    conexion = sqlite3.connect(RUTA_DB)
    total = conexion.execute(
        "SELECT COUNT(*) FROM movimiento WHERE producto_id = ?", (producto_id,)
    ).fetchone()[0]
    conexion.close()
    return total


def test_listar_primera_pagina():
    respuesta = client.get("/productos")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["total"] == 8
    assert [p["codigo"] for p in datos["items"]] == ["PROD-001", "PROD-002", "PROD-003"]


def test_ultima_pagina_incompleta():
    datos = client.get("/productos", params={"pagina": 3}).json()
    assert len(datos["items"]) == 2


def test_pagina_inexistente_devuelve_lista_vacia():
    respuesta = client.get("/productos", params={"pagina": 4})
    assert respuesta.status_code == 200
    assert respuesta.json()["items"] == []
    assert respuesta.json()["total"] == 8


def test_filtrar_por_categoria():
    datos = client.get("/productos", params={"categoria": "empaque"}).json()
    assert datos["total"] == 4


def test_pagina_cero_se_rechaza():
    respuesta = client.get("/productos", params={"pagina": 0})
    assert respuesta.status_code == 422


def test_stock_de_producto():
    respuesta = client.get("/productos/PROD-006/stock")
    assert respuesta.status_code == 200
    assert respuesta.json()["stock_total"] == 15


def test_stock_de_producto_inexistente():
    assert client.get("/productos/PROD-999/stock").status_code == 404


def test_salida_valida():
    respuesta = client.post("/movimientos", json=SALIDA)
    assert respuesta.status_code == 201
    assert respuesta.json()["cantidad_nueva"] == 10
    assert client.get("/productos/PROD-006/stock").json()["stock_total"] == 10


def test_salida_mayor_al_stock_se_rechaza_sin_cambiar_nada():
    respuesta = client.post("/movimientos", json={**SALIDA, "cantidad": 50})
    assert respuesta.status_code == 409
    assert client.get("/productos/PROD-006/stock").json()["stock_total"] == 15
    assert contar_movimientos(6) == 1


def test_entrada_en_ubicacion_nueva():
    entrada = {"producto_id": 6, "ubicacion_id": 2, "tipo": "entrada", "cantidad": 20}
    respuesta = client.post("/movimientos", json=entrada)
    assert respuesta.status_code == 201
    assert client.get("/productos/PROD-006/stock").json()["stock_total"] == 35


def test_movimiento_con_producto_inexistente():
    respuesta = client.post("/movimientos", json={**SALIDA, "producto_id": 99})
    assert respuesta.status_code == 404


@pytest.mark.parametrize(
    "cambio", [{"cantidad": 0}, {"cantidad": -5}, {"tipo": "robo"}]
)
def test_movimiento_invalido_se_rechaza(cambio):
    respuesta = client.post("/movimientos", json={**SALIDA, **cambio})
    assert respuesta.status_code == 422


def test_salida_de_producto_sin_existencia():
    respuesta = client.post("/movimientos", json={**SALIDA, "producto_id": 8})
    assert respuesta.status_code == 409

def test_listar_productos_incluye_id():
    datos = client.get("/productos").json()
    assert datos["items"][0]["id"] == 1