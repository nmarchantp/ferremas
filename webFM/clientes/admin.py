from django.contrib import admin
from .models import Cliente

# Registrar el modelo Cliente en el admin
admin.site.register(Cliente)
