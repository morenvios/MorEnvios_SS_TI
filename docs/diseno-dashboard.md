# Diseño del dashboard de envíos

## Tema
Dashboard operativo de envíos de MorEnvíos (datos ficticios).

## Datos
Archivo: `data/envios.json`

| Campo | Descripción |
|---|---|
| id | Identificador único del envío |
| cliente | Nombre ficticio |
| destino | Ciudad de entrega |
| estado | pendiente, en_transito, entregado o retrasado |
| fecha | Fecha de envío |
| costo | Costo en pesos |

## Indicadores calculados
- Total de envíos
- Costo total

Se calculan sobre los envíos que se están mostrando (después de filtros y búsqueda).

## Estados de la interfaz
- Cargando
- Con datos
- Vacío (sin resultados)
- Error al cargar

## Boceto
(Aquí va el enlace a la imagen del boceto en Drive)