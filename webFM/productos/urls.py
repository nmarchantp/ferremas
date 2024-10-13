# productos/urls.py
from django.urls import path
from .views import (
    CategoriaListView, CategoriaDetailView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
    buscar_producto
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
]
