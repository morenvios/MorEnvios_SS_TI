# Matriz de Pruebas — Sitio Corporativo MorEnvíos
### Semana 2 · Responsive + Accesibilidad

---

## 1. Matriz de pruebas responsive (360px / 768px / 1440px)

| Página | 360px | 768px | 1440px | Observaciones |
|---|---|---|---|---|
| `index.html` |  Sin desbordamientos |  Sin desbordamientos |  Grid de tarjetas se expande a 4 columnas | — |
| `servicios.html` |  Sin desbordamientos |  Sin desbordamientos |  Grid de tarjetas se expande a 4 columnas | — |
| `nosotros.html` |  Sin desbordamientos |  Sin desbordamientos |  Grids se expanden correctamente | — |
| `contacto.html` |  Sin desbordamientos |  Sin desbordamientos |  Formulario se mantiene angosto (max-width intencional) | El formulario no se estira a todo el ancho por legibilidad — comportamiento esperado, no es un bug |

**Metodología:** DevTools (F12) → modo responsive → se probó cada página fijando el ancho exacto en 360px, 768px y 1440px, revisando scroll horizontal, encimado de elementos y legibilidad del texto.

---

## 2. Checklist de accesibilidad

| Criterio | Estado | Detalle |
|---|---|---|
| Un solo `<h1>` por página | X | Confirmado en las 4 páginas |
| HTML semántico (`header`, `nav`, `main`, `section`, `footer`) | X | Estructura consistente en las 4 páginas |
| Foco visible en enlaces/botones (`:focus-visible`) | X | Definido globalmente en `estilos.css` |
| Todos los campos de formulario con `<label>` | X | Verificado en `contacto.html`: 5/5 campos con `for`/`id` coincidentes |
| Enlace "Saltar al contenido" | X | Presente en las 4 páginas |
| `aria-current="page"` en el link activo del menú | X | Verificado en las 4 páginas |
| `aria-labelledby` apunta a un `id` existente | X | Se corrigió un caso en `nosotros.html` donde apuntaba a un id inexistente |
| Contraste de color (WCAG AA, mínimo 4.5:1 texto normal) | X | Se detectó que el botón (`.boton`, verde claro `#00A44F`) tenía contraste insuficiente (3.27:1). Corregido usando `--color-verde-oscuro` (5.46:1) |
| Texto alternativo en imágenes | N/A | El sitio no usa imágenes en esta versión |

---

## 3. Hallazgos y correcciones aplicadas

- **Contraste de botón:** el verde original del botón principal no cumplía el mínimo de accesibilidad para texto blanco encima. Se corrigió usando el tono más oscuro de la misma paleta.
- **`aria-labelledby` roto en `nosotros.html`:** una sección apuntaba a un `id` que no existía en el `<h2>` correspondiente. Corregido.
- **Footer inconsistente en `nosotros.html`:** no coincidía con el de las otras 3 páginas. Corregido para mantener consistencia en todo el sitio.
- **Formulario sin contenedor en `contacto.html`:** faltaba el `<div class="contenedor">`, causando que el contenido se viera pegado al borde izquierdo sin centrar. Corregido.

---

## 4. Conclusión

Las 4 páginas cumplen los criterios de aceptación de la semana: HTML semántico, navegación completa, sin desbordamientos en los 3 anchos probados, contraste adecuado, foco visible y formularios etiquetados correctamente.
