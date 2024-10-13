
from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def productos(request):
    return render(request, 'productos/producto.html')

def catalogo(request):
    return render(request, 'productos/catalogo.html')

def contacto(request):
    return render(request, 'contacto.html')
