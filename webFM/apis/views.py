# webFM/apis/views.py (actualizado para usar la API REST externa)

import json
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def pagar(request):
    if request.method == 'POST':

        if 'cliente' not in request.session:
            return JsonResponse({'error': 'Debes iniciar sesión para pagar.'}, status=403)

        try:
            data = json.loads(request.body)
            amount = data.get('amount')

            if not amount:
                return JsonResponse({"error": "Monto no proporcionado"}, status=400)

            # Usa datos de sesión como session_id si es necesario
            session_id = request.session.session_key or 'anon'

            # Llamada a la API REST para iniciar la transacción
            response = requests.post(
                "http://localhost:8000/api/webpay/pagar/",
                json={"amount": amount, "session_id": session_id},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                redirect_url = f"{data['url']}?token_ws={data['token']}"
                return JsonResponse({"redirect_url": redirect_url})
            else:
                return JsonResponse({"error": "No se pudo iniciar el pago"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud malformada. Se esperaba JSON.'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


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

            # Limpiar carrito (opcional: revisar si se hace en API)
            if 'carrito' in request.session:
                del request.session['carrito']
            if 'cart_count' in request.session:
                del request.session['cart_count']
            request.session.modified = True

            return render(request, 'apis/success.html', data)
        else:
            return render(request, 'apis/failure.html', {'error_message': 'Error en la transacción'})
    except Exception as e:
        return render(request, 'apis/failure.html', {'error_message': str(e)})
