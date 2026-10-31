# Retrospectiva Final — Programa MorEnvíos (Semanas 1 a 8)

## 1. ¿Qué logramos?
*   **Crecimiento técnico:** Pasamos de hacer HTML básico a construir una arquitectura completa (Frontend, Backend en Python, Base de datos SQL y consumo de APIs de IA).
*   **Trabajo en equipo:** Aprendimos a resolver conflictos en Git, a revisar el código del otro (peer review) y a documentar cada decisión. El sistema no depende de una sola persona.
*   **Resiliencia:** Aprendimos a diseñar sistemas tolerantes a fallos (el *fallback* de la IA nos salvó de quedar sin saldo).
*   **Mentalidad de seguridad:** Ya no vemos el código solo para que "funcione", sino para que sea seguro (mitigando XSS, inyecciones y exponiendo menos datos).

## 2. ¿Qué fue lo más difícil? (Deuda y retos)
*   **La curva de la Inteligencia Artificial:** Entender cómo estructurar el *prompt* y qué hacer si la API externa falla fue un reto, pero la solución del *fallback* con SQL nos enseñó mucho.
*   **El manejo de entornos:** Lidiar con las variables de entorno, los bloqueos de Windows con los entornos virtuales (`venv`) y los problemas de CORS nos costaron tiempo, pero ahora sabemos diagnosticarlos en minutos.
*   **Control de versiones:** Las ramas, los *cherry-picks* y los conflictos fueron complejos, pero el flujo de trabajo ahora es profesional.

## 3. Plan de mejora (Para la vida profesional)
*   Implementar pruebas automatizadas (como `pytest`) desde el primer día de cualquier proyecto nuevo.
*   Documentar la arquitectura antes de escribir la primera línea de código.
*   Mantener siempre un plan de riesgos y un *fallback* en cualquier servicio de terceros que usemos.

## 4. Conclusión
Terminamos el servicio social con un sistema funcional (SmartCommerce) que integra IA de forma segura, documentada y sobre todo, **reproducible**. Estamos listos para el proyecto real.