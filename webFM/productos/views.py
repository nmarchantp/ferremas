from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from .forms import ProductoForm
from .models import Categoria, Producto
from .utils import admin_required
from apis.api_views import listar_productos, obtener_producto_por_id
import json


# ---------- CATEGORÍAS ----------

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'catalogo.html'


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'productos/catalogo_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(categoria_producto=self.object)
        return context


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

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto.html'
    context_object_name = 'object_list'


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'producto_detalle.html'


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


# ---------- CARRITO ----------

def obtener_datos_carrito(request):
    carrito = request.session.get('carrito', {})
    ids = list(map(int, carrito.keys()))
    productos = Producto.objects.filter(id_producto__in=ids)
    cantidades = {int(pid): carrito[str(pid)] for pid in ids}
    total = sum(p.precio_producto * cantidades[p.id_producto] for p in productos)

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

    context = {
        'cart_count': request.session['cart_count'],
        'productos': listar_productos()  # uso de API interna
    }
    return render(request, 'productos/producto_list.html', context)


def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id_producto=producto_id)
        carrito = request.session.get('carrito', {})
        pid = str(producto_id)
        carrito[pid] = carrito.get(pid, 0) + 1
        request.session['carrito'] = carrito
        request.session.modified = True
        return JsonResponse({'mensaje': 'Producto agregado al carrito.'})
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

def obtener_producto(producto_id):
    try:
        p = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'id': p.id,
            'nombre': p.nombre,
            'imagen': p.imagen.url if p.imagen else '',
            'precio': p.precio
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def detalle_producto(request, producto_id):
    p = get_object_or_404(Producto, id=producto_id)
    return JsonResponse({
        'id': p.id,
        'nombre': p.nombre,
        'imagen': p.imagen.url if p.imagen else ''
    })
