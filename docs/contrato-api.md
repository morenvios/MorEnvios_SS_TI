# Contrato de la API de inventario

API de inventario de MorEnvíos, construida con FastAPI. Este documento describe qué rutas tendrá la API, qué recibe cada una y qué devuelve. Se escribe antes de programar y sirve de guía para la implementación y las pruebas.

## Recurso: Producto

Un producto tiene los siguientes campos, todos obligatorios:

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| `id` | texto | Identificador único del producto | `"PROD-001"` |
| `nombre` | texto | Nombre del producto | `"Caja de cartón chica"` |
| `categoria` | texto | Categoría a la que pertenece | `"empaque"` |
| `precio` | número decimal | Precio unitario | `12.5` |
| `ubicacion` | texto | Lugar donde se almacena | `"Almacén A"` |
| `stock` | número entero | Unidades disponibles | `100` |

## Rutas

| Método | Ruta | Qué hace | Recibe | Éxito | Errores |
|---|---|---|---|---|---|
| GET | `/` | Mensaje de bienvenida | nada | 200 | |
| GET | `/productos` | Lista todos los productos | nada | 200 | |
| GET | `/productos/{id}` | Devuelve un producto | `id` en la ruta | 200 | 404 si no existe |
| POST | `/productos` | Crea un producto | JSON con los 6 campos | 201 | 422 datos inválidos, 409 si el `id` ya existe |
| PUT | `/productos/{id}` | Reemplaza un producto existente | `id` en la ruta + JSON completo | 200 | 404 si no existe, 422 datos inválidos |
| DELETE | `/productos/{id}` | Elimina un producto | `id` en la ruta | 200 | 404 si no existe |

## Códigos de estado usados

- **200**: la operación salió bien.
- **201**: el producto se creó correctamente.
- **404**: el producto solicitado no existe.
- **409**: conflicto, ya existe un producto con ese `id`.
- **422**: los datos enviados no son válidos (campo faltante o tipo incorrecto).

## Reglas de negocio (a implementar el miércoles)

- El `id` no puede repetirse.
- El `precio` no puede ser negativo.
- El `stock` no puede ser negativo.

## Ejemplo de producto (cuerpo JSON)

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

## Estado de implementación

- [x] `GET /`
- [x] `GET /productos`
- [x] `POST /productos` (responde 200; falta pasar a 201 y validar `id` repetido)
- [x] `GET /productos/{id}`
- [x] `PUT /productos/{id}`
- [x] `DELETE /productos/{id}`
