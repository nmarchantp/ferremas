from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente
from django.contrib.auth.decorators import login_required


def registro(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        email = request.POST['email']
        password = request.POST['password']
        nombre = request.POST['nombre']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            Cliente.objects.create(user=user, nombre=nombre)  # Crear el cliente asociado
            messages.success(request, "Registro exitoso.")
            return redirect('ingreso')  # Redirigir después del registro exitoso
        except Exception as e:
            messages.error(request, "Error en el registro: " + str(e))
    return render(request, 'clientes/registro.html')

def ingreso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')  # Redirigir a la página principal
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'clientes/ingreso.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Obtener el correo electrónico
        password = request.POST.get('password')

        # Buscar al usuario por correo electrónico
        try:
            user = User.objects.get(email=email)  # Obtener el usuario por su correo electrónico
        except User.DoesNotExist:
            user = None

        # Autenticar con el nombre de usuario y la contraseña
        if user and user.check_password(password):  # Verificar la contraseña
            login(request, user)  # Iniciar sesión
            return redirect('inicio')  # Redirige a la página principal
        else:
            return render(request, 'clientes/ingreso.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'clientes/ingreso.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")  # Mensaje de éxito
    return redirect('inicio')  # Redirigir a la página principal
