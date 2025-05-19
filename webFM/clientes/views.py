from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Usar la API interna
from apis.api_views import crear_cliente, autenticar_por_email


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')

        try:
            crear_cliente(username, email, password, nombre)
            messages.success(request, "Registro exitoso.")
            return redirect('ingreso')
        except Exception as e:
            messages.error(request, "Error en el registro: " + str(e))

    return render(request, 'clientes/registro.html')


def ingreso(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'clientes/ingreso.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = autenticar_por_email(email, password)

        if user:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'clientes/ingreso.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'clientes/ingreso.html')


@login_required
def logout_view(request):
    logout(request)

     #Limpiar carrito al salir
    request.session['carrito'] = {}
    request.session['cart_count'] = 0
    request.session.modified = True

    messages.success(request, "Has cerrado sesión.")
    return redirect('inicio')
