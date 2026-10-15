import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).parent / "almacen.db"


def ejecutar(titulo, sql, parametros=()):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    filas = conexion.execute(sql, parametros).fetchall()
    print(f"\n{titulo} ({len(filas)} filas)")
    for fila in filas:
        print("  ", dict(fila))
    conexion.close()


ejecutar("Todas las categorias", "SELECT * FROM categoria")

ejecutar(
    "Productos de mas de 20, del mas caro al mas barato",
    "SELECT codigo, nombre, precio FROM producto WHERE precio > 20 ORDER BY precio DESC",
)

ejecutar(
    "Productos cuyo nombre contiene 'carton'",
    "SELECT codigo, nombre FROM producto WHERE nombre LIKE ?",
    ("%carton%",),
)

ejecutar(
    "Productos con el nombre de su categoria",
    """
    SELECT p.codigo, p.nombre, c.nombre AS categoria
    FROM producto p
    JOIN categoria c ON c.id = p.categoria_id
    ORDER BY p.codigo
    """,
)

ejecutar(
    "Existencias por producto y ubicacion (JOIN)",
    """
    SELECT p.codigo, p.nombre, u.nombre AS ubicacion, e.cantidad
    FROM existencia e
    JOIN producto p ON p.id = e.producto_id
    JOIN ubicacion u ON u.id = e.ubicacion_id
    ORDER BY p.codigo, u.nombre
    """,
)

ejecutar(
    "Todos los productos con su cantidad (LEFT JOIN)",
    """
    SELECT p.codigo, p.nombre, e.cantidad
    FROM producto p
    LEFT JOIN existencia e ON e.producto_id = p.id
    ORDER BY p.codigo
    """,
)

ejecutar(
    "Productos sin ninguna existencia",
    """
    SELECT p.codigo, p.nombre
    FROM producto p
    LEFT JOIN existencia e ON e.producto_id = p.id
    WHERE e.producto_id IS NULL
    """,
)

ejecutar(
    "Stock total por producto (SUM)",
    """
    SELECT p.codigo, p.nombre, SUM(e.cantidad) AS stock_total
    FROM producto p
    JOIN existencia e ON e.producto_id = p.id
    GROUP BY p.codigo, p.nombre
    ORDER BY p.codigo
    """,
)

ejecutar(
    "Cantidad de productos por categoria (COUNT)",
    """
    SELECT c.nombre AS categoria, COUNT(*) AS total_productos
    FROM categoria c
    JOIN producto p ON p.categoria_id = c.id
    GROUP BY c.nombre
    ORDER BY c.nombre
    """,
)

for pagina in (1, 2, 3):
    ejecutar(
        f"Productos, pagina {pagina} (de 3 en 3)",
        "SELECT codigo, nombre FROM producto ORDER BY codigo LIMIT ? OFFSET ?",
        (3, (pagina - 1) * 3),
    )

    ejecutar(
    "Stock total por producto (SUM)",
    """
    SELECT p.codigo, p.nombre, SUM(e.cantidad) AS stock_total
    FROM producto p
    JOIN existencia e ON e.producto_id = p.id
    GROUP BY p.codigo, p.nombre
    ORDER BY p.codigo
    """,
)

ejecutar(
    "Cantidad de productos por categoria (COUNT)",
    """
    SELECT c.nombre AS categoria, COUNT(*) AS total_productos
    FROM categoria c
    JOIN producto p ON p.categoria_id = c.id
    GROUP BY c.nombre
    ORDER BY c.nombre
    """,
)