# Plan de Riesgos Residuales — Semana 7

A pesar de las correcciones aplicadas durante la auditoría (CORS, validación de entrada, XSS, dependencias y ocultamiento de Swagger), el sistema presenta los siguientes riesgos que deben ser atendidos en futuras iteraciones (Semana 8).

| ID | Riesgo Residual | Impacto | Mitigación Futura (Semana 8) |
| :--- | :--- | :--- | :--- |
| RR-01 | **Ausencia de Autenticación:** Cualquier persona con la URL puede hacer un POST al checkout o modificar inventario. | Alto | Implementar JWT (JSON Web Tokens) o al menos una API Key para los endpoints de escritura. |
| RR-02 | **Falta de Rate Limiting:** Un atacante podría saturar la API con miles de peticiones por segundo (DDoS). | Medio | Usar un middleware de FastAPI (como `slowapi`) para limitar peticiones por IP. |
| RR-03 | **Dependencia de SQLite:** SQLite no soporta múltiples usuarios concurrentes de forma robusta. | Medio | Migrar a PostgreSQL o MySQL para el entorno de producción real. |
| RR-04 | **Exposición de datos en LocalStorage:** El carrito guarda información del producto en texto plano en el navegador. | Bajo | Encriptar los datos del carrito o usar cookies HttpOnly con sesiones en el servidor. |