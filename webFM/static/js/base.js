document.addEventListener('DOMContentLoaded', function () {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || {}; // Cargar carrito desde localStorage o inicializar vacío
    const carritoContenido = document.getElementById('carritoContenido');
    const carritoOffcanvasElement = document.getElementById('offcanvasCarrito');
    const carritoOffcanvas = new bootstrap.Offcanvas(carritoOffcanvasElement); // Inicializar el offcanvas de Bootstrap

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Coincide con csrftoken
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    

    // Eliminar manualmente el backdrop cuando el offcanvas se oculta
    carritoOffcanvasElement.addEventListener('hidden.bs.offcanvas', function () {
        document.querySelectorAll('.offcanvas-backdrop').forEach(backdrop => backdrop.remove());
    });

    // Guardar el carrito en localStorage
    function guardarCarrito() {
        localStorage.setItem('carrito', JSON.stringify(carrito)); // Guardar el carrito en localStorage
    }

    // Función para obtener la tasa de conversión del servidor
    async function obtenerTasaConversion(totalUSD) {
        try {
            const response = await fetch(`/api/convertir/?monto_usd=${totalUSD}`);
            const data = await response.json();
            console.log(data);
            return data.monto_clp;
        } catch (error) {
            console.error("Error al obtener la tasa de conversión:", error);
            return null;
        }
    }

    async function mostrarCarrito() {
        if (!carritoContenido) {
            console.error("El elemento carritoContenido no existe en el DOM.");
            return;
        }

        carritoContenido.innerHTML = ''; // Limpiar contenido antes de actualizar
        let totalProductos = 0;
        let totalValor = 0;

        for (const id in carrito) {
            const producto = carrito[id];

            // Crear contenedor de cada producto en el carrito
            const item = document.createElement('div');
            item.classList.add('carrito-item');

            // Imagen del producto
            const img = document.createElement('img');
            img.src = producto.imagen_producto;
            img.alt = producto.nombre_producto;
            img.classList.add('img-fluid', 'carrito-img');
            img.style.width = '120px';
            img.style.height = '120px';
            img.style.objectFit = 'cover';
            img.style.borderRadius = '8px';
            item.appendChild(img);

            // Contenedor para nombre y precio
            const productoInfo = document.createElement('div');
            productoInfo.classList.add('producto-info');

            // Nombre del producto
            const nombre = document.createElement('span');
            nombre.textContent = `${producto.nombre_producto} x ${producto.cantidad}`;
            productoInfo.appendChild(nombre);

            // Precio del producto
            const precio = document.createElement('span');
            precio.textContent = `Precio: $${producto.precio}`;
            productoInfo.appendChild(precio);

            item.appendChild(productoInfo);

            // Controles de cantidad
            const cantidadControles = document.createElement('div');
            cantidadControles.classList.add('cantidad-controles');

            // Botón para disminuir cantidad
            const btnDisminuir = document.createElement('button');
            btnDisminuir.textContent = '-';
            btnDisminuir.classList.add('btn', 'btn-sm', 'btn-danger');
            btnDisminuir.addEventListener('click', function () {
                if (producto.cantidad > 1) {
                    producto.cantidad--;
                } else {
                    delete carrito[id];
                }
                guardarCarrito();
                mostrarCarrito();
            });
            cantidadControles.appendChild(btnDisminuir);

            // Cantidad actual
            const cantidad = document.createElement('span');
            cantidad.textContent = producto.cantidad;
            cantidadControles.appendChild(cantidad);

            // Botón para aumentar cantidad
            const btnAumentar = document.createElement('button');
            btnAumentar.textContent = '+';
            btnAumentar.classList.add('btn', 'btn-sm', 'btn-success');
            btnAumentar.addEventListener('click', function () {
                producto.cantidad++;
                guardarCarrito();
                mostrarCarrito();
            });
            cantidadControles.appendChild(btnAumentar);

            item.appendChild(cantidadControles);

            // Botón para eliminar producto
            const btnEliminar = document.createElement('button');
            btnEliminar.textContent = 'Eliminar';
            btnEliminar.classList.add('btn', 'btn-sm', 'btn-danger', 'ml-2');
            btnEliminar.addEventListener('click', function () {
                delete carrito[id];
                guardarCarrito();
                mostrarCarrito();
            });
            item.appendChild(btnEliminar);

            carritoContenido.appendChild(item);

            // Calcular el total en USD
            totalProductos += producto.cantidad;
            totalValor += producto.precio * producto.cantidad;
        }

        // Redondear el total en USD a dos decimales
        const totalValorRedondeado = totalValor.toFixed(2);

        // Actualizar o crear el elemento para el total en USD
        let totalElement = document.querySelector('.carrito-total');
        if (!totalElement) {
            totalElement = document.createElement('div');
            totalElement.classList.add('carrito-total');
            carritoContenido.appendChild(totalElement);
        }
        totalElement.textContent = `Total: $${totalValorRedondeado}`;

        // Obtener y mostrar el total en CLP
        const totalEnCLP = await obtenerTasaConversion(totalValor);
        let totalCLPElement = document.querySelector('.carrito-total-clp');
        if (!totalCLPElement) {
            totalCLPElement = document.createElement('div');
            totalCLPElement.classList.add('carrito-total-clp');
            carritoContenido.appendChild(totalCLPElement);
        }

        if (totalEnCLP !== null) {
            const totalEnCLPAbsoluto = Math.round(totalEnCLP);
            totalCLPElement.textContent = `Total en CLP: $${totalEnCLPAbsoluto}`;

            // Crear o actualizar el botón de pago
            let pagarButton = document.querySelector('.btn-pagar');
            if (!pagarButton) {
                pagarButton = document.createElement('button');
                pagarButton.classList.add('btn', 'btn-primary', 'mt-3', 'btn-pagar');
                pagarButton.textContent = "Pagar con Transbank";
                carritoContenido.appendChild(pagarButton);
            }

            // Agregar evento para iniciar el pago
            pagarButton.onclick = () => iniciarPagoConTransbank(totalEnCLPAbsoluto);
        } else {
            console.warn("No se pudo calcular el total en pesos chilenos.");
        }
    }


    // Función para iniciar el pago enviando el monto en CLP a la vista de Django
    async function iniciarPagoConTransbank(montoCLP) {
    if (!montoCLP || isNaN(montoCLP) || montoCLP <= 0) {
        alert("Monto inválido. Debe ser mayor que cero.");
        return;
    }

    try {
        const response = await fetch('/pagar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // usa esta función si tienes CSRF habilitado
            },
            body: JSON.stringify({ amount: montoCLP })
        });

        const data = await response.json();

        if (response.ok && data.redirect_url) {
            window.location.href = data.redirect_url;  // redirige a Webpay
        } else {
            alert(data.error || "Error al iniciar el pago");
        }

    } catch (error) {
        console.error("Error al pagar:", error);
        alert("Hubo un problema al intentar iniciar el pago.");
    }
}


    // Cargar el carrito al cargar la página
    mostrarCarrito();

    // Evento para agregar productos al carrito
    document.querySelectorAll('.btn-agregar').forEach(button => {
        button.addEventListener('click', function () {
            const productoId = this.getAttribute('data-id');
            const productoNombre = this.parentElement.querySelector('.card-title').textContent;
            const productoPrecio = parseFloat(this.getAttribute('data-precio'));
            const productoImagen = this.parentElement.parentElement.querySelector('img').src;

            if (carrito[productoId]) {
                carrito[productoId].cantidad++;
            } else {
                carrito[productoId] = {
                    nombre_producto: productoNombre,
                    cantidad: 1,
                    precio: productoPrecio,
                    imagen_producto: productoImagen
                };
            }

            console.log(`Producto actualizado en el carrito: ${productoId}, Cantidad: ${carrito[productoId].cantidad}`);
            guardarCarrito();
            mostrarCarrito();
            if (carritoOffcanvas) carritoOffcanvas.show();

        });
    });
});
