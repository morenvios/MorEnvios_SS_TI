import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).parent / "almacen.db"


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_DB, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    try:
        yield conexion
    finally:
        conexion.close()