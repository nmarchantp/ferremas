from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion_producto', 'precio_producto', 'unidad_pack', 'categoria_producto', 'imagen_producto']