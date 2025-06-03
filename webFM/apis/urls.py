from django.urls import path
from . import views


urlpatterns = [
    path('convertir/', views.convertir, name='convertir'),
    path('api/webpay/pagar/', views.pagar_transbank, name='pagar_transbank'),
    path('webpay/return/', views.transaccion_completa, name='transaccion_completa'),
    
]
