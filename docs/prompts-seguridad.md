# Registro de Prompts Sanitizados (Semana 7)

Este documento registra el uso de IA para auditoría, demostrando la aplicación de técnicas de sanitización para no exponer datos internos.

## Ejercicio 1: Revisión de consulta SQL

###  Prompt Inseguro (Lo que NO se hace)
> "Hola ChatGPT, tengo esta consulta en mi archivo `S:\Descargas\MorEnvios_SS_TI\api\almacen.py`. Me da un error de stock. Mi usuario de base de datos es admin y la contraseña es root123. Aquí está el código con los datos reales de mi cliente:
> `INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES (1, 1, 'salida', 20);`
> ¿Por qué falla?"

*(Problemas: Expone ruta local, credenciales de BD y un ID real de su sistema).*

###  Prompt Sanitizado (El correcto)
> "Actúa como un experto en bases de datos SQLite. Estoy construyendo una API para un sistema de inventario. Necesito revisar la lógica de una consulta que registra un movimiento de salida y resta stock de una tabla llamada `existencia`. El código es ficticio:
> `INSERT INTO movimientos (prod_id, loc_id, tipo, cant) VALUES (?, ?, 'salida', ?);`
> `UPDATE existencia SET cantidad = cantidad - ? WHERE prod_id = ? AND loc_id = ?;`

*(Ventajas: No expone rutas, no hay credenciales, los nombres de las tablas son genéricos o ficticios, y el enfoque es aprender la lógica, no que la IA escriba el código por mí).*
