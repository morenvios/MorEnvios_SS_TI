# Retrospectiva — Semana 6: MiniCommerce

## 1. ¿Qué salió bien? (Aciertos)
*   **Decisión técnica:** Elegir reutilizar nuestra API de Python en lugar de aprender un stack nuevo como WooCommerce nos ahorró tiempo y nos permitió integrar el sistema de punta a punta.
*   **Diseño:** Logramos unificar la tienda con el diseño corporativo de la semana 2 (`style.css`), lo que demuestra reutilización de código y consistencia visual.
*   **Integridad de datos:** La base de datos está protegida. Cuando intentamos comprar más de lo que había, la transacción (Error 409) evitó que el inventario se corrompiera.
*   **Trabajo en equipo:** Logramos resolver los conflictos de Git y mantener nuestras ramas sincronizadas antes de los commits.

## 2. ¿Qué falló o fue difícil? (Deuda técnica)
*   **Configuración del entorno:** Tuvimos problemas al recrear el entorno virtual (`venv`) por bloqueos de permisos en Windows (Error 13).
*   **CORS:** Fue un reto entender por qué el navegador bloqueaba las peticiones hasta que configuramos el middleware en FastAPI.
*   **Rutas relativas:** Tuvimos errores con las rutas del HTML hacia el JS y el CSS (el archivo no se encontraba).

## 3. Plan de mejora (Para la Semana 7)
*   **Automatización:** Investigar cómo automatizar las pruebas de frontend para no depender de pruebas manuales.
*   **Documentación temprana:** Crear el manual de operación desde el primer día de la semana, en lugar de dejarlo para el final.
*   **Revisión de código:** Implementar una revisión cruzada (peer review) antes de hacer el `push` a GitHub para detectar errores de rutas o imports a tiempo.
