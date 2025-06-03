from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import requests
from .forms import ProductoForm
from .models import Categoria, Producto
from .utils import admin_required
import json
from django.views import View

# ---------- CATEGORÍAS ----------

class CategoriaDetailView(View):
    def get(self, request, pk):
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/categorias/{pk}/")
            if response.status_code == 200:
                categoria = response.json()
                return render(request, 'productos/catalogo_detalle.html', {'categoria': categoria})
        except Exception as e:
            print("❌ Error al obtener categoría:", e)
        return redirect('categoria-list')

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'catalogo.html'


@method_decorator(admin_required, name='dispatch')
class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'catalogo_form.html'
    fields = ['codigo_interno', 'nombre_categoria', 'estado_categoria']
    success_url = reverse_lazy('categoria-list')


@method_decorator(admin_required, name='dispatch')
class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'catalogo_form.html'
    fields = ['nombre_categoria', 'estado_categoria']
    success_url = reverse_lazy('categoria-list')


@method_decorator(admin_required, name='dispatch')
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'catalogo_delete.html'
    success_url = reverse_lazy('categoria-list')


# ---------- PRODUCTOS ----------
class ProductoListView(View):
    template_name = 'productos/producto.html'

    def get(self, request):
        try:
            response = requests.get('http://127.0.0.1:8000/api/productos/')
            response.raise_for_status()
            productos = response.json()
        except requests.exceptions.RequestException as e:
            productos = []
            print(f"Error al consumir la API: {e}")

        return render(request, self.template_name, {
            'object_list': productos
        })

class ProductoDetailView(View):
    def get(self, request, pk):
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/productos/{pk}/")
            if response.status_code == 200:
                producto = response.json()
                return render(request, 'producto_detalle.html', {'object': producto})
        except Exception as e:
            print("❌ Error en detalle producto:", e)

        return redirect('producto-list')

@method_decorator(admin_required, name='dispatch')
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')


@method_decorator(admin_required, name='dispatch')
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')


@method_decorator(admin_required, name='dispatch')
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')


def buscar_producto(request):
    codigo = request.GET.get('codigo')
    if codigo:
        producto = get_object_or_404(Producto, codigo_interno=codigo)
        return redirect('producto-detail', pk=producto.pk)
    return redirect('producto-list')


def listar_productos():
    try:
        response = requests.get('http://localhost:8000/api/productos/')
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def obtener_producto_por_id(producto_id):
    try:
        response = requests.get(f'http://localhost:8000/api/productos/{producto_id}/')
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error al obtener producto {producto_id}: {e}")
        return None


# ---------- CARRITO ----------

def obtener_datos_carrito(request):
    carrito = request.session.get('carrito', {})
    ids = list(map(int, carrito.keys()))
    productos = []
    cantidades = {int(pid): carrito[str(pid)] for pid in ids}

    for pid in ids:
        try:
            res = requests.get(f"http://127.0.0.1:8000/api/productos/{pid}/")
            if res.status_code == 200:
                producto = res.json()
                producto['cantidad'] = cantidades[pid]
                productos.append(producto)
        except:
            continue

    total = sum(p['precio'] * p['cantidad'] for p in productos)
    tasa_dolar = 850

    return {
        'productos': productos,
        'cantidad_por_producto': cantidades,
        'total_carrito': total,
        'total_dolares': total / tasa_dolar
    }


def carrito_pagina_completa(request):
    return render(request, 'productos/carrito.html', obtener_datos_carrito(request))


def carrito_offcanvas(request):
    return render(request, 'productos/carrito_list.html', obtener_datos_carrito(request))


def producto_list(request):
    if 'cart_count' not in request.session:
        request.session['cart_count'] = 0

    try:
        response = requests.get("http://127.0.0.1:8000/api/productos/")
        productos = response.json() if response.status_code == 200 else []
    except Exception as e:
        productos = []
        print("❌ Error al cargar productos desde la API:", e)

    context = {
        'cart_count': request.session['cart_count'],
        'productos': productos
    }
    return render(request, 'productos/producto_list.html', context)


def agregar_al_carrito(request, producto_id):
    print("📦 Sesión actual:", request.session.get('cliente'))  # ⬅️ Agrega esto

    if 'cliente' not in request.session:
        return JsonResponse({'mensaje': 'Debes iniciar sesión para comprar.'}, status=403)
    if request.method == 'POST':
        try:
 
            response = requests.get(f"http://127.0.0.1:8000/api/productos/{producto_id}/")
            if response.status_code != 200:
                return JsonResponse({'mensaje': 'Producto no encontrado'}, status=404)

            producto = response.json()

            carrito = request.session.get('carrito', {})
            pid = str(producto_id)
            carrito[pid] = carrito.get(pid, 0) + 1
            request.session['carrito'] = carrito
            request.session.modified = True

            return JsonResponse({'mensaje': 'Producto agregado al carrito.'})
        except Exception as e:
            return JsonResponse({'mensaje': str(e)}, status=500)

    return JsonResponse({'mensaje': 'Error al agregar el producto.'}, status=400)


def eliminar_producto_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    pid = str(producto_id)
    if pid in carrito:
        del carrito[pid]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('carrito')


# ---------- PRODUCTOS API LIGHT ----------


def detalle_producto(request, producto_id):
    p = get_object_or_404(Producto, id=producto_id)
    return JsonResponse({
        'id': p.id,
        'nombre': p.nombre,
        'imagen': p.imagen.url if p.imagen else ''
    })
