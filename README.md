# Proyecto Django - Ferretería B2B

Este es un proyecto de Django para la gestión de productos y categorías en una ferretería B2B. Incluye funcionalidades para la administración de categorías, productos y un sistema de autenticación para acceder al panel de administración.

## Requisitos Previos

- Python 3.x
- Git
- pip (instalador de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

## Instalación y Configuración

Sigue estos pasos para descargar, instalar y ejecutar el proyecto en tu máquina local:

### 1. Clonar el Repositorio

Primero, clona el repositorio desde GitHub:

git clone https://github.com/nmarchantp/ferremas.git

## Cambia al directorio del proyecto:

cd webFM

### 2. Crear y Activar un Entorno Virtual

## Crea un entorno virtual

python -m venv env

## Activa el entorno virtual

cd env
cd Scripts
.\activate

### 3. Instalar Dependencias

pip install -r requirements.txt

### 4. Migrar la Base de Datos

python manage.py makemigrations

python manage.py migrate

### 5. Carga los datos iniciales

python load_data.py

### 6. Inicia el servidor

## Asegúrate de estar en la carpeta webFM

python manage.py runserver



### Adicionales
## Eliminar migraciones de producto
rm productos/migrations/0*.py
## Eliminar archivos temporales
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item
## Crear requeriments.txt por codigo
pip freeze > requirements.txt

