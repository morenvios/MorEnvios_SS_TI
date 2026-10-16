import sqlite3

conexion = sqlite3.connect("almacen.db")
conexion.execute("PRAGMA foreign_keys = ON")


def intentar(descripcion, sql):
    try:
        conexion.execute(sql)
        print("OK        ", descripcion)
    except sqlite3.IntegrityError as error:
        print("RECHAZADO ", descripcion, "->", error)


intentar("crear categoria", "INSERT INTO categoria (nombre) VALUES ('empaque')")
intentar("crear ubicacion", "INSERT INTO ubicacion (nombre) VALUES ('Almacen A')")
intentar(
    "crear producto",
    "INSERT INTO producto (codigo, nombre, precio, categoria_id) VALUES ('P-1', 'Caja', 10, 1)",
)
intentar(
    "existencia con cantidad negativa",
    "INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES (1, 1, -3)",
)
intentar(
    "existencia valida",
    "INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES (1, 1, 50)",
)
intentar(
    "existencia repetida (mismo producto y ubicacion)",
    "INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES (1, 1, 20)",
)
intentar(
    "existencia de un producto inexistente",
    "INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES (99, 1, 5)",
)
intentar(
    "movimiento con tipo invalido",
    "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES (1, 1, 'robo', 5)",
)
intentar(
    "movimiento con cantidad cero",
    "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES (1, 1, 'entrada', 0)",
)
intentar(
    "movimiento valido",
    "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES (1, 1, 'entrada', 10)",
)
intentar("borrar ubicacion con existencias", "DELETE FROM ubicacion WHERE id = 1")

conexion.close()