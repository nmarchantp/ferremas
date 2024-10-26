document.addEventListener('DOMContentLoaded', function() {
    const carrito = {};
    const carritoContenido = document.getElementById('carrito-contenido');
    const carritoMenu = document.getElementById('carrito-menu');
    const carritoToggle = document.getElementById('carrito-toggle');

    let carritoAbierto = false;

    function mostrarCarrito() {
        carritoContenido.innerHTML = '<h4>Productos en el carrito:</h4>';
        for (const id in carrito) {
            const item = document.createElement('div');
            item.classList.add('carrito-item');

            const imagen = document.createElement('img');
            imagen.src = carrito[id].imagen;
            imagen.alt = carrito[id].nombre;
            imagen.style.width = '50px';
            imagen.style.height = '50px';
            imagen.style.objectFit = 'cover';

            const texto = document.createElement('span');
            texto.textContent = `${carrito[id].nombre} x ${carrito[id].cantidad}`;

            item.appendChild(imagen);
            item.appendChild(texto);
            carritoContenido.appendChild(item);
        }
    }

    async function agregarAlCarrito(productoId) {
        try {
            const response = await fetch(`/api/producto/${productoId}/`);
            if (!response.ok) throw new Error("Producto no encontrado");
            const data = await response.json();

            if (carrito[productoId]) {
                carrito[productoId].cantidad += 1;
            } else {
                carrito[productoId] = { nombre: data.nombre, imagen: data.imagen, cantidad: 1 };
            }

            mostrarCarrito();
        } catch (error) {
            console.error("Error al obtener el producto:", error);
        }
    }

    document.querySelectorAll('.btn-agregar').forEach(button => {
        button.addEventListener('click', function() {
            const productoId = this.getAttribute('data-id');
            agregarAlCarrito(productoId);
        });
    });

    if (carritoToggle && carritoMenu) {
        carritoToggle.addEventListener('click', function() {
            carritoAbierto = !carritoAbierto;
            carritoMenu.style.display = carritoAbierto ? 'block' : 'none';
            mostrarCarrito();
        });
    }
});
