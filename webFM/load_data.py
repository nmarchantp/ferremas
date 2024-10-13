import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webFM.settings")
django.setup()

from django.contrib.auth.models import User
from productos.models import Categoria, Producto  

# Crear superusuario si no existe
SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@example.com"
SUPERUSER_PASSWORD = "admin123"  

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD
    )
    print(f"Superusuario '{SUPERUSER_USERNAME}' creado exitosamente.")
else:
    print(f"El superusuario '{SUPERUSER_USERNAME}' ya existe.")



categorias_data = [
    {"id_categoria": 1, "codigo_interno": "BC", "nombre_categoria": "Baño y cocina", "estado_categoria": True},
    {"id_categoria": 2, "codigo_interno": "PP", "nombre_categoria": "Pinturas y pastas", "estado_categoria": True},
    {"id_categoria": 3, "codigo_interno": "JA", "nombre_categoria": "Jardín y accesorios", "estado_categoria": True},
    {"id_categoria": 4, "codigo_interno": "FI", "nombre_categoria": "Fijaciones", "estado_categoria": True},
    {"id_categoria": 5, "codigo_interno": "RV", "nombre_categoria": "Revestimientos", "estado_categoria": True},
]

# Crear o actualizar categorías
for categoria_data in categorias_data:
    Categoria.objects.update_or_create(
        id_categoria=categoria_data["id_categoria"],
        defaults={
            "codigo_interno": categoria_data["codigo_interno"],
            "nombre_categoria": categoria_data["nombre_categoria"],
            "estado_categoria": categoria_data["estado_categoria"]
        }
    )

# Datos para los productos
productos_data = [
    {"nombre_producto": "Grifo de cocina", "estado_producto": True, "precio_producto": 15000.00, "id_categoria": 1},
    {"nombre_producto": "Pintura lavable blanca", "estado_producto": True, "precio_producto": 12000.00, "id_categoria": 2},
    {"nombre_producto": "Manguera de jardín", "estado_producto": True, "precio_producto": 2500.00, "id_categoria": 3},
    {"nombre_producto": "Tornillo de fijación", "estado_producto": True, "precio_producto": 300.00, "id_categoria": 4},
    {"nombre_producto": "Baldosa cerámica", "estado_producto": True, "precio_producto": 5000.00, "id_categoria": 5},
]

# Crear productos con códigos internos generados en función de la categoría
for producto_data in productos_data:
    try:
        categoria = Categoria.objects.get(id_categoria=producto_data["id_categoria"])
        
        # Contar productos en la categoría para generar el número secuencial
        numero_producto = Producto.objects.filter(categoria_producto=categoria).count() + 1
        codigo_producto = f"{categoria.codigo_interno}-{numero_producto:04d}"
        
        Producto.objects.create(
            codigo_interno=codigo_producto,
            nombre_producto=producto_data["nombre_producto"],
            estado_producto=producto_data["estado_producto"],
            precio_producto=producto_data["precio_producto"],
            categoria_producto=categoria
        )
        print(f"Producto '{producto_data['nombre_producto']}' creado con código interno '{codigo_producto}'.")
        
    except Categoria.DoesNotExist:
        print(f"La categoría con ID {producto_data['id_categoria']} no existe y no se creó el producto {producto_data['nombre_producto']}.")

print("Categorías y productos cargados exitosamente.")
