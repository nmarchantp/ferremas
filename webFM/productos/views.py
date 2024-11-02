from pyexpat.errors import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Categoria, Producto, Carrito
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from .forms import ProductoForm
from .utils import admin_required
from django.http import JsonResponse

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

# Vistas para Producto
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto.html'  # Asegúrate de que este sea el nombre correcto de tu template
    context_object_name = 'object_list'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'producto_detalle.html'

@method_decorator(admin_required, name='dispatch')
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm  # Usa el formulario que creaste
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')

@method_decorator(admin_required, name='dispatch')
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm  # Usa el formulario que creaste
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')


@method_decorator(admin_required, name='dispatch')
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')


def buscar_producto(request):
    codigo = request.GET.get('codigo', None)
    if codigo:
        producto = get_object_or_404(Producto, codigo_interno=codigo)
        return redirect(reverse('producto-detail', args=[producto.pk]))
    return redirect('producto-list')


def obtener_datos_carrito(request):
    productos_en_carrito = request.session.get('carrito', {})
    
    # Convertir las claves del carrito (strings) a enteros
    productos_ids = map(int, productos_en_carrito.keys())
    productos = Producto.objects.filter(id_producto__in=productos_ids)

    # Contar la cantidad de cada producto en el carrito
    cantidad_por_producto = {producto.id_producto: productos_en_carrito[str(producto.id_producto)] for producto in productos}

    # Calcular el total en pesos chilenos
    total_carrito = sum(producto.precio_producto * cantidad_por_producto[producto.id_producto] for producto in productos)

    # Tasa de cambio (usa la API del Banco Central si la tienes)
    tasa_cambio_dolar = 850
    total_dolares = total_carrito / tasa_cambio_dolar

    # Devuelve la información del carrito en un diccionario
    return {
        'productos': productos,
        'cantidad_por_producto': cantidad_por_producto,
        'total_carrito': total_carrito,
        'total_dolares': total_dolares,
    }

def carrito_pagina_completa(request):
    # Llama al método para obtener los datos del carrito
    datos_carrito = obtener_datos_carrito(request)
    
    # Renderiza la página completa del carrito
    return render(request, 'productos/carrito.html', datos_carrito)

def carrito_offcanvas(request):
    # Llama al método para obtener los datos del carrito
    datos_carrito = obtener_datos_carrito(request)
    
    # Renderiza solo la parte que se va a mostrar en el offcanvas
    return render(request, 'productos/carrito_list.html', datos_carrito)


def producto_list(request):
    # Verificar si el carrito está en la sesión, si no, inicializarlo
    if 'cart_count' not in request.session:
        request.session['cart_count'] = 0

    # Obtener el número de productos en el carrito
    cart_count = request.session['cart_count']

    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()  # Asegúrate de que 'Producto' es el nombre de tu modelo

    context = {
        'cart_count': cart_count,
        'productos': productos,  # Agrega la lista de productos al contexto
    }
    
    return render(request, 'productos/producto_list.html', context)


def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        # Verificar si el producto existe en la base de datos
        producto = get_object_or_404(Producto, id_producto=producto_id)

        # Obtener el carrito de la sesión o crear uno nuevo
        carrito = request.session.get('carrito', {})

        # Convertir el producto_id a string, ya que las claves de la sesión son strings
        producto_id_str = str(producto_id)

        # Aumentar la cantidad del producto en el carrito
        if producto_id_str in carrito:
            carrito[producto_id_str] += 1  # Aumentar la cantidad en 1
        else:
            carrito[producto_id_str] = 1  # Agregar el producto con cantidad 1

        # Guardar el carrito en la sesión
        request.session['carrito'] = carrito
        request.session.modified = True  # Marca la sesión como modificada

        return JsonResponse({'mensaje': 'Producto agregado al carrito.'})
    
    return JsonResponse({'mensaje': 'Error al agregar el producto.'}, status=400)

    

def eliminar_producto_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    producto_id_str = str(producto_id)
    if producto_id_str in carrito:
        del carrito[producto_id_str]

        # Guardar el carrito actualizado en la sesión
        request.session['carrito'] = carrito
        request.session.modified = True  # Marca la sesión como modificada

    return redirect('carrito')


def obtener_producto( producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'imagen': producto.imagen.url,
            'precio': producto.precio,  # Agrega otros campos según lo necesario
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    
def detalle_producto(request, producto_id):
    # Busca el producto o retorna un error 404 si no se encuentra
    producto = get_object_or_404(Producto, id=producto_id)
    data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'imagen': producto.imagen.url if producto.imagen else '',  # Asegura que el campo 'imagen' exista
    }
    return JsonResponse(data)