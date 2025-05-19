import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
import bcchapi
from .transbank import transaction

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

            response = transaction.create(
                buy_order='orden123',
                session_id=request.session.session_key,
                amount=amount,
                return_url=settings.TRANSBANK_RETURN_URL
            )

            redirect_url = f"{response.get('url')}?token_ws={response.get('token')}"
            return JsonResponse({'redirect_url': redirect_url})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud malformada. Se esperaba JSON.'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    
    # Si no se encuentra el token, muestra una página de error
    if not token_ws:
        return render(request, 'apis/failure.html', {'error_message': 'No se encontró el token de la transacción.'})

    # Confirma la transacción con Transbank
    result = transaction.commit(token_ws)
    
    # Si la transacción fue exitosa
    if result.get('status') == 'AUTHORIZED':
        amount = result.get('amount')  # Obtén el monto de la transacción

        #Limpiar carrito
        if 'carrito' in request.session:
            del request.session['carrito']
        if 'cart_count' in request.session:
            del request.session['cart_count']
        request.session.modified = True

        return render(request, 'apis/success.html', {
            'token_ws': token_ws,
            'amount': amount
        })
    else:
        # Si la transacción falló, muestra una página de error con el estado
        error_status = result.get("status")
        return render(request, 'apis/failure.html', {
            'error_message': f"Error en la transacción: {error_status}"
        })