from django.urls import path
from . import views

urlpatterns = [
    # Registro y autenticación
    path('registro/', views.registro, name='registro'),
    path('ingreso/', views.ingreso, name='ingreso'),      # Login por username
    path('login/', views.login_view, name='login'),       # Login por email
    path('logout/', views.logout_view, name='logout'),    # Cierre de sesión
]
