# Retrospectiva de la semana 5

Semana 5: SQL, modelado y API REST. Producto: API de almacén persistente.

> Borrador para ajustar en equipo. Es el balance del equipo, así que cada punto debe reflejar lo que de verdad pasó.

## Qué salió bien

- El esquema SQLite se reconstruye desde cero con `migrar.py` y las migraciones numeradas, así que la instalación es reproducible.
- Las restricciones (`NOT NULL`, `UNIQUE`, `CHECK` y claves foráneas) se comprobaron a propósito con datos inválidos antes de confiar en ellas.
- Las transacciones se demostraron con un caso real: sin transacción, una salida mayor al stock dejaba el movimiento guardado, y con transacción se deshacía todo.
- La auditoría (`auditar.py`) detectó una inconsistencia que las restricciones no ven (existencia 87 contra 80 del historial).
- En los issues #13 y #14 se escribió la prueba antes del cambio y se vio fallar, y después se hizo pasar.
- Los dos PR se revisaron de forma cruzada, ejecutando la rama del otro y probando a mano en `/docs`.

## Qué salió mal y qué aprendimos

| Problema | Causa | Qué aprendimos |
|---|---|---|
| Commits con el número de issue equivocado y la API de almacén sin subir en una de las ramas | Se hicieron commits sin revisar `git status` ni qué contenía cada uno | Revisar `git status` antes de cada commit y usar un commit por cambio lógico |
| Ramas con el número de un ejemplo (`fix/8-...`) | Se copió el comando sin cambiar el número | Cambiar siempre el número por el del issue propio |
| Rutas de Git que fallaban en una computadora | La carpeta se llama `API` en disco pero Git la registró como `api` | Ejecutar los comandos de Git desde la raíz del proyecto |
| Comandos pegados en bloque que se rompían en PowerShell | Una comilla sin cerrar | Pegar los comandos de uno en uno |
| `pytest` no encontrado | El entorno virtual no estaba activo | Comprobar que el prompt empiece con `(venv)` |
| Issues cerrados antes de que los PR estuvieran revisados | Se cerraron al abrir el PR | Cerrar el issue cuando el PR esté revisado y fusionado |
| Atraso de días respecto al calendario | Pendiente de analizar en equipo | Registrar horas y fechas reales en la bitácora |

## Decisiones técnicas

- **SQLite** en vez de PostgreSQL: viene con Python y simplifica la instalación.
- **Historial de movimientos:** se guarda, porque permite verificar el stock y sostiene las transacciones.
- **Clave primaria compuesta** en `existencia` (producto y ubicación), para impedir duplicados.
- Los detalles están en `requerimientos-almacen.md`, `diagrama-er.md` y `diccionario-de-datos.md`.

## Deuda técnica

- La API de almacén solo lista productos, consulta stock y registra movimientos. No permite crear ni editar productos, categorías o ubicaciones.
- `GET /movimientos` no tiene paginación.
- Los movimientos no se pueden anular; un error se corrige con un movimiento contrario.
- El precio se guarda como `REAL`, que puede tener pequeñas imprecisiones.
- Los PR de esta semana se fusionaron en las ramas de trabajo, no en `main`. El PR #6 de la semana 3 sigue abierto con conflictos.
- El despliegue en GitHub Pages sigue pendiente por permisos.
- Ejecutar `pytest` reconstruye la base de desarrollo, lo que obliga a no probar a mano al mismo tiempo.

## Plan de mejora para la semana 6

- Crear el issue y la rama al inicio de la semana, y abrir el PR a mitad de semana para revisarlo con tiempo.
- Un commit por cambio lógico, con el número del issue, y `git status` antes de cada commit.
- Pegar los comandos de uno en uno y confirmar `(venv)` antes de ejecutar nada.
- Hacer commit, push y bitácora el mismo día.
- Definir por escrito el stack y el alcance el lunes.
- Rotar los roles: nadie repite el de la semana anterior.
