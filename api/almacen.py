from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from db import obtener_conexion
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de almacen")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class MovimientoNuevo(BaseModel):
    producto_id: int
    ubicacion_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int = Field(gt=0)

@app.get("/productos")
def listar_productos(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(3, ge=1, le=50),
    categoria: str | None = None,
    conexion=Depends(obtener_conexion),
):
    filtros = ""
    parametros = []
    if categoria is not None:
        filtros = "WHERE c.nombre = ?"
        parametros.append(categoria)

    total = conexion.execute(
        f"SELECT COUNT(*) FROM producto p JOIN categoria c ON c.id = p.categoria_id {filtros}",
        parametros,
    ).fetchone()[0]

    filas = conexion.execute(
        f"""
        SELECT p.codigo, p.nombre, p.precio, c.nombre AS categoria
        FROM producto p
        JOIN categoria c ON c.id = p.categoria_id
        {filtros}
        ORDER BY p.codigo
        LIMIT ? OFFSET ?
        """,
        parametros + [por_pagina, (pagina - 1) * por_pagina],
    ).fetchall()

    return {
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total": total,
        "items": [dict(fila) for fila in filas],
    }

@app.post("/movimientos", status_code=201)
def registrar_movimiento(mov: MovimientoNuevo, conexion=Depends(obtener_conexion)):
    producto = conexion.execute(
        "SELECT 1 FROM producto WHERE id = ?", (mov.producto_id,)
    ).fetchone()
    ubicacion = conexion.execute(
        "SELECT 1 FROM ubicacion WHERE id = ?", (mov.ubicacion_id,)
    ).fetchone()
    if producto is None or ubicacion is None:
        raise HTTPException(status_code=404, detail="Producto o ubicacion no encontrados")

    fila = conexion.execute(
        "SELECT cantidad FROM existencia WHERE producto_id = ? AND ubicacion_id = ?",
        (mov.producto_id, mov.ubicacion_id),
    ).fetchone()
    actual = fila["cantidad"] if fila else 0

    if mov.tipo == "salida" and mov.cantidad > actual:
        raise HTTPException(status_code=409, detail=f"Stock insuficiente: hay {actual}")

    with conexion:
        conexion.execute(
            "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) "
            "VALUES (?, ?, ?, ?)",
            (mov.producto_id, mov.ubicacion_id, mov.tipo, mov.cantidad),
        )
        if mov.tipo == "entrada":
            conexion.execute(
                "INSERT INTO existencia (producto_id, ubicacion_id, cantidad) "
                "VALUES (?, ?, ?) "
                "ON CONFLICT (producto_id, ubicacion_id) "
                "DO UPDATE SET cantidad = cantidad + excluded.cantidad",
                (mov.producto_id, mov.ubicacion_id, mov.cantidad),
            )
        else:
            conexion.execute(
                "UPDATE existencia SET cantidad = cantidad - ? "
                "WHERE producto_id = ? AND ubicacion_id = ?",
                (mov.cantidad, mov.producto_id, mov.ubicacion_id),
            )

    nueva = actual + mov.cantidad if mov.tipo == "entrada" else actual - mov.cantidad
    return {**mov.model_dump(), "cantidad_nueva": nueva}

@app.get("/productos/{codigo}/stock")
def stock_producto(codigo: str, conexion=Depends(obtener_conexion)):
    producto = conexion.execute(
        "SELECT id, nombre FROM producto WHERE codigo = ?", (codigo,)
    ).fetchone()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    filas = conexion.execute(
        """
        SELECT u.nombre AS ubicacion, e.cantidad
        FROM existencia e
        JOIN ubicacion u ON u.id = e.ubicacion_id
        WHERE e.producto_id = ?
        ORDER BY u.nombre
        """,
        (producto["id"],),
    ).fetchall()
    return {
        "codigo": codigo,
        "nombre": producto["nombre"],
        "stock_total": sum(f["cantidad"] for f in filas),
        "ubicaciones": [dict(f) for f in filas],
    }

@app.get("/ubicaciones")
def listar_ubicaciones(conexion=Depends(obtener_conexion)):
    filas = conexion.execute("SELECT id, nombre FROM ubicacion ORDER BY id").fetchall()
    return [dict(fila) for fila in filas]

@app.get("/tienda/catalogo")
def obtener_catalogo(conexion=Depends(obtener_conexion)):
    consulta = """
        SELECT 
            p.id, 
            p.codigo, 
            p.nombre, 
            p.precio, 
            COALESCE(SUM(e.cantidad), 0) AS stock_total
        FROM producto p
        LEFT JOIN existencia e ON p.id = e.producto_id
        GROUP BY p.id, p.codigo, p.nombre, p.precio
        ORDER BY p.id
    """
    filas = conexion.execute(consulta).fetchall()
    
    return [dict(fila) for fila in filas]

class ItemCarrito(BaseModel):
    producto_id: int
    cantidad: int

@app.post("/tienda/checkout", status_code=201)
def procesar_checkout(carrito: list[ItemCarrito], conexion=Depends(obtener_conexion)):
    # 1. Primera pasada: Validar que HAYA stock de TODO antes de tocar la base de datos
    for item in carrito:
        existencias = conexion.execute(
            "SELECT cantidad FROM existencia WHERE producto_id = ?",
            (item.producto_id,)
        ).fetchall()
        
        stock_total = sum(e["cantidad"] for e in existencias)
        
        if stock_total < item.cantidad:
            raise HTTPException(
                status_code=409, 
                detail=f"Stock insuficiente del producto ID {item.producto_id}. Solicitado: {item.cantidad}, Disponible: {stock_total}"
            )
            
    # 2. Segunda pasada: Si pasó la validación, ejecutamos la transacción
    with conexion:
        for item in carrito:
            # Buscamos de qué almacén descontar (el primero que tenga suficiente)
            existe = conexion.execute(
                "SELECT ubicacion_id FROM existencia WHERE producto_id = ? AND cantidad >= ? LIMIT 1",
                (item.producto_id, item.cantidad)
            ).fetchone()
            
            ubicacion_id = existe["ubicacion_id"]
            
            # Registrar el movimiento de salida
            conexion.execute(
                "INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES (?, ?, 'salida', ?)",
                (item.producto_id, ubicacion_id, item.cantidad)
            )
            
            # Descontar el stock
            conexion.execute(
                "UPDATE existencia SET cantidad = cantidad - ? WHERE producto_id = ? AND ubicacion_id = ?",
                (item.cantidad, item.producto_id, ubicacion_id)
            )
            
    return {"mensaje": "Compra procesada con éxito", "items_procesados": len(carrito)}