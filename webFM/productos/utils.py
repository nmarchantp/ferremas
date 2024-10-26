from django.http import HttpResponseRedirect
from django.urls import reverse

def admin_required(view_func):
    """Decorador para asegurar que el usuario es administrador."""
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si el usuario está autenticado y es administrador
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        # Si no es administrador, redirigir al login u otra página
        return HttpResponseRedirect(reverse('login'))  # O cualquier otra página
    return _wrapped_view
