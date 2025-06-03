from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import requests


def perfil_cliente(request):
    # Suponiendo que el ID del cliente coincide con el del user logueado
    cliente_id = request.user.id
    api_url = f'http://127.0.0.1:8000/api/clientes/{cliente_id}/'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        cliente = response.json()
    except requests.exceptions.RequestException as e:
        return render(request, 'clientes/perfil_error.html', {'error': str(e)})

    return render(request, 'clientes/perfil.html', {'cliente': cliente})


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')

        data = {
            "user": {
                "username": username,
                "email": email,
                "password": password
            },
            "nombre": nombre
        }

        try:
            response = requests.post("http://127.0.0.1:8000/api/clientes/", json=data)

            if response.status_code == 201:
                # Registro exitoso → redirige al login
                return redirect('login')
            else:
                # Mostrar mensaje de error devuelto por la API
                return render(request, 'clientes/registro.html', {
                    'error': response.json()
                })
        except Exception as e:
            return render(request, 'clientes/registro.html', {'error': str(e)})

    return render(request, 'clientes/registro.html')


def ingreso(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil_cliente') 

        return render(request, 'clientes/ingreso.html', {'error': 'Credenciales inválidas'})

    return render(request, 'clientes/ingreso.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/clientes/login/',
                json={'email': email, 'password': password} 
            )

            if response.status_code == 200:
                cliente = response.json()
                request.session['cliente'] = cliente
                return redirect('inicio') 
            else:
                return render(request, 'clientes/ingreso.html', {
                    'error': response.json().get('error', 'Credenciales inválidas')
                })
        except Exception as e:
            return render(request, 'clientes/ingreso.html', {'error': str(e)})

    return render(request, 'clientes/ingreso.html')

def logout_view(request):
    if 'cliente' in request.session:
        del request.session['cliente']
    return redirect('inicio')