# API de MorEnvíos

Esta carpeta contiene dos APIs hechas con FastAPI:

| API | Archivo | Datos | Semana |
|---|---|---|---|
| Inventario | `main.py` | en memoria (se pierden al reiniciar) | 4 |
| Almacén | `almacen.py` | base de datos SQLite (persisten) | 5 |

Los datos de ejemplo son ficticios.

## Requisitos

- Python 3.11 o superior
- Git

SQLite viene incluido con Python: no hay que instalar ni configurar ningún servidor de base de datos.

## Instalación

Desde la raíz del repositorio:

```
cd api
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## API de almacén (semana 5)

### Crear la base de datos

```
python migrar.py
```

Borra `almacen.db` si existe, ejecuta en orden los archivos de `migraciones/` y carga los datos semilla. Al final imprime las tablas creadas y cuántas filas tiene cada una. El archivo `almacen.db` no se sube a Git: se regenera siempre con este comando.

### Ejecutar el servidor

```
uvicorn almacen:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

La API de inventario de la semana 4 usa el mismo puerto (`uvicorn main:app --reload`), así que no se ejecutan al mismo tiempo.

### Rutas

| Método | Ruta | Qué hace | Éxito | Errores |
|---|---|---|---|---|
| GET | `/productos` | Lista productos (con su `id`), con paginación y filtro opcional por categoría | 200 | 422 parámetros inválidos |
| GET | `/ubicaciones` | Lista las ubicaciones con su `id` y su nombre | 200 | |
| GET | `/productos/{codigo}/stock` | Stock total y por ubicación de un producto | 200 | 404 si no existe |
| POST | `/movimientos` | Registra una entrada o salida y actualiza la existencia | 201 | 404 producto o ubicación inexistentes, 409 stock insuficiente, 422 datos inválidos |

Parámetros de `GET /productos`:

| Parámetro | Tipo | Valor por defecto | Regla |
|---|---|---|---|
| `pagina` | entero | 1 | mínimo 1 |
| `por_pagina` | entero | 3 | entre 1 y 50 |
| `categoria` | texto | sin filtro | nombre exacto de la categoría |

Una página que no existe devuelve `items: []`, no un error.

Ejemplo de cuerpo para `POST /movimientos`:

Los `id` que pide este cuerpo se consultan con `GET /productos` (campo `id` de cada producto) y `GET /ubicaciones`.

```json
{"producto_id": 6, "ubicacion_id": 1, "tipo": "salida", "cantidad": 5}
```

`tipo` solo admite `entrada` o `salida`, y `cantidad` debe ser mayor que 0.

### Modelo de datos

Cinco tablas: `categoria`, `ubicacion`, `producto`, `existencia` (cantidad de un producto en una ubicación) y `movimiento` (historial de entradas y salidas). El diagrama está en [`../docs/diagrama-er.md`](../docs/diagrama-er.md) y los requerimientos en [`../docs/requerimientos-almacen.md`](../docs/requerimientos-almacen.md).

### Reglas de integridad

| Regla | Dónde se hace cumplir |
|---|---|
| El código de producto no se repite | `UNIQUE` en `producto.codigo` |
| Precio y cantidad no pueden ser negativos | `CHECK` en la base |
| Una salida mayor al stock se rechaza | la API responde 409 antes de escribir; el `CHECK` de `existencia` es la última defensa |
| Movimiento y existencia cambian juntos o ninguno cambia | transacción (`with conexion:`) |
| No se borra una categoría, producto o ubicación con dependencias | claves foráneas con `ON DELETE RESTRICT` |

### Auditoría

```
python auditar.py
```

Comprueba que las claves foráneas sean válidas, que no haya cantidades negativas, que cada existencia coincida con la suma de sus entradas menos sus salidas, y que ninguna cantidad exista sin movimientos que la respalden. Cada revisión imprime `OK` o `PROBLEMA`.

### Otros scripts

| Script | Para qué sirve |
|---|---|
| `consultar.py` | Consultas SQL de ejemplo: filtros, joins, resúmenes y paginación |
| `transacciones.py` | Demuestra qué pasa con y sin transacción cuando una operación falla |
| `probar_restricciones.py` | Intenta insertar datos inválidos y muestra cómo los rechaza la base |

## Pruebas

```
pytest
```

Ejecuta las pruebas de las dos APIs. Las de `test_almacen.py` reconstruyen `almacen.db` antes de cada prueba, por lo que **borran los cambios hechos a mano en la base de desarrollo**: no las ejecutes mientras pruebas el servidor.

## Estructura

```
api/
├── main.py                   # API de inventario (semana 4)
├── modelos.py                # modelo Producto (semana 4)
├── servicio.py               # lógica del inventario en memoria (semana 4)
├── almacen.py                # API de almacén (semana 5)
├── db.py                     # conexión a SQLite por petición
├── migrar.py                 # reconstruye la base desde cero
├── migraciones/              # esquema y datos semilla, en orden
├── auditar.py                # auditoría de integridad
├── consultar.py              # consultas de ejemplo
├── transacciones.py          # demostración de transacciones
├── probar_restricciones.py   # prueba de restricciones
├── test_api.py               # pruebas de la API de inventario
├── test_almacen.py           # pruebas de la API de almacén
└── requirements.txt          # dependencias
```

## Limitaciones conocidas

- La API de almacén solo lista productos, consulta stock y registra movimientos. No tiene rutas para crear o editar productos, categorías ni ubicaciones: esos datos vienen de la semilla.
- Los movimientos no se pueden anular ni editar. Un error se corrige con un movimiento contrario.
- El precio se guarda como número decimal (`REAL`), que puede tener pequeñas imprecisiones. Un sistema con dinero real guardaría centavos como enteros.
- SQLite trae las claves foráneas apagadas por defecto. La API las activa en cada conexión con `PRAGMA foreign_keys = ON`; una conexión externa que no lo haga no las hará cumplir.
- No hay autenticación ni registro de quién hizo cada movimiento.
- Un `UPDATE` directo a la base puede dejarla inconsistente sin violar ninguna restricción. `auditar.py` existe para detectarlo.
- Las pruebas de `test_almacen.py` dependen de `migrar.py` y de los datos semilla.
