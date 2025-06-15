# webFM/apis/views.py (actualizado para usar la API REST externa)

import json
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def pagar_transbank(request):
    if request.method == 'POST':
        if 'cliente' not in request.session:
            return JsonResponse({'error': 'Debes iniciar sesión'}, status=403)

        data = json.loads(request.body)
        amount = data.get('amount')

        cliente_id = request.session['cliente']['id']  
        session_id = request.session.session_key or 'anon'
        orden_compra = f"orden-{session_id[:8]}"

        response = requests.post(
            'http://127.0.0.1:8000/api/webpay/pagar/',  
            json={
                'amount': amount,
                'orden_compra': orden_compra,
                'cliente_id': cliente_id 
            },
            headers={'Content-Type': 'application/json'}
        )

        r = response.json()

        if response.status_code == 200 and 'url' in r and 'token' in r:
            redirect_url = f"{r['url']}?token_ws={r['token']}"
            return JsonResponse({'redirect_url': redirect_url})
        else:
            print(f"⚠️ Error desde API externa: {r}")
            return JsonResponse({
                'error': r.get('error', 'Error desconocido en API externa'),
                'detalle': r
            }, status=response.status_code)



@csrf_exempt
def pago_exito(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return render(request, 'pago_fallido.html', {'mensaje': 'Token no entregado'})

    response = requests.post(
        'http://127.0.0.1:8000/api/webpay/confirmar/',
        json={'token_ws': token_ws},
        headers={'Content-Type': 'application/json'}
    )

    resultado = response.json()

    if response.status_code == 200:
        return render(request, 'pago_exitoso.html', {'resultado': resultado})
    else:
        return render(request, 'pago_fallido.html', {'mensaje': resultado.get('error', 'Error desconocido')})


def convertir(request):
    monto_usd = float(request.GET.get('monto_usd', 0))
    if monto_usd <= 0:
        return JsonResponse({'error': 'Monto en USD no válido'}, status=400)

    try:
        response = requests.get("http://localhost:8000/api/convertir/", params={"monto_usd": monto_usd})
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Error al obtener la tasa de cambio'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')

    if not token_ws:
        return render(request, 'apis/failure.html', {'error_message': 'No se encontró el token de la transacción.'})

    try:
        response = requests.get("http://localhost:8000/api/webpay/return/", params={"token_ws": token_ws})
        if response.status_code == 200:
            data = response.json()

            limpiar_carrito(request)

            return render(request, 'apis/success.html', data)
        else:
            return render(request, 'apis/failure.html', {'error_message': 'Error en la transacción'})
    except Exception as e:
        return render(request, 'apis/failure.html', {'error_message': str(e)})


def limpiar_carrito(request):
    for key in ['carrito', 'cart_count']:
        if key in request.session:
            del request.session[key]
    request.session.modified = True