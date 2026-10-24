# Matriz de Pruebas — MiniCommerce (Semana 6)

Documento de evidencia de las pruebas manuales realizadas el día jueves. El objetivo es validar la navegación, el estado del carrito, la accesibilidad, el diseño responsive y la integridad de la base de datos ante errores.

| ID | Caso de Prueba | Pasos para reproducir | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TP-01 | Persistencia del carrito | Agregar 3 productos distintos y recargar la página (F5). | El carrito y el total conservan los productos seleccionados. | El carrito mantiene los productos y sumas usando `localStorage`. |  Pasa |
| TP-02 | Validación de Stock (Fallo) | Modificar `localStorage` para pedir 500 cajas. Intentar comprar. | La API rechaza la compra (Error 409) y el stock no disminuye. | La API devuelve error de "Stock insuficiente", alerta en pantalla y la transacción no afecta la BD. |  Pasa |
| TP-03 | Flujo de compra exitoso | Agregar 2 productos con stock válido y finalizar compra. | El carrito se vacía, sale mensaje de éxito y el stock baja. | Compra exitosa (201 Created), carrito limpio y catálogo recargado. |  Pasa |
| TP-04 | Eliminación de carrito | Agregar un producto y hacer clic en la "X" roja. | El producto desaparece y el total vuelve a calcularse. | El producto se elimina del DOM y del `localStorage` correctamente. |  Pasa |
| TP-05 | Accesibilidad (Teclado) | Navegar por la página usando solo la tecla `Tab`. | El foco es visible en enlaces y botones de compra. | Los botones muestran el borde de foco verde definido en `style.css`. |  Pasa |
| TP-06 | Diseño Responsive | Abrir DevTools (F12) y simular pantalla de celular (360px). | Las tarjetas se apilan en una columna sin desbordarse. | El grid se adapta automáticamente, sin scroll horizontal. |  Pasa |