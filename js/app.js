let todosLosEnvios = [];
async function cargarEnvios() {
  try {
    const respuesta = await fetch('data/envios.json');

    if (!respuesta.ok) {
      throw new Error('No se pudo cargar el archivo de envíos');
    }

    const datos = await respuesta.json();
    todosLosEnvios = datos;

    mostrarEnvios(datos);
  } catch (error) {
    console.error(error);
    mostrarError();
  }
}

function mostrarError() {
  document.getElementById('total-envios').textContent = '';
  document.getElementById('costo-total').textContent = '';

  const cuerpoTabla = document.getElementById('cuerpo-tabla');
  cuerpoTabla.innerHTML = '<tr><td colspan="5">Error al cargar los envíos.</td></tr>';
}

function mostrarEnvios(envios) {
  const costoTotal = envios.reduce((acumulado, envio) => acumulado + Number(envio.costo ?? 0), 0);
  document.getElementById('total-envios').textContent = envios.length;
  document.getElementById('costo-total').textContent = costoTotal;

  const cuerpoTabla = document.getElementById('cuerpo-tabla');
  cuerpoTabla.innerHTML = '';
  if (envios.length === 0) {
  cuerpoTabla.innerHTML = '<tr><td colspan="5">No se encontraron envíos.</td></tr>';
  return;
}

  envios.forEach(envio => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${envio.id}</td>
      <td>${envio.cliente}</td>
      <td>${envio.destino}</td>
      <td>${envio.estado}</td>
      <td>${envio.costo !== undefined ? '$' + envio.costo : 'Sin costo'}</td>
    `;
    cuerpoTabla.appendChild(fila);
  });
}

function aplicarFiltros() {
  const estadoElegido = document.getElementById('filtro-estado').value;
  const texto = document.getElementById('buscar').value.toLowerCase();

  let resultado = todosLosEnvios;

  if (estadoElegido !== '') {
    resultado = resultado.filter(envio => envio.estado === estadoElegido);
  }

  if (texto !== '') {
    resultado = resultado.filter(envio => {
      return envio.id.toLowerCase().includes(texto)
        || envio.cliente.toLowerCase().includes(texto)
        || envio.destino.toLowerCase().includes(texto);
    });
  }

   const ordenElegido = document.getElementById('ordenar').value;

  if (ordenElegido === 'fecha') {
    resultado.sort((a, b) => a.fecha.localeCompare(b.fecha));
  }

  mostrarEnvios(resultado);
}

document.getElementById('filtro-estado').addEventListener('change', aplicarFiltros);
document.getElementById('buscar').addEventListener('input', aplicarFiltros);
document.getElementById('ordenar').addEventListener('change', aplicarFiltros);

cargarEnvios();