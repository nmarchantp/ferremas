from django.urls import path
from .views import registro, ingreso, logout_view, login_view

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('ingreso/', ingreso, name='ingreso'),
    path('login/', login_view, name='login'), 
    path('logout/', logout_view, name='logout'),

]