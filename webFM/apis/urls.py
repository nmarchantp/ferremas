from django.urls import path
from . import views

urlpatterns = [
    path('convertir/', views.convertir, name='convertir'),
    path('pagar/', views.pagar, name='pagar'),
    path('webpay/return/', views.transaccion_completa, name='transaccion_completa'),

]
