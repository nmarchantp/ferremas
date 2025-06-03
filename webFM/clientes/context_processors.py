def cliente_en_contexto(request):
    return {
        'cliente_logeado': request.session.get('cliente')
    }
