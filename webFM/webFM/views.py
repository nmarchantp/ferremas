from django.shortcuts import render
from productos.models import Producto  # Asegúrate de tener esta importación

def inicio(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'inicio.html', {'productos': productos})

def productos(request):
    return render(request, 'productos/producto.html')

def catalogo(request):
    return render(request, 'productos/catalogo.html')

def contacto(request):
    return render(request, 'contacto.html')

def ingreso(request):
    return render(request, 'ingreso.html')
