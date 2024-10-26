document.addEventListener('DOMContentLoaded', function() {
    // Inicializa botones y formularios
    const loginLink = document.getElementById('login-link');
    const registrationForm = document.getElementById('registrationModal');

    // Verifica si el loginLink existe
    if (loginLink) {
        loginLink.addEventListener('click', function(event) {
            event.preventDefault();
            const modal = new bootstrap.Modal(registrationForm);
            modal.show();
        });
    }

    // Manejo del carrito
    const carrito = {}; // Cambiado a un objeto para manejar las cantidades
    const carritoContenido = document.getElementById('carrito-contenido');
    const carritoMenu = document.getElementById('carrito-menu');
    const carritoToggle = document.getElementById('carrito-toggle');

    let carritoAbierto = false; // Variable de estado para el menú del carrito

    // Mapeo de productos (incluyendo imagen)
    const productos = {
        "1": { nombre: "Grifo de cocina", imagen: "/media/producto/grifo-negro-cocina-berna.jpg" },
        "2": { nombre: "Pintura lavable blanca", imagen: "/media/producto/cerecita.jpg" },
        "3": { nombre: "Manguera de Jardín", imagen: "/media/producto/manguera_tramontina.jpg" },
        "4": { nombre: "Tornillo fijación", imagen: "/media/producto/tornillo_fijacion.jpg" },
        "5": { nombre: "Baldosa Cerámica", imagen: "/media/producto/ceramica_cordillera.jpg" },
        "6": { nombre: "Producto 6", imagen: "/media/producto/producto_6.jpg" },
        "7": { nombre: "Producto 7", imagen: "/media/producto/producto_7.jpg" },
        "8": { nombre: "Producto 8", imagen: "/media/producto/producto_8.jpg" }
        // Agrega más productos según sea necesario
    };

    if (carritoToggle && carritoMenu) { // Verifica que existan los elementos
        // Evento para mostrar/ocultar el menú del carrito al hacer clic
        carritoToggle.addEventListener('click', function() {
            carritoAbierto = !carritoAbierto; // Cambia el estado
            if (carritoAbierto) {
                carritoMenu.style.display = 'block';
                
                // Ajuste para asegurarse de que el carrito esté en la pantalla
                const rect = carritoMenu.getBoundingClientRect();
                if (rect.right > window.innerWidth) {
                    carritoMenu.style.left = 'auto';
                    carritoMenu.style.right = '20px';
                }
            } else {
                carritoMenu.style.display = 'none';
            }
            mostrarCarrito(); // Muestra el contenido del carrito
        });
    }

    // Función para mostrar el carrito
    function mostrarCarrito() {
        carritoContenido.innerHTML = '<h4>Productos en el carrito:</h4>'; // Título del carrito
        for (const id in carrito) {
            const item = document.createElement('div');
            item.classList.add('carrito-item');
    
            // Crea el elemento de imagen
            const imagen = document.createElement('img');
            imagen.src = productos[id].imagen; // Asigna la URL de la imagen del producto
            imagen.alt = productos[id].nombre; // Texto alternativo
            imagen.style.width = '50px'; // Ajusta el tamaño de la imagen
            imagen.style.height = '50px';
            imagen.style.objectFit = 'cover'; // Mantiene la proporción de la imagen
    
            // Crea el texto que muestra nombre y cantidad
            const texto = document.createElement('span');
            texto.textContent = `${productos[id].nombre} x ${carrito[id]}`; 
    
            // Añade la imagen y el texto al contenedor del producto
            item.appendChild(imagen);
            item.appendChild(texto);
    
            carritoContenido.appendChild(item);
        }
        console.log("Carrito: ", carrito);
    }

    // Agregar al carrito
    document.querySelectorAll('.btn-agregar').forEach(button => {
        button.addEventListener('click', function() {
            const productoId = this.getAttribute('data-id');
            
            if (carrito[productoId]) {
                carrito[productoId] += 1; // Aumenta la cantidad
                console.log(`Producto actualizado en el carrito: ${productoId}, Cantidad: ${carrito[productoId]}`);
            } else {
                carrito[productoId] = 1; // Inicializa la cantidad
                console.log("Producto agregado al carrito:", productoId);
            }

            mostrarCarrito();
        });
    });
});
