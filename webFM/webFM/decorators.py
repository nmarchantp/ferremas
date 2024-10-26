from django.shortcuts import redirect
from django.urls import reverse

def admin_required_redirect(function):
    def wrap(request, *args, **kwargs):
        print("Verificando permisos para el usuario:", request.user)
        if request.user.is_authenticated and request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            print("Acceso denegado, redirigiendo a login.")
            return redirect(reverse('login'))
    return wrap