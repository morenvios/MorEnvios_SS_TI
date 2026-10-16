import sqlite3

from db import RUTA_DB


def revisar(titulo, sql):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    hallazgos = conexion.execute(sql).fetchall()
    conexion.close()
    estado = "OK" if not hallazgos else "PROBLEMA"
    print(f"{estado:9} {titulo} ({len(hallazgos)} hallazgos)")
    for fila in hallazgos:
        print("          ", dict(fila))


revisar("Claves foraneas validas", "PRAGMA foreign_key_check")

revisar("Sin cantidades negativas", "SELECT * FROM existencia WHERE cantidad < 0")

revisar(
    "Existencia coincide con el historial de movimientos",
    """
    SELECT m.producto_id, m.ubicacion_id,
           SUM(CASE m.tipo WHEN 'entrada' THEN m.cantidad ELSE -m.cantidad END)
               AS segun_movimientos,
           COALESCE(e.cantidad, 0) AS en_existencia
    FROM movimiento m
    LEFT JOIN existencia e
           ON e.producto_id = m.producto_id AND e.ubicacion_id = m.ubicacion_id
    GROUP BY m.producto_id, m.ubicacion_id, e.cantidad
    HAVING segun_movimientos != en_existencia
    """,
)

revisar(
    "Existencias con cantidad pero sin ningun movimiento",
    """
    SELECT e.producto_id, e.ubicacion_id, e.cantidad
    FROM existencia e
    LEFT JOIN movimiento m
           ON m.producto_id = e.producto_id AND m.ubicacion_id = e.ubicacion_id
    WHERE m.id IS NULL AND e.cantidad != 0
    """,
)