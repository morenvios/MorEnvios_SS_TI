const API_URL = "http://127.0.0.1:8000/tienda/catalogo";
const contenedor = document.getElementById("contenedor-productos");

async function cargarProductos() {
    try {
        const respuesta = await fetch(API_URL);
        
        if (!respuesta.ok) {
            throw new Error("Error al conectar con la API");
        }
        
        const productos = await respuesta.json();
        contenedor.innerHTML = "";

        productos.forEach(prod => {
            const tarjeta = document.createElement("div");
            tarjeta.className = "tarjeta";
            
            const sinStock = prod.stock_total === 0;
            const botonDeshabilitado = sinStock ? "disabled" : "";
            const textoBoton = sinStock ? "Sin stock" : "Agregar al carrito";

            tarjeta.innerHTML = `
                <div>
                    <h3>${prod.nombre}</h3>
                    <p style="color: #666; font-size: 0.9em;">Código: ${prod.codigo}</p>
                    <p>Precio: <span class="precio">$${prod.precio.toFixed(2)}</span></p>
                    <p>Disponibles: ${prod.stock_total}</p>
                </div>
                <button ${botonDeshabilitado}>
                    ${textoBoton}
                </button>
            `;
            contenedor.appendChild(tarjeta);
        });
        
    } catch (error) {
        contenedor.innerHTML = `<p style="color: red; font-weight: bold;">Error: ${error.message}. Asegúrate de que el servidor de Python esté corriendo.</p>`;
    }
}

cargarProductos();