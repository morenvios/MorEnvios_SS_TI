import sqlite3
from pathlib import Path

from migrar import migrar

RUTA_DB = Path(__file__).parent / "almacen.db"


def conectar(**opciones):
    conexion = sqlite3.connect(RUTA_DB, **opciones)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def estado(conexion, titulo):
    cantidad = conexion.execute(
        "SELECT cantidad FROM existencia WHERE producto_id = 6 AND ubicacion_id = 1"
    ).fetchone()[0]
    movimientos = conexion.execute(
        "SELECT COUNT(*) FROM movimiento WHERE producto_id = 6"
    ).fetchone()[0]
    print(f"  {titulo}: cantidad = {cantidad}, movimientos de PROD-006 = {movimientos}")


def salida(conexion, producto_id, ubicacion_id, cantidad):
    conexion.execute(
        "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) "
        "VALUES (?, ?, 'salida', ?)",
        (producto_id, ubicacion_id, cantidad),
    )
    conexion.execute(
        "UPDATE existencia SET cantidad = cantidad - ? "
        "WHERE producto_id = ? AND ubicacion_id = ?",
        (cantidad, producto_id, ubicacion_id),
    )

    print("SIN transaccion")
migrar()
conexion = conectar(isolation_level=None)
estado(conexion, "Antes")
try:
    salida(conexion, 6, 1, 50)
except sqlite3.IntegrityError as error:
    print("  Error:", error)
estado(conexion, "Despues")
conexion.close()

print("CON transaccion")
migrar()
conexion = conectar()
estado(conexion, "Antes")
try:
    with conexion:
        salida(conexion, 6, 1, 50)
except sqlite3.IntegrityError as error:
    print("  Error:", error)
estado(conexion, "Despues")

print("Salida valida (5 unidades)")
with conexion:
    salida(conexion, 6, 1, 5)
estado(conexion, "Despues")
conexion.close()