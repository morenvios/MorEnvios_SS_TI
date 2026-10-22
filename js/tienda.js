const API_URL = "http://127.0.0.1:8000/tienda/catalogo";
const contenedor = document.getElementById("contenedor-productos");

let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

async function cargarProductos() {
    try {
        const respuesta = await fetch(API_URL);
        if (!respuesta.ok) throw new Error("Error al conectar con la API");
        
        const productos = await respuesta.json();
        contenedor.innerHTML = ""; 

        productos.forEach(prod => {
            const tarjeta = document.createElement("div");
            tarjeta.className = "tarjeta";
            
            const sinStock = prod.stock_total === 0;
            const botonDeshabilitado = sinStock ? "disabled" : "";
            const textoBoton = sinStock ? "Sin stock" : "Agregar al carrito";

            tarjeta.innerHTML = `
                <h3>${prod.nombre}</h3>
                <p style="font-size: 0.9em; color: var(--color-texto-suave);">Código: ${prod.codigo}</p>
                <p>Precio: <strong style="color: var(--color-verde);">$${prod.precio.toFixed(2)}</strong></p>
                <p>Disponibles: ${prod.stock_total}</p>
                <button class="boton" onclick="agregarAlCarrito(${prod.id}, '${prod.nombre}', ${prod.precio}, ${prod.stock_total})" ${botonDeshabilitado} style="width: 100%; margin-top: var(--esp-2);">
                    ${textoBoton}
                </button>
            `;
            contenedor.appendChild(tarjeta);
        });
    } catch (error) {
        contenedor.innerHTML = `<p style="color: red;">Error: ${error.message}. Verifica que uvicorn esté corriendo.</p>`;
    }
}

function agregarAlCarrito(id, nombre, precio, stockTotal) {
    const productoExistente = carrito.find(item => item.id === id);
    
    if (productoExistente) {
        if (productoExistente.cantidad < stockTotal) {
            productoExistente.cantidad++;
        } else {
            alert("No puedes agregar más, has alcanzado el stock disponible.");
            return;
        }
    } else {
        carrito.push({ id, nombre, precio, cantidad: 1 });
    }
    guardarYActualizar();
}

function guardarYActualizar() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
    
    const contenedorItems = document.getElementById("items-carrito");
    const spanTotal = document.getElementById("total-carrito");
    const contadorHeader = document.getElementById("contador-carrito");
    
    contenedorItems.innerHTML = ""; 
    
    if (carrito.length === 0) {
        contenedorItems.innerHTML = "<p>El carrito está vacío.</p>";
        spanTotal.textContent = "0.00";
        if(contadorHeader) contadorHeader.textContent = "0";
        return;
    }

    let total = 0;
    let totalItems = 0;
    
    carrito.forEach(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        totalItems += item.cantidad;
        
        const divItem = document.createElement("div");
        divItem.style.display = "flex";
        divItem.style.justifyContent = "space-between";
        divItem.style.alignItems = "center";
        divItem.style.marginBottom = "10px";
        
        divItem.innerHTML = `
            <span>${item.cantidad}x ${item.nombre} - $${subtotal.toFixed(2)}</span>
            <button onclick="eliminarDelCarrito(${item.id})" style="background: #d32f2f; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; width: auto;">X</button>
        `;
        contenedorItems.appendChild(divItem);
    });

    spanTotal.textContent = total.toFixed(2);
    if(contadorHeader) contadorHeader.textContent = totalItems;
}

function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.id !== id);
    guardarYActualizar();
}

async function procesarCompra() {
    if (carrito.length === 0) {
        alert("Tu carrito está vacío. Agrega productos primero.");
        return;
    }

    const itemsParaEnviar = carrito.map(item => ({
        producto_id: item.id,
        cantidad: item.cantidad
    }));

    try {
        const respuesta = await fetch("http://127.0.0.1:8000/tienda/checkout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(itemsParaEnviar)
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.detail || "Error al procesar la compra");
        }

        alert("¡Compra exitosa! El inventario ha sido actualizado.");
        carrito = [];
        localStorage.setItem("carrito", JSON.stringify(carrito));
        guardarYActualizar(); 
        cargarProductos();

    } catch (error) {
        alert("X " + error.message);
    }
}

cargarProductos();
guardarYActualizar();