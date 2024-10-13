from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=255)
    estado_categoria = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    estado_producto = models.BooleanField(default=True)  
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_producto
    

