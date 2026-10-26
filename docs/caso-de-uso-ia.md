# Caso de Uso de IA — SmartCommerce (Semana 8)

## 1. Función de IA elegida
  Asistente de Búsqueda Inteligente en el catálogo.

## 2. ¿Qué problema resuelve? (Medible)
Los clientes que no conocen los términos técnicos del empaque (ej. "necesito algo para que no se rompa") no encuentran los productos adecuados. La IA traducirá esa necesidad a palabras clave técnicas (ej. "plástico burbuja", "esquineros") y devolverá los 3 productos más recomendados.
*Métrica de éxito:* Reducir la búsqueda fallida y devolver recomendaciones en menos de 5 segundos.

## 3. Riesgos Identificados
*   **Alucinación:** La IA podría recomendar productos que no existen en el catálogo. *Mitigación:* El backend de Python siempre validará contra la base de datos SQLite que el producto recomendado realmente exista.
*   **Caída de la API de OpenAI (o falta de saldo):** *Mitigación:* Implementar un *Fallback*. Si la IA falla, el sistema hará una búsqueda tradicional usando `LIKE` en SQL para devolver los productos.

## 4. Métrica de Evaluación
¿Cómo sabremos si funciona?
*   Prueba 1: "Quiero proteger cosas frágiles" -> Debería recomendar "Plástico burbuja".
*   Prueba 2: "Necesito sellar cajas" -> Debería recomendar "Cinta adhesiva".
*   Prueba 3: "Que no se mueva lo de adentro" -> Debería recomendar "Esquineros" o "Relleno".
