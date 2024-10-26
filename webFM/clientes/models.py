from django.contrib.auth.models import User
from django.db import models

# Si deseas agregar campos personalizados
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)  # Agregar campo nombre

    def __str__(self):
        return self.user.username  # O cualquier otra representación