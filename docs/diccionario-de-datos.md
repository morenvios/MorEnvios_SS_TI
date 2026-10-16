# Diccionario de datos del almacén

Describe cada tabla y columna de la base de datos `almacen.db` (SQLite), con su tipo, si admite nulos, sus restricciones y por qué se eligieron así. El esquema completo está en `api/migraciones/` y el diagrama en [`diagrama-er.md`](diagrama-er.md).

Todos los datos de ejemplo son ficticios.

## Convenciones

- **PK:** clave primaria. **FK:** clave foránea. **UK:** valor único.
- SQLite no tiene tipo de fecha propio: `fecha` se guarda como texto en UTC.
- Todas las claves foráneas usan `ON DELETE RESTRICT`: no se puede borrar un registro que otro todavía referencia (RI-05). Se hacen cumplir con `PRAGMA foreign_keys = ON`, que la API activa en cada conexión.

## categoria

Agrupa los productos (por ejemplo, empaque o etiquetado).

| Columna | Tipo | Nulo | Restricciones | Descripción | Justificación |
|---|---|---|---|---|---|
| `id` | INTEGER | No | PK | Identificador técnico, se numera solo | Identifica la fila sin depender del nombre, que podría cambiar |
| `nombre` | TEXT | No | UK | Nombre de la categoría | Una categoría sin nombre no tiene sentido; único para evitar duplicados como "Empaque" y "empaque" |

## ubicacion

Lugar físico donde se almacena un producto (por ejemplo, Almacen A).

| Columna | Tipo | Nulo | Restricciones | Descripción | Justificación |
|---|---|---|---|---|---|
| `id` | INTEGER | No | PK | Identificador técnico | Igual que en `categoria` |
| `nombre` | TEXT | No | UK | Nombre de la ubicación | Obligatorio y único, por la misma razón que el nombre de categoría |

## producto

Artículo del catálogo del almacén. No guarda cuánto hay: eso vive en `existencia`.

| Columna | Tipo | Nulo | Restricciones | Descripción | Justificación |
|---|---|---|---|---|---|
| `id` | INTEGER | No | PK | Identificador técnico | Separa la identidad de la fila del código de negocio |
| `codigo` | TEXT | No | UK | Código del producto, por ejemplo `PROD-001` | Único por RI-01. No es la PK porque un código de negocio puede cambiar de formato |
| `nombre` | TEXT | No | | Nombre descriptivo | Un producto sin nombre no se puede identificar en un listado |
| `precio` | REAL | No | CHECK (precio >= 0) | Precio unitario | Obligatorio y no negativo (RI-02). El cero se permite |
| `categoria_id` | INTEGER | No | FK a `categoria(id)` | Categoría a la que pertenece | Obligatorio porque cada producto pertenece a una categoría (RF-02) |

## existencia

Cantidad de un producto en una ubicación concreta. Es la tabla intermedia de la relación muchos a muchos entre `producto` y `ubicacion` (RF-04).

| Columna | Tipo | Nulo | Restricciones | Descripción | Justificación |
|---|---|---|---|---|---|
| `producto_id` | INTEGER | No | PK compuesta, FK a `producto(id)` | Producto almacenado | Forma la clave junto con `ubicacion_id` |
| `ubicacion_id` | INTEGER | No | PK compuesta, FK a `ubicacion(id)` | Lugar donde está | La pareja (producto, ubicación) impide tener dos filas del mismo producto en el mismo lugar |
| `cantidad` | INTEGER | No | CHECK (cantidad >= 0), DEFAULT 0 | Unidades disponibles | No puede ser negativa (RI-02). Empieza en 0 al crear la fila, y 0 es un valor válido (producto agotado) |

La clave primaria compuesta se declara también `NOT NULL` en cada columna, porque SQLite permite nulos en claves compuestas si no se prohíben.

## movimiento

Historial de entradas y salidas. Cada fila es un hecho que ocurrió y no se modifica.

| Columna | Tipo | Nulo | Restricciones | Descripción | Justificación |
|---|---|---|---|---|---|
| `id` | INTEGER | No | PK | Identificador técnico | Un mismo producto puede tener muchos movimientos en la misma ubicación, así que la pareja no sirve como clave |
| `producto_id` | INTEGER | No | FK a `producto(id)` | Producto que se movió | Un movimiento sin producto no significa nada |
| `ubicacion_id` | INTEGER | No | FK a `ubicacion(id)` | Ubicación afectada | Igual que el producto |
| `tipo` | TEXT | No | CHECK (tipo IN ('entrada', 'salida')) | Sentido del movimiento | Lista cerrada de valores: evita datos como `'robo'` o `'Entrada '` |
| `cantidad` | INTEGER | No | CHECK (cantidad > 0) | Unidades que entran o salen | Siempre positiva: el sentido lo da `tipo`. Una cantidad de cero no sería un movimiento |
| `fecha` | TEXT | No | DEFAULT CURRENT_TIMESTAMP | Momento del registro, en UTC | Se llena sola, para que no dependa de quien llama a la API |

## Invariantes entre tablas

Estas condiciones no las puede imponer una restricción de columna, y las comprueba `api/auditar.py`:

- Para cada producto y ubicación, `existencia.cantidad` es igual a la suma de sus entradas menos la suma de sus salidas en `movimiento`.
- No hay existencias con cantidad distinta de cero sin movimientos que la respalden.
- Ninguna clave foránea apunta a una fila que no existe.

## Reglas de integridad y dónde se cumplen

| Regla | Mecanismo |
|---|---|
| RI-01 El código de producto no se repite | UK en `producto.codigo` |
| RI-02 Precio y cantidad no negativos | CHECK en `producto.precio` y `existencia.cantidad` |
| RI-03 Una salida mayor al stock se rechaza | La API responde 409 antes de escribir; el CHECK de `existencia` es la última defensa |
| RI-04 Movimiento y existencia cambian juntos o ninguno | Transacción en `POST /movimientos` |
| RI-05 No se borra lo que tiene dependencias | FK con `ON DELETE RESTRICT` |
