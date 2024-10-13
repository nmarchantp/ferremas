# productos/views.py
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Categoria, Producto
from django.shortcuts import render, redirect, get_object_or_404


# Vistas para Categoria
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'catalogo.html'  # Nombre de la plantilla para listar

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'productos/catalogo_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener productos relacionados a la categoría
        context['productos'] = Producto.objects.filter(categoria_producto=self.object)
        return context

class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'catalogo_form.html'  # Nombre de la plantilla para formulario de creación
    fields = ['nombre_categoria', 'estado_categoria']
    success_url = reverse_lazy('categoria-list')

class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'catalogo_form.html'  # Reutilizamos la misma plantilla para editar
    fields = ['nombre_categoria', 'estado_categoria']
    success_url = reverse_lazy('categoria-list')

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'catalogo_delete.html'  # Nombre de la plantilla para confirmación de eliminación
    success_url = reverse_lazy('categoria-list')

# Vistas para Producto
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto.html'  # Nombre de la plantilla para listar

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'producto_detalle.html'  # Nombre de la plantilla para detalle

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'producto_form.html'  # Nombre de la plantilla para formulario de creación
    fields = ['nombre_producto', 'estado_producto', 'precio_producto', 'categoria_producto']
    success_url = reverse_lazy('producto-list')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'producto_form.html'  # Reutilizamos la misma plantilla para editar
    fields = ['nombre_producto', 'estado_producto', 'precio_producto', 'categoria_producto']
    success_url = reverse_lazy('producto-list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_delete.html' 
    success_url = reverse_lazy('producto-list')

def buscar_producto(request):
    codigo = request.GET.get('codigo', None)  # Captura el código del producto del parámetro GET
    producto = None

    if codigo:
        # Buscar el producto por ID (o cambiar a otro campo si buscas por nombre u otro atributo)
        producto = get_object_or_404(Producto, codigo_interno=codigo)
        return redirect(reverse('producto-detail', args=[producto.pk]))

    return redirect('producto-list')