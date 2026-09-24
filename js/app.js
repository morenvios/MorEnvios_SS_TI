async function cargarEnvios() {
  const respuesta = await fetch('data/envios.json');
  const datos = await respuesta.json();


  const costoTotal = datos.reduce((acumulado, envio) => acumulado + envio.costo, 0);
  document.getElementById('total-envios').textContent = datos.length;
  document.getElementById('costo-total').textContent = costoTotal;
  mostrarEnvios(datos);
}

function mostrarEnvios(envios) {
  const cuerpoTabla = document.getElementById('cuerpo-tabla');

  envios.forEach(envio => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${envio.id}</td>
      <td>${envio.cliente}</td>
      <td>${envio.destino}</td>
      <td>${envio.estado}</td>
      <td>$${envio.costo}</td>
    `;
    cuerpoTabla.appendChild(fila);
  });
}

cargarEnvios();