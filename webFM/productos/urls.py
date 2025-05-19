from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ----------- Categorías -----------
    path('categoria/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/create/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categoria/<int:pk>/update/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/<int:pk>/delete/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),

    # ----------- Productos (admin y detalle) -----------
    path('producto/', views.ProductoListView.as_view(), name='producto-list'),
    path('producto/create/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),
    path('producto/<int:pk>/update/', views.ProductoUpdateView.as_view(), name='producto-update'),
    path('producto/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),

    # ----------- Carrito -----------
    path('carrito/', views.carrito_pagina_completa, name='carrito_pagina_completa'),
    path('carrito-offcanvas/', views.carrito_offcanvas, name='carrito_offcanvas'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-carrito/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),

    # ----------- Funcionalidad extra -----------
    path('producto_list/', views.producto_list, name='producto_list'),
    path('buscar-producto/', views.buscar_producto, name='buscar-producto'),

    # ----------- API interna simple -----------
    path('api/producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]

# Servir media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
