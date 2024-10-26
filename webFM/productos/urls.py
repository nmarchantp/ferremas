# productos/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CategoriaListView, CategoriaDetailView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
    buscar_producto, carrito, producto_list, agregar_al_carrito
)

urlpatterns = [
    # URLs para Categoria
    path('categoria/', CategoriaListView.as_view(template_name='catalogo.html'), name='categoria-list'),
    path('categoria/<int:pk>/', CategoriaDetailView.as_view(template_name='catalogo_detalle.html'), name='categoria-detail'),
    path('categoria/create/', CategoriaCreateView.as_view(template_name='catalogo_form.html'), name='categoria-create'),
    path('categoria/<int:pk>/update/', CategoriaUpdateView.as_view(template_name='catalogo_form.html'), name='categoria-update'),
    path('categoria/<int:pk>/delete/', CategoriaDeleteView.as_view(template_name='catalogo_delete.html'), name='categoria-delete'),

    # URLs para Producto
    path('producto/', ProductoListView.as_view(template_name='producto.html'), name='producto-list'),
    path('producto/<int:pk>/', ProductoDetailView.as_view(template_name='producto_detalle.html'), name='producto-detail'),
    path('producto/create/', ProductoCreateView.as_view(template_name='producto_form.html'), name='producto-create'),
    path('producto/<int:pk>/update/', ProductoUpdateView.as_view(template_name='producto_form.html'), name='producto-update'),
    path('producto/<int:pk>/delete/', ProductoDeleteView.as_view(template_name='producto_delete.html'), name='producto-delete'),
    path('buscar-producto/', buscar_producto, name='buscar-producto'),
    path('carrito/', carrito, name='carrito'),
    path('productos/', producto_list, name='producto_list'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('api/producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)