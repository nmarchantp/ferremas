from productos.models import Categoria, Producto
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webFM.settings")
django.setup()

def run():
    Categoria.objects.all().delete()
    Producto.objects.all().delete()
    print("Datos de Categoria y Producto eliminados.")