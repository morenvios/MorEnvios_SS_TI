# Guía Semana 2 — Sitio Corporativo
### Registro profesional de tareas · MorEnvíos SS_TI

> Antes de escribir código: copia el `<header>` y el `<footer>` completos de `index.html` en tu página, sin cambiar nada excepto el `aria-current="page"` en el link del menú que corresponda a tu página. Usa siempre las variables de `css/estilos.css` (colores, espaciados) — no inventes valores nuevos.

---

## Guía para Persona 2 — `nosotros.html`

### Objetivo
Contar quién es la empresa: misión, historia breve, valores. Es texto narrativo, no una lista de productos.

### Contenido a incluir
- Misión / visión (1-2 líneas cada una)
- Historia breve de la empresa (2-3 líneas)
- Valores (puede ser una lista corta)
- Opcional: cifras (años operando, municipios cubiertos, envíos realizados)

### Qué etiquetas usar (y por qué)
- Cada bloque de contenido (misión, historia, valores) va en su propio `<section>`, cada uno con su `<h2>` propio.
- Texto narrativo → `<p>`, no listas.
- Si pones cifras o datos sueltos (ej. "10 años", "15 municipios"), ahí sí una lista `<ul>` tiene sentido, porque son ítems independientes.

### Errores comunes a evitar
- Poner más de un `<h1>` en la página — solo debe haber uno, y normalmente es el título de la sección hero, no un título por cada bloque.
- Usar `<div>` en vez de `<section>` — pierdes el significado semántico que pide la rúbrica.
- Copiar el nombre del archivo CSS mal (`estilo.css` en vez de `estilos.css`) — revisa el `href` del `<link>` con cuidado.

### Checklist antes de avisar que terminaste
- [ ] `<title>` dice "Nosotros"
- [ ] Header y footer idénticos a `index.html`, con `aria-current="page"` en "Nosotros"
- [ ] Un solo `<h1>` en toda la página
- [ ] Probaste la página en 360px, 768px y 1440px (F12 → modo responsive) sin que nada se desborde
- [ ] `git add` → `git commit` → `git push origin [tu-rama]`

---

## Guía para Persona 3 — `contacto.html`

### Objetivo
Que alguien pueda escribirle a la empresa: formulario + datos de contacto directos.

### Contenido a incluir
- Formulario con: nombre, correo, mensaje (mínimo)
- Teléfono y dirección (datos directos, sin formulario)
- Opcional: zona de cobertura

### Qué etiquetas usar (y por qué)
- El formulario va en `<form>`.
- **Regla obligatoria:** cada campo necesita su `<label>` conectado al `<input>` mediante `for` (en el label) e `id` (en el input), y ambos deben ser **exactamente iguales**. Ejemplo de relación (no de código completo): `label for="nombre"` se conecta con `input id="nombre"`.
- Los datos de contacto directos (teléfono, correo, dirección) van dentro de `<address>` — es la etiqueta semántica correcta para esto, ya la usaste en el footer de `index.html`, es la misma idea.
- El botón de enviar el formulario es un `<button type="submit">`, no un link (`<a>`).

### Errores comunes a evitar
- Poner un `<input>` sin su `<label>` correspondiente — es el criterio de aceptación que más se olvida y el que más fácil se revisa.
- Que el `for` del label y el `id` del input no coincidan exactamente (ojo con mayúsculas/minúsculas y espacios).
- Usar `<div>` para los datos de contacto en vez de `<address>`.

### Checklist antes de avisar que terminaste
- [ ] `<title>` dice "Contacto"
- [ ] Header y footer idénticos a `index.html`, con `aria-current="page"` en "Contacto"
- [ ] Cada `<input>` tiene su `<label>` con `for`/`id` coincidentes
- [ ] Teléfono/dirección están dentro de `<address>`
- [ ] Probaste la página en 360px, 768px y 1440px sin que nada se desborde
- [ ] `git add` → `git commit` → `git push origin [tu-rama]`

---

## Recordatorio para los tres (viernes)

- Juntar los 3 hallazgos de accesibilidad en una sola matriz de pruebas.
- Revisar el Pull Request de un compañero cada quien.
- Preparar su defensa individual: qué decisión técnica tomaron y por qué.
- Desplegar en GitHub Pages y escribir el reporte breve de decisiones.
