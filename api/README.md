# API de inventario - MorEnvíos

API REST construida con FastAPI para gestionar el inventario de productos de MorEnvíos. Permite crear, consultar, actualizar y eliminar productos, con validaciones y reglas de negocio.

Los datos se guardan **en memoria**: al reiniciar el servidor, el inventario queda vacío. Es una limitación esperada en esta etapa del proyecto.

## Requisitos

- Python 3.11 o superior
- Git

## Instalación

Desde la raíz del repositorio:

```
cd api
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

El entorno virtual (`venv`) no se sube a Git; cada persona crea el suyo con `requirements.txt`.

> Si PowerShell bloquea la activación, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Ejecutar el servidor

Con el entorno activado y dentro de la carpeta `api`:

```
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

## Producto

Todos los campos son obligatorios.

| Campo | Tipo | Regla |
|---|---|---|
| `id` | texto | único |
| `nombre` | texto | |
| `categoria` | texto | |
| `precio` | decimal | mayor o igual a 0 |
| `ubicacion` | texto | |
| `stock` | entero | mayor o igual a 0 |

Ejemplo:

```json
{
  "id": "PROD-001",
  "nombre": "Caja de cartón chica",
  "categoria": "empaque",
  "precio": 12.5,
  "ubicacion": "Almacén A",
  "stock": 100
}
```

## Rutas

| Método | Ruta | Qué hace | Éxito | Errores |
|---|---|---|---|---|
| GET | `/` | Mensaje de bienvenida | 200 | |
| GET | `/productos` | Lista todos los productos | 200 | |
| GET | `/productos/{id}` | Devuelve un producto | 200 | 404 si no existe |
| POST | `/productos` | Crea un producto | 201 | 409 `id` repetido, 422 datos inválidos |
| PUT | `/productos/{id}` | Reemplaza un producto | 200 | 404 si no existe, 422 datos inválidos |
| DELETE | `/productos/{id}` | Elimina un producto | 200 | 404 si no existe |

El detalle completo está en [`docs/contrato-api.md`](../docs/contrato-api.md).

## Reglas de negocio

- No se puede crear un producto con un `id` que ya existe (409).
- `precio` y `stock` no pueden ser negativos (422). El valor 0 sí es válido.

## Estructura

```
api/
├── main.py            # rutas: reciben la petición y delegan al servicio
├── servicio.py        # lista de productos y reglas de negocio
├── modelos.py         # modelo Producto y sus validaciones
├── test_api.py        # pruebas automáticas
└── requirements.txt   # dependencias
```

## Pruebas

Con el entorno activado y dentro de la carpeta `api`:

```
pytest
```

Las pruebas cubren las seis rutas, el rechazo de `id` repetido, los valores negativos y el valor límite (`stock` en 0). Cada prueba empieza con el inventario vacío.
