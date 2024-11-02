from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs para Categoria
    path('categoria/', views.CategoriaListView.as_view(template_name='productos/catalogo.html'), name='categoria-list'),
    path('categoria/<int:pk>/', views.CategoriaDetailView.as_view(template_name='productos/productos/catalogo_detalle.html'), name='categoria-detail'),
    path('categoria/create/', views.CategoriaCreateView.as_view(template_name='productos/catalogo_form.html'), name='categoria-create'),
    path('categoria/<int:pk>/update/', views.CategoriaUpdateView.as_view(template_name='productos/catalogo_form.html'), name='categoria-update'),
    path('categoria/<int:pk>/delete/', views.CategoriaDeleteView.as_view(template_name='productos/catalogo_delete.html'), name='categoria-delete'),

    # URLs para Producto
    path('producto/', views.ProductoListView.as_view(template_name='productos/producto.html'), name='producto-list'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(template_name='productos/producto_detalle.html'), name='producto-detail'),
    path('producto/create/', views.ProductoCreateView.as_view(template_name='productos/producto_form.html'), name='producto-create'),
    path('producto/<int:pk>/update/', views.ProductoUpdateView.as_view(template_name='productos/producto_form.html'), name='producto-update'),
    path('producto/<int:pk>/delete/', views.ProductoDeleteView.as_view(template_name='productos/producto_delete.html'), name='producto-delete'),
    
    # Buscar producto
    path('buscar-producto/', views.buscar_producto, name='buscar-producto'),
    
    # Carrito de compras
    path('carrito/', views.carrito_pagina_completa, name='carrito_pagina_completa'),  # Página completa del carrito
    path('carrito-offcanvas/', views.carrito_offcanvas, name='carrito_offcanvas'),  # Vista para el carrito en el offcanvas
    
    # Agregar y gestionar carrito
    path('producto_list/', views.producto_list, name='producto_list'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    # API para obtener detalles de un producto
    path('api/producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]

# Añadir las rutas para archivos estáticos si estás en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
