# Generated by Django 5.1.2 on 2024-10-30 00:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_interno', models.CharField(max_length=10, null=True, unique=True)),
                ('nombre_categoria', models.CharField(max_length=255)),
                ('estado_categoria', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_interno', models.CharField(blank=True, max_length=50)),
                ('nombre_producto', models.CharField(max_length=255)),
                ('descripcion_producto', models.CharField(blank=True, max_length=300)),
                ('estado_producto', models.BooleanField(default=True)),
                ('precio_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidad_pack', models.IntegerField()),
                ('imagen_producto', models.ImageField(blank=True, null=True, upload_to='producto/')),
                ('categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.categoria')),
            ],
            options={
                'unique_together': {('categoria_producto', 'codigo_interno')},
            },
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
    ]
