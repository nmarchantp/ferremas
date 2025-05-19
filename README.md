<h1>Proyecto Django - Ferretería B2B <img src="https://github.com/user-attachments/assets/c78f78e6-bec6-44ab-a08a-f8258d0de698" alt="imagen del proyecto" width="80" height="80" />
</h1>
<p>
Este es un proyecto de Django para la gestión de productos y categorías en una ferretería B2B. 
Incluye funcionalidades para la administración de categorías, productos y un sistema de autenticación 
para acceder al panel de administración.
</p>

<p>
Está desarrollado en Python (framework Django) con base de datos SQLite e integración con Banco Central y Transbank Webpay Plus.
</p>

<h2>Arquitectura</h2>

Elemento	Función principal
HTML	Interfaz visual para el usuario
JavaScript	Lógica en el navegador (AJAX, fetch, SPA)
views.py	Recibe y responde solicitudes web tradicionales o JS
api_views.py	Contiene la lógica de negocio reutilizable y endpoints JSON
models.py	Representa las tablas de la base de datos

Usuario ←→ HTML ←→ views.py (clientes/productos) ←→ api_views.py (lógica) ←→ models.py (DB)
         ↑
      JavaScript (opcional)

<img src="https://github.com/user-attachments/assets/b27042be-9270-442b-a409-c8e0595d6bf0" alt="arquitectura del proyecto" />

<h2>Requisitos Previos</h2>
<ul>
  <li>Python 3.x</li>
  <li>Git</li>
  <li>pip (instalador de paquetes de Python)</li>
  <li>Virtualenv (opcional, pero recomendado)</li>
</ul>

<h2>Instalación y Configuración</h2>

<h3>1. Clonar el Repositorio</h3>
<pre><code>git clone https://github.com/nmarchantp/ferremas.git</code></pre>

<h3>2. Cambiar al Directorio del Proyecto</h3>
<pre><code>cd webFM</code></pre>

<h3>3. Crear y Activar un Entorno Virtual</h3>
<pre><code>
python -m venv env
cd env/Scripts
.\activate
</code></pre>

<h3>4. Instalar Dependencias</h3>
<pre><code>
cd ../../webFM
pip install -r requirements.txt
</code></pre>

<h3>5. Migrar la Base de Datos</h3>
<pre><code>
python manage.py makemigrations
python manage.py migrate
</code></pre>

<h3>6. Cargar los Datos Iniciales</h3>
<pre><code>python load_data.py</code></pre>

<h3>7. Iniciar el Servidor</h3>
<pre><code>
python manage.py runserver
</code></pre>

<h2>Credenciales de Prueba</h2>

<h3>Administrador</h3>
<ul>
  <li>Usuario: admin@example.com</li>
  <li>Password: admin123</li>
</ul>

<h3>Cliente</h3>
<ul>
  <li>Usuario: cliente@example.com</li>
  <li>Password: cliente123</li>
</ul>

<h2>Datos para Simular Compra por Transbank</h2>
<ul>
  <li>VISA: 4051 8856 0044 6623 — CVV 123 — Cualquier fecha — Aprobada</li>
  <li>MASTERCARD: 5186 0595 5959 0568 — CVV 123 — Cualquier fecha — Rechazada</li>
  <li>Redcompra: 4051 8842 3993 7763 — Aprobada (débito)</li>
</ul>
<p>Formulario de autenticación: usar RUT <strong>11.111.111-1</strong> y clave <strong>123</strong></p>

<h2>Comandos Adicionales</h2>

<h3>Eliminar migraciones de productos</h3>
<pre><code>rm productos/migrations/0*.py</code></pre>

<h3>Eliminar archivos temporales</h3>
<pre><code>Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item</code></pre>

<h3>Crear archivo requirements.txt</h3>
<pre><code>pip freeze > requirements.txt</code></pre>
