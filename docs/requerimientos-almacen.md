# Requerimientos de la API de almacén

Semana 5: SQL + modelado + API REST. Producto: API de almacén persistente.

> Borrador para ajustar en equipo. Todo dato es ficticio.

## Contexto

La API de inventario de la semana 4 guarda los productos en una lista en memoria: al reiniciar el servidor, se pierde todo. El almacén necesita guardar sus datos en una base de datos relacional, mantener su integridad y consultarlos con filtros y paginación.

## Requerimientos funcionales

| Código | Requerimiento |
|---|---|
| RF-01 | El sistema registra productos con código, nombre, precio y categoría. |
| RF-02 | Cada producto pertenece a una sola categoría; una categoría agrupa muchos productos. |
| RF-03 | El almacén tiene varias ubicaciones (por ejemplo, Almacén A y Almacén B). |
| RF-04 | Un producto puede estar en más de una ubicación, con su propia cantidad en cada una. |
| RF-05 | Se pueden registrar movimientos de inventario: entradas y salidas de un producto en una ubicación. |
| RF-06 | Se pueden consultar productos con filtros (por categoría, por ubicación) y paginación. |
| RF-07 | Se puede consultar el stock total de un producto sumando todas sus ubicaciones. |

## Reglas de integridad

| Código | Regla |
|---|---|
| RI-01 | No pueden existir dos productos con el mismo código. |
| RI-02 | El precio y la cantidad en una ubicación nunca pueden ser negativos. |
| RI-03 | Una salida mayor a la cantidad disponible se rechaza sin cambiar ningún dato. |
| RI-04 | Un movimiento registrado actualiza la cantidad de esa ubicación, o ninguna de las dos cosas ocurre. |
| RI-05 | No se puede eliminar una categoría ni una ubicación que todavía tenga productos. |

## Criterios de aceptación del programa

- PK, FK, nulabilidad y unicidad justificadas.
- No se corrompe el inventario ante una operación inválida.
- La instalación se reproduce con las instrucciones del README.

## Preguntas abiertas (a decidir en equipo)


- ¿Se necesita registrar quién hizo cada movimiento?
R: Si para registrar movimientos/modificaciones
- ¿Un producto puede cambiar de categoría con el tiempo?
R:Probablemente si
