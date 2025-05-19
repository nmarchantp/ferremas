from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('convertir/', views.convertir, name='convertir'),
    path('pagar/', views.pagar, name='pagar'),
    path('webpay/return/', views.transaccion_completa, name='transaccion_completa'),
    path('clientes/perfil/', api_views.api_perfil_cliente, name='api-perfil-cliente'),
    path('clientes/<int:cliente_id>/', api_views.api_cliente_por_id, name='api-cliente-id'),
    path('clientes/', api_views.api_listar_clientes, name='api-clientes'),
    path('clientes/perfil/actualizar/', api_views.api_actualizar_perfil_cliente, name='api-actualizar-perfil'),
    path('productos/', api_views.api_listar_productos, name='api-productos'),
    path('productos/<int:producto_id>/', api_views.api_producto_por_id, name='api-producto-detalle'),
    path('productos/crear/', api_views.api_crear_producto, name='api-producto-crear'),
    path('productos/<int:producto_id>/actualizar/', api_views.api_actualizar_producto, name='api-producto-actualizar'),
    path('productos/<int:producto_id>/eliminar/', api_views.api_eliminar_producto, name='api-producto-eliminar'),

]
