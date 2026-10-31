# Arquitectura de SmartCommerce — MorEnvíos

Este documento describe la arquitectura del sistema, mostrando la integración del frontend, el backend y los servicios externos de Inteligencia Artificial.

## 1. Diagrama de Arquitectura

```mermaid
graph TD
    A[Usuario / Navegador] -->|1. Pide catálogo o busca| B(Frontend: HTML/JS/CSS)
    B -->|2. Petición HTTP REST (Fetch)| C{Backend: FastAPI (Python)}
    C -->|3. Consulta de productos| D[(Base de Datos: SQLite)]
    C -->|4. Envía prompt al Asistente| E[OpenAI API]
    E -.->|5a. Respuesta exitosa| C
    E -.->|5b. Error / Sin saldo| F[Fallback: Búsqueda SQL tradicional]
    F --> D
    D -->|6. Devuelve datos JSON| C
    C -->|7. Respuesta JSON| B
    B -->|8. Renderiza productos| A
```