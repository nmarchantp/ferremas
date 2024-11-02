from django.shortcuts import render
from productos.models import Producto 

def inicio(request):
    try:
        productos = Producto.objects.all()
        print("Productos obtenidos:", productos)
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        productos = []
    return render(request, 'inicio.html', {'productos': productos})

def productos(request):
    return render(request, 'productos/producto.html')

def catalogo(request):
    return render(request, 'productos/catalogo.html')

def contacto(request):
    return render(request, 'contacto.html')

def ingreso(request):
    return render(request, 'ingreso.html')
