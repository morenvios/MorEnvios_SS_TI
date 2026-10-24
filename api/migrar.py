import sqlite3
from pathlib import Path

CARPETA = Path(__file__).parent
RUTA_DB = CARPETA / "almacen.db"
MIGRACIONES = CARPETA / "migraciones"


def migrar():
    if RUTA_DB.exists():
        RUTA_DB.unlink()
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("PRAGMA foreign_keys = ON")
    for archivo in sorted(MIGRACIONES.glob("*.sql")):
        conexion.executescript(archivo.read_text(encoding="utf-8"))
    tablas = conexion.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    print("Tablas creadas:", [t[0] for t in tablas])
    for (tabla,) in tablas:
        total = conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        print(f"  {tabla}: {total} filas")
    conexion.close()


if __name__ == "__main__":
    migrar()