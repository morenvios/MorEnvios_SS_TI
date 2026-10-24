# Manual de Operación y Arquitectura — MiniCommerce MorEnvíos

## 1. Arquitectura del Sistema
El proyecto MiniCommerce está construido bajo una arquitectura cliente-servidor:
*   **Backend (Servidor):** Python con FastAPI. Se encarga de la lógica de negocio, validación de stock y transacciones con la base de datos.
*   **Base de Datos:** SQLite (relacional). Almacena el catálogo, existencias por almacén y el historial de movimientos.
*   **Frontend (Cliente):** HTML5, CSS3 (con el sistema de diseño corporativo) y JavaScript puro (Vanilla JS). Consume la API mediante `fetch` y utiliza `localStorage` para persistir el carrito de compras en el navegador.

## 2. Requisitos Previos
*   Python 3.10 o superior.
*   Entorno virtual de Python (`venv`).
*   Extensiones recomendadas para VS Code: Live Server.

## 3. Guía de Instalación y Ejecución Local
Sigue estos pasos para levantar el proyecto desde cero:

1. Clonar el repositorio y acceder a la carpeta de la API:
   ```bash
   git clone <url-del-repositorio>
   cd MorEnvios_SS_TI/api