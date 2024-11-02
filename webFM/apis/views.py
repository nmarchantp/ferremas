import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from django.conf import settings
from django.shortcuts import redirect, render
import bcchapi

from datetime import datetime, timedelta

def convertir(request):
    # Obtener el monto en USD desde los parámetros de la solicitud GET
    monto_usd = float(request.GET.get('monto_usd', 0))  # Valor por defecto es 0 si no se proporciona

    # Crear instancia de la API del Banco Central con las credenciales
    siete_instance = bcchapi.Siete(usr=settings.BC_USUARIO, pwd=settings.BC_PASSWORD)
    
    # Establecer la fecha inicial como hoy y el rango de búsqueda en días hacia atrás
    fecha_hoy = datetime.now()
    dias_retroceso = 7  # Número de días hacia atrás para buscar el último valor
    
    cuadro = None
    for i in range(dias_retroceso):
        # Calcular la fecha de búsqueda en días hacia atrás
        fecha_busqueda = fecha_hoy - timedelta(days=i)
        fecha_busqueda_str = fecha_busqueda.strftime("%Y-%m-%d")
        
        # Obtener el tipo de cambio para la serie de dólares (F073.TCO.PRE.Z.D) en esa fecha
        cuadro = siete_instance.cuadro(
            series=['F073.TCO.PRE.Z.D'],
            desde=fecha_busqueda_str,
            hasta=fecha_busqueda_str
        )
        
        # Si el DataFrame no está vacío, hemos encontrado el valor más reciente
        if not cuadro.empty:
            break

    # Verificar si encontramos datos en el rango de búsqueda
    if cuadro is None or cuadro.empty:
        return JsonResponse({'error': 'No se encontraron datos de tipo de cambio en el rango de búsqueda.'}, status=400)
    
    # Extraer la tasa de cambio de la respuesta
    tasa_cambio = cuadro.iloc[-1]['F073.TCO.PRE.Z.D']
    
    # Realizar la conversión de USD a CLP
    monto_clp = monto_usd * tasa_cambio
    
    # Devolver el monto en pesos chilenos como JSON
    return JsonResponse({'monto_clp': monto_clp, 'tasa_cambio': tasa_cambio})

options = WebpayOptions(settings.TRANSBANK_COMMERCE_CODE, settings.TRANSBANK_API_KEY, IntegrationType.TEST)
transaction = Transaction(options)

@csrf_exempt
@login_required(login_url='/clientes/ingreso/')
def pagar(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

        try:
            data = json.loads(request.body)
            amount = data.get('amount')

            if not amount:
                return JsonResponse({"error": "Monto no proporcionado"}, status=400)

            # Crea la transacción en Transbank
            response = transaction.create(
                buy_order='orden123',
                session_id=request.session.session_key,
                amount=amount,
                return_url=settings.TRANSBANK_RETURN_URL
            )

            redirect_url = response.get('url') + '?token_ws=' + response.get('token')
            if redirect_url:
                return JsonResponse({'redirect_url': redirect_url})
            else:
                return JsonResponse({'error': 'No se pudo obtener la URL de redirección'}, status=500)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud malformada. Se esperaba JSON.'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    
    if not token_ws:
        return HttpResponse('Error: No se encontró el token de la transacción.', status=400)
    
    result = transaction.commit(token_ws)
    
    if result.get('status') == 'AUTHORIZED':
        return HttpResponse('Transacción exitosa')
    else:
        return HttpResponse(f'Error en la transacción: {result.get("status")}')