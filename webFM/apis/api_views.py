# apis/api_views.py

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from clientes.models import Cliente
from productos.models import Producto
import json

### -----------------------------
### CLIENTES - API INTERNA
### -----------------------------

def crear_cliente(username, email, password, nombre=None):
    """
    Crea un nuevo usuario y un cliente asociado.
    """
    user = User.objects.create_user(username=username, email=email, password=password)
    cliente = Cliente.objects.create(user=user, nombre=nombre)
    return cliente


def autenticar_por_email(email, password):
    """
    Autentica un usuario utilizando su email en lugar de su username.
    """
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def obtener_cliente_por_usuario(user):
    """
    Retorna el objeto Cliente asociado a un usuario dado.
    """
    try:
        return Cliente.objects.get(user=user)
    except Cliente.DoesNotExist:
        return None


def obtener_cliente_por_id(cliente_id):
    """
    Retorna el objeto Cliente por su ID (si existe).
    """
    try:
        return Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return None


def listar_clientes():
    """
    Retorna todos los clientes.
    """
    return Cliente.objects.select_related('user').all()


@login_required
def api_perfil_cliente(request):
    """
    Devuelve el perfil del cliente autenticado (JSON).
    """
    cliente = obtener_cliente_por_usuario(request.user)
    if cliente:
        data = {
            'id': cliente.id,
            'username': cliente.user.username,
            'email': cliente.user.email,
            'nombre': cliente.nombre,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


@login_required
def api_cliente_por_id(request, cliente_id):
    """
    Devuelve el detalle de un cliente por ID.
    """
    cliente = obtener_cliente_por_id(cliente_id)
    if cliente:
        data = {
            'id': cliente.id,
            'username': cliente.user.username,
            'email': cliente.user.email,
            'nombre': cliente.nombre,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


@login_required
def api_listar_clientes(request):
    """
    Lista todos los clientes. Solo accesible para superusuarios.
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Acceso no autorizado'}, status=403)

    clientes = listar_clientes()
    data = [{
        'id': c.id,
        'username': c.user.username,
        'email': c.user.email,
        'nombre': c.nombre,
    } for c in clientes]
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def api_actualizar_perfil_cliente(request):
    """
    Permite al cliente autenticado actualizar su perfil (nombre, email, contraseña).
    """
    if request.method != 'PUT':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        import json
        data = json.loads(request.body)
        cliente = obtener_cliente_por_usuario(request.user)

        if not cliente:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

        # Actualizar campos del perfil
        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.user.email = data.get('email', cliente.user.email)

        nueva_contraseña = data.get('password', None)
        if nueva_contraseña:
            cliente.user.set_password(nueva_contraseña)

        cliente.save()
        cliente.user.save()

        return JsonResponse({'mensaje': 'Perfil actualizado correctamente'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
### -----------------------------
### FIN CLIENTES - API INTERNA
### -----------------------------

### -----------------------------
### PRODUCTOS - API INTERNA
### -----------------------------

def listar_productos():
    return Producto.objects.all()


def obtener_producto_por_id(id_producto):
    return get_object_or_404(Producto, id_producto=id_producto)


def crear_producto(data):
    producto = Producto.objects.create(
        nombre_producto=data['nombre'],
        descripcion_producto=data.get('descripcion', ''),
        estado_producto=data.get('estado', True),
        precio_producto=data['precio'],
        unidad_pack=data['unidad'],
        categoria_producto_id=data['categoria_id'],  # cuidado: validar existencia
        imagen_producto=data.get('imagen')  # opcional
    )
    return producto


def actualizar_producto(producto, data):
    producto.nombre_producto = data.get('nombre', producto.nombre_producto)
    producto.descripcion_producto = data.get('descripcion', producto.descripcion_producto)
    producto.estado_producto = data.get('estado', producto.estado_producto)
    producto.precio_producto = data.get('precio', producto.precio_producto)
    producto.unidad_pack = data.get('unidad', producto.unidad_pack)
    producto.categoria_producto_id = data.get('categoria_id', producto.categoria_producto_id)
    producto.save()
    return producto


def eliminar_producto(producto_id):
    producto = Producto.objects.get(id_producto=producto_id)
    producto.delete()


@login_required
def api_listar_productos(request):
    productos = listar_productos()
    data = [{
        'id': p.id_producto,
        'nombre': p.nombre_producto,
        'descripcion': p.descripcion_producto,
        'precio': float(p.precio_producto),
        'unidad': p.unidad_pack,
        'categoria_id': p.categoria_producto_id,
        'imagen': p.imagen_producto.url if p.imagen_producto else None
    } for p in productos]
    return JsonResponse(data, safe=False)


@login_required
def api_producto_por_id(request, producto_id):
    try:
        producto = obtener_producto_por_id(producto_id)
        data = {
            'id': producto.id_producto,
            'nombre': producto.nombre_producto,
            'descripcion': producto.descripcion_producto,
            'precio': float(producto.precio_producto),
            'unidad': producto.unidad_pack,
            'categoria_id': producto.categoria_producto_id,
            'imagen': producto.imagen_producto.url if producto.imagen_producto else None
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


@csrf_exempt
@login_required
def api_crear_producto(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        producto = crear_producto(data)
        return JsonResponse({'mensaje': 'Producto creado', 'id': producto.id_producto}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@login_required
def api_actualizar_producto(request, producto_id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        producto = obtener_producto_por_id(producto_id)
        data = json.loads(request.body)
        producto = actualizar_producto(producto, data)
        return JsonResponse({'mensaje': 'Producto actualizado', 'id': producto.id_producto})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@login_required
def api_eliminar_producto(request, producto_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        eliminar_producto(producto_id)
        return JsonResponse({'mensaje': 'Producto eliminado'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
### -----------------------------
### FIN PRODUCTOS - API INTERNA
### -----------------------------
