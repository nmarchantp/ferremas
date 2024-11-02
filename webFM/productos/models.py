from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=10, null=True, unique=True)
    nombre_categoria = models.CharField(max_length=255)
    estado_categoria = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=50, blank=True)
    nombre_producto = models.CharField(max_length=255)
    descripcion_producto = models.CharField(max_length=300, blank=True)
    estado_producto = models.BooleanField(default=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_pack = models.IntegerField()
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_producto = models.ImageField(upload_to='producto/', blank=True,null=True)

    class Meta:
        unique_together = ('categoria_producto', 'codigo_interno')

    def save(self, *args, **kwargs):
        if not self.codigo_interno:
            categoria_codigo = self.categoria_producto.codigo_interno
            productos_en_categoria = Producto.objects.filter(categoria_producto=self.categoria_producto).count() + 1
            numero = f"{productos_en_categoria:04d}"
            self.codigo_interno = f"{categoria_codigo}-{numero}"

        super().save(*args, **kwargs)
    
    def get_id_producto(self):
        return self.id_producto

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre_producto} ({self.cantidad})"
