from django.http import JsonResponse
from webFM.apis.views import convertir

def convertir_api(request):
    monto_usd = float(request.GET.get('monto_usd', 0))  # Obtiene el monto en USD desde la solicitud
    if monto_usd <= 0:
        return JsonResponse({'error': 'Monto en USD no válido'}, status=400)

    try:
        monto_clp = convertir(monto_usd)  # Llama a la función convertir
        return JsonResponse({'monto_clp': monto_clp}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
