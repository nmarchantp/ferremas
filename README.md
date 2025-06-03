<h1>Proyecto Django - Ferretería B2B 👨‍💼<img src="https://github.com/user-attachments/assets/c78f78e6-bec6-44ab-a08a-f8258d0de698" alt="imagen del proyecto" width="30" height="30" /></h1>

Este es un proyecto de Django para la gestión de productos y categorías en una ferretería B2B.
Incluye funcionalidades para la administración de categorías, productos y un sistema de autenticación
para acceder al panel de administración.

Está desarrollado en Python (framework Django) que consume una API con base de datos SQLite e integración con Banco Central y Transbank Webpay Plus.
<a href="https://github.com/nmarchantp/API-ferremas_">Visitar Github de API Ferremas</a>


---

## 🧱 Arquitectura

| 🧹 Elemento          | 📌 Función principal                                        |
| -------------------- | ----------------------------------------------------------- |
| 🌐 **HTML**          | Interfaz visual para el usuario                             |
| 🧠 **JavaScript**    | Lógica en el navegador (AJAX, fetch, SPA)                   |
| 🥭 **views.py**      | Recibe y responde solicitudes web tradicionales o JS        |
| 🔁 **API-ferremas ** | Contiene la lógica de negocio reutilizable y endpoints JSON |
| 📃 **models.py**     | Representa las tablas de la base de datos                   |

```
🧍 Usuario
   ↓
🌐 HTML (formularios, botones)
   ↓
🥭 views.py (maneja la petición)
   ↓
🔁 API-ferremas (lógica reutilizable)
   ↓
📃 models.py (base de datos)

📆 JavaScript puede enviar datos directamente a views o api_views si usas fetch/AJAX.
```

![arquitectura del proyecto](https://github.com/user-attachments/assets/b27042be-9270-442b-a409-c8e0595d6bf0)

---

## ⚙️ Requisitos Previos

* Python 3.x
* Git
* pip (instalador de paquetes de Python)
* Virtualenv (opcional, pero recomendado)

---

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/nmarchantp/ferremas.git
```

### 2. Cambiar al Directorio del Proyecto

```bash
cd webFM
```

### 3. Crear y Activar un Entorno Virtual

```bash
python -m venv env
cd env/Scripts
.\activate
```

### 4. Instalar Dependencias

```bash
cd ../../webFM
pip install -r requirements.txt
```

### 5. Migrar la Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Cargar los Datos Iniciales

```bash
python load_data.py
```

### 7. Iniciar el Servidor

```bash
python manage.py runserver
```

---

## 🔐 Credenciales de Prueba

### Administrador

* Usuario: `admin@example.com`
* Password: `admin123`

### Cliente

* Usuario: `cliente@example.com`
* Password: `cliente123`

---

## 💳 Datos para Simular Compra por Transbank

* **VISA:** 4051 8856 0044 6623 — CVV 123 — Cualquier fecha — ✅ Aprobada
* **MASTERCARD:** 5186 0595 5959 0568 — CVV 123 — ❌ Rechazada
* **Redcompra (débito):** 4051 8842 3993 7763 — ✅ Aprobada

> Formulario de autenticación: usar RUT **11.111.111-1** y clave **123**

---

## 🧰 Comandos Adicionales

### Eliminar migraciones de productos

```bash
rm productos/migrations/0*.py
```

### Eliminar archivos temporales `.pyc`

```powershell
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item
```

### Crear archivo `requirements.txt`

```bash
pip freeze > requirements.txt
```
