from django.contrib import admin
from .models import Producto, Categoria, Carrito


admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Carrito)