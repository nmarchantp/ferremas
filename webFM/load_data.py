import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webFM.settings")
django.setup()

from productos.models import Categoria, Producto  

categorias_data = [
    {"id_categoria": 1, "nombre_categoria": "Baño y cocina", "estado_categoria": True},
    {"id_categoria": 2, "nombre_categoria": "Pinturas y pastas", "estado_categoria": True},
    {"id_categoria": 3, "nombre_categoria": "Jardín y accesorios", "estado_categoria": True},
    {"id_categoria": 4, "nombre_categoria": "Fijaciones", "estado_categoria": True},
    {"id_categoria": 5, "nombre_categoria": "Revestimientos", "estado_categoria": True},
]

for categoria_data in categorias_data:
    Categoria.objects.update_or_create(
        id_categoria=categoria_data["id_categoria"],
        defaults={
            "nombre_categoria": categoria_data["nombre_categoria"],
            "estado_categoria": categoria_data["estado_categoria"]
        }
    )


productos_data = [
    {"nombre_producto": "Grifo de cocina", "estado_producto": True, "precio_producto": 15000.00, "id_categoria": 1},
    {"nombre_producto": "Pintura lavable blanca", "estado_producto": True, "precio_producto": 12000.00, "id_categoria": 2},
    {"nombre_producto": "Manguera de jardín", "estado_producto": True, "precio_producto": 2500.00, "id_categoria": 3},
    {"nombre_producto": "Tornillo de fijación", "estado_producto": True, "precio_producto": 300.00, "id_categoria": 4},
    {"nombre_producto": "Baldosa cerámica", "estado_producto": True, "precio_producto": 5000.00, "id_categoria": 5},
]

for producto_data in productos_data:
    try:
        categoria = Categoria.objects.get(id_categoria=producto_data["id_categoria"])
        Producto.objects.create(
            nombre_producto=producto_data["nombre_producto"],
            estado_producto=producto_data["estado_producto"],
            precio_producto=producto_data["precio_producto"],
            categoria_producto=categoria
        )
    except Categoria.DoesNotExist:
        print(f"La categoría con ID {producto_data['id_categoria']} no existe y no se creó el producto {producto_data['nombre_producto']}.")

print("Categorías y productos cargados exitosamente.")
