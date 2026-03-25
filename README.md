# 🐾 VetCare — Sistema de Gestión Veterinaria

Sistema web completo desarrollado en **Django 5** para la clínica veterinaria de Ibagué.
Incluye tres paneles diferenciados (Cliente, Veterinario, Administrador), autenticación en dos pasos (2FA), login social con Google, y reglas de negocio para el agendamiento de citas.

---

## 📋 Tabla de Contenidos

1. [Requisitos del sistema](#1-requisitos-del-sistema)
2. [Instalación paso a paso](#2-instalación-paso-a-paso)
3. [Configuración de base de datos (Supabase)](#3-configuración-de-base-de-datos-supabase)
4. [Configurar autenticación social (Google)](#4-configurar-autenticación-social-google)
5. [Crear datos de prueba](#5-crear-datos-de-prueba)
6. [Ejecutar el servidor](#6-ejecutar-el-servidor)
7. [Estructura del proyecto](#7-estructura-del-proyecto)
8. [Paneles y funcionalidades](#8-paneles-y-funcionalidades)
9. [Reglas de negocio](#9-reglas-de-negocio)
10. [API REST](#10-api-rest)
11. [Despliegue en producción](#11-despliegue-en-producción)
12. [Solución de problemas frecuentes](#12-solución-de-problemas-frecuentes)

---

## 1. Requisitos del sistema

Antes de comenzar, asegúrate de tener instalado:

| Herramienta | Versión mínima | Verificar con |
|-------------|----------------|---------------|
| Python      | 3.10+          | `python --version` |
| pip         | 23+            | `pip --version` |
| Git         | cualquiera     | `git --version` |

> En Windows se recomienda usar Git Bash o PowerShell.

---

## 2. Instalación paso a paso

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/vetcare.git
cd vetcare
```

### Paso 2 — Crear el entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat
```

Cuando el entorno esté activo verás `(venv)` al inicio de la línea de comandos.

### Paso 3 — Instalar dependencias

```bash
pip install -r requirements.txt
pip install requests PyJWT cryptography 
```

Este proceso puede tardar 1-2 minutos.Instala Django, django-allauth, django-two-factor-auth, djangorestframework , crispy-forms y más.
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

### Paso 4 — Crear las migraciones y la base de datos
pip install PyJWT
pip install requests
```bash
python manage.py makemigrations usuarios
python manage.py makemigrations mascotas
python manage.py makemigrations citas
python manage.py migrate
```

> **¿Por qué en ese orden?** La app `usuarios` define el modelo `Usuario` personalizado, del cual dependen `mascotas` y `citas`. Siempre migra `usuarios` primero.

### Paso 5 — Crear el superusuario administrador

```bash
python manage.py createsuperuser
```

Te pedirá:
- **Email**: pon tu correo (es el campo de login)
- **Username**: cualquier nombre de usuario
- **First name / Last name**: tu nombre
- **Password**: mínimo 8 caracteres, no demasiado simple

> Después de crearlo, entra al admin `/admin/` y en la sección **Usuarios**, cambia el campo **Rol** a `administrador`.

### Paso 6 — Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

---

## 3. Configuración de base de datos (Supabase)

Por defecto el proyecto usa SQLite (archivo `db.sqlite3`), que funciona perfectamente para desarrollo. Para producción o para usar **Supabase (PostgreSQL)**:

### Paso 1 — Crea tu proyecto en Supabase

1. Ve a [https://supabase.com](https://supabase.com) y crea una cuenta gratuita.
2. Haz clic en **New Project**.
3. Anota los datos de conexión: `Host`, `Database name`, `User`, `Password`, `Port`.

### Paso 2 — Edita `veterinaria/settings.py`

Busca la sección de base de datos y **comenta SQLite, descomenta PostgreSQL**:

```python
# Comenta esto:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Descomenta y rellena esto:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'TU_PASSWORD_SUPABASE',
        'HOST': 'db.XXXXXX.supabase.co',   # lo encuentras en Supabase → Settings → Database
        'PORT': '5432',
    }
}
```

### Paso 3 — Migrar a Supabase

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 4. Configurar autenticación social (Google)

### 4.1 Google OAuth

#### Crear credenciales en Google Cloud Console:

1. Ve a [https://console.cloud.google.com](https://console.cloud.google.com)
2. Crea un nuevo proyecto o selecciona uno existente.
3. En el menú lateral: **APIs y servicios → Credenciales**.
4. Haz clic en **+ CREAR CREDENCIALES → ID de cliente de OAuth**.
5. Tipo de aplicación: **Aplicación web**.
6. Nombre: `VetCare`.
7. En **Orígenes JavaScript autorizados**: `http://localhost:8000`
8. En **URIs de redirección autorizados**: `http://localhost:8000/cuentas/google/login/callback/`
9. Haz clic en **CREAR** y anota el **Client ID** y **Client Secret**.

#### Configurar en el proyecto:

**Opción A — Variables de entorno (recomendado):**

Crea un archivo `.env` en la raíz del proyecto (nunca lo subas a GitHub):

```env
GOOGLE_CLIENT_ID=tu-client-id-de-google.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret-de-google
```

**Opción B — Directamente en settings.py:**

En `veterinaria/settings.py`, busca `SOCIALACCOUNT_PROVIDERS` y reemplaza los valores:

```python
'APP': {
    'client_id': 'PEGA_AQUÍ_TU_CLIENT_ID',
    'secret': 'PEGA_AQUÍ_TU_CLIENT_SECRET',
    'key': '',
},
```

#### Registrar en Django Admin:

1. Ejecuta el servidor: `python manage.py runserver`
2. Ve a `http://localhost:8000/admin/`
3. En **Sites**, edita el sitio por defecto y pon: `Domain: localhost:8000`, `Display name: VetCare Local`.
4. En **Social applications**, haz clic en **+ Agregar**:
   - Provider: `Google`
   - Name: `Google`
   - Client id: tu Client ID
   - Secret key: tu Client Secret
   - Mueve el site de "Available" a "Chosen"
   - Guarda.

---

## 5. Crear datos de prueba

Para tener datos de ejemplo (admin, veterinarios, clientes, mascotas y una cita):

```bash
python manage.py shell < scripts/crear_datos.py
```

Esto crea los siguientes usuarios:

| Rol           | Email                       | Contraseña      |
|---------------|-----------------------------|-----------------|
| Administrador | admin@vetcare.com           | Admin2024!      |
| Veterinario   | levelwind55@gmail.com       | vet1234.        |
| Cliente       | sebastiansxd8@gmail.com     | levelwind.      |
 test               test2fa@vetcare.com        TestPassword123! |
 veterinario        laura.mendoza@vetcare.com   LauraVet123!
  veterinario     andres.quiroga@vetcare.com      AndresVet123!        
  veterianrio   camila.rojas@vetcare.com       CamilaVet123!
> ⚠️ **IMPORTANTE**: Estas contraseñas son solo para pruebas. Cámbialas antes de poner el proyecto en producción.

---

## 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre el navegador en: **http://localhost:8000**

| URL                              | Descripción                      |
|----------------------------------|----------------------------------|
| http://localhost:8000/cuentas/login/ | Inicio de sesión con 2FA       |
| http://localhost:8000/registro/  | Registro de nuevos clientes      |
| http://localhost:8000/dashboard/ | Panel principal (según rol)      |
| http://localhost:8000/admin/     | Panel de administración Django   |
| http://localhost:8000/citas/     | Listado de citas                 |
| http://localhost:8000/mascotas/  | Listado de mascotas              |
| http://localhost:8000/api/       | API REST con Token Auth          |

---

## 7. Estructura del proyecto

```
vetcare/
├── veterinaria/                  # Configuración principal del proyecto
│   ├── settings.py               # Configuración (DB, apps, auth, email)
│   ├── urls.py                   # URLs raíz del proyecto
│   └── wsgi.py                   # Punto de entrada WSGI
│
├── apps/
│   ├── usuarios/                 # App de usuarios y autenticación
│   │   ├── models.py             # Usuario personalizado + PerfilVeterinario
│   │   ├── views.py              # Registro, perfil, gestión de usuarios
│   │   ├── forms.py              # Formularios de registro y perfil
│   │   ├── decorators.py         # @solo_administrador, @solo_veterinario_o_admin
│   │   ├── urls.py               # URLs de la app
│   │   ├── api_views.py          # Endpoint /api/usuarios/
│   │   └── api_urls.py           # URLs de la API
│   │
│   ├── mascotas/                 # App de mascotas
│   │   ├── models.py             # Mascota, HistorialMedico, Vacuna
│   │   ├── views.py              # CRUD mascotas + historial + vacunas
│   │   ├── forms.py              # Formularios
│   │   └── urls.py
│   │
│   ├── citas/                    # App de citas médicas
│   │   ├── models.py             # Cita + HorarioDisponible (con validaciones)
│   │   ├── views.py              # Agendar, listar, detalle, cancelar citas
│   │   ├── forms.py              # Formularios con validación de horarios
│   │   ├── api_views.py          # API REST de citas
│   │   └── urls.py
│   │
│   └── dashboard/                # App del panel principal
│       ├── views.py              # Vista que redirige por rol
│       └── urls.py
│
├── templates/                    # Plantillas HTML
│   ├── base.html                 # Layout principal con sidebar
│   ├── dashboard/                # Paneles por rol
│   ├── citas/                    # Templates de citas
│   ├── mascotas/                 # Templates de mascotas
│   ├── usuarios/                 # Templates de usuarios
│   ├── two_factor/               # Login 2FA y setup
│   └── account/                  # Recuperación de contraseña
│
├── static/
│   ├── css/main.css              # Estilos del sistema
│   └── js/main.js                # JavaScript (sidebar, horarios dinámicos)
│
├── scripts/
│   └── crear_datos.py            # Script de datos de prueba
│
├── requirements.txt              # Dependencias Python
└── manage.py                     # Herramienta de gestión Django
```

---

## 8. Paneles y funcionalidades

### Panel Cliente
- Ver mis mascotas y registrar nuevas
- **Agendar cita**: seleccionar veterinario, ver horarios disponibles en tiempo real, elegir slot
- Ver todas mis citas (próximas, pasadas, activas)
- Ver detalle de cada cita
- Cancelar citas pendientes o confirmadas
- Ver historial médico (diagnósticos, tratamientos)
- **Antecedentes básicos de salud**: vacunas al día, detalle de vacunas, esterilización y última desparasitación.
- Ver vacunas registradas en bloques de alertas.
- Editar mi perfil personal
- Activar/gestionar autenticación en dos pasos

### Panel Veterinario
- Ver citas del día con información completa: nombre de la mascota, especie, raza, peso, alergias, enfermedades crónicas, dueño con teléfono
- Ver próximas citas
- Acceder al detalle de cada cita y actualizar el estado
- Agregar diagnóstico, tratamiento y medicamentos (registra historial médico)
- Agregar vacunas a los pacientes
- Configurar perfil profesional: especialidad, horario, días laborales, duración de citas
- Ver lista de pacientes (mascotas que han atendido)

### Panel Administrador
- Dashboard con estadísticas: total clientes, veterinarios, mascotas, citas del día, pendientes
- Ver y filtrar todas las citas del sistema
- Gestionar usuarios: activar/desactivar, filtrar por rol
- Crear nuevos veterinarios con su perfil profesional
- Ver detalle de cada veterinario

---

## 9. Reglas de negocio

Implementadas en `apps/citas/models.py` método `clean()`:

### Regla 1 — Una mascota solo puede tener una cita activa a la vez

Si una mascota tiene una cita en estado `pendiente`, `confirmada` o `en_proceso`, el sistema **rechaza** cualquier intento de agendar otra cita para esa mascota hasta que la cita actual sea completada o cancelada.

```
Error: "La mascota Rocky ya tiene una cita activa (#12). Cancela la cita anterior primero."
```

### Regla 2 — El veterinario no puede tener dos citas al mismo tiempo

El sistema verifica que el veterinario no tenga otra cita cuyo horario se solape con la nueva. Dos citas se solapan si `hora_inicio_nueva < hora_fin_existente AND hora_fin_nueva > hora_inicio_existente`.

```
Error: "El Dr(a). María García ya tiene una cita ese día de 10:00 a 10:30. Por favor elige otro horario."
```

### Regla 3 — No se pueden agendar citas en el pasado

```
Error: "No puedes agendar una cita en una fecha pasada."
```

### Regla 4 — La hora de fin debe ser posterior a la de inicio

### Regla 5 — Verificación de días laborales del veterinario

En el formulario de agendamiento se verifica que la fecha seleccionada corresponda a un día en que el veterinario atiende.

---

## 10. API REST

La API usa autenticación por **Token**.

### Obtener token

```bash
curl -X POST http://localhost:8000/api/usuarios/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez@gmail.com", "password": "Cliente2024!"}'
```

Respuesta:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 5,
  "email": "juan.perez@gmail.com",
  "rol": "cliente",
  "nombre": "Juan Pérez"
}
```

### Endpoints disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| `POST` | `/api/usuarios/token/` | Obtener token de autenticación |
| `GET`  | `/api/usuarios/veterinarios/` | Listar veterinarios activos |
| `GET`  | `/api/citas/` | Mis citas (filtradas por rol) |
| `POST` | `/api/citas/` | Crear nueva cita |
| `GET`  | `/api/citas/{id}/` | Detalle de cita |
| `PATCH`| `/api/citas/{id}/` | Actualizar estado/notas de cita |
| `GET`  | `/api/horarios/?veterinario_id=1&fecha=2024-12-20` | Horarios disponibles |

### Ejemplo con token

```bash
curl http://localhost:8000/api/citas/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

---

## 11. Despliegue en producción

### Variables de entorno recomendadas

Crea el archivo `.env` (nunca subir a GitHub):

```env
SECRET_KEY=genera-una-clave-secreta-muy-larga-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://usuario:password@host:5432/dbname
GOOGLE_CLIENT_ID=tu-google-client-id
GOOGLE_CLIENT_SECRET=tu-google-client-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Cambios en settings.py para producción

```python
DEBUG = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Usar WhiteNoise para servir estáticos
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Comandos de despliegue

```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn veterinaria.wsgi:application --bind 0.0.0.0:8000
```

---

## 12. Solución de problemas frecuentes

### ❌ Error: `No module named 'allauth'`
```bash
pip install -r requirements.txt
```

### ❌ Error al migrar: campo AUTH_USER_MODEL
Si cambias `AUTH_USER_MODEL` después de haber hecho migraciones:
```bash
# Elimina la base de datos y vuelve a migrar
rm db.sqlite3
python manage.py migrate
```

### ❌ Error: `SITE_ID` — Sites matching query does not exist
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.create(domain='localhost:8000', name='VetCare Local')
```

### ❌ Error de login con Google: `SocialApp matching query does not exist`
Debes registrar la app social en el admin de Django. Ve a `http://localhost:8000/admin/socialaccount/socialapp/` y agrega la app.

### ❌ Error: `phonenumbers` o campos de teléfono
Asegúrate de tener `django-phonenumber-field` instalado:
```bash
pip install django-phonenumber-field phonenumbers
```

### ❌ El código QR de 2FA no aparece
```bash
pip install qrcode Pillow
```

### ❌ Imágenes no se muestran
En desarrollo, agrega a `urls.py` (ya está configurado):
```python
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### ❌ El filtro `user.es_cliente` no funciona en templates
Asegúrate que el modelo `Usuario` tenga el método definido. Usa `user.es_cliente` (sin paréntesis) en templates Django.

---

## 🔐 Seguridad — Lista de verificación antes de producción

- [ ] Cambiar `SECRET_KEY` por una aleatoria segura
- [ ] Establecer `DEBUG = False`
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Cambiar todas las contraseñas de prueba
- [ ] Activar HTTPS y cambiar `ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'`
- [ ] Configurar email SMTP real (no console)
- [ ] Usar variables de entorno para credenciales (nunca hardcodear)
- [ ] Ejecutar `python manage.py check --deploy`

---

## 📞 Integrantes del Grupo 1

- Castaño Vargas Sebastian
- Díaz Espinosa Samuel Ricardo
- Forero Lopez Andrés Felipe

**Curso**: Sistema de Gestión de Veterinaria — Ibagué

---

> **VetCare** — Sistema desarrollado con Django 5, Bootstrap 5, django-allauth, django-two-factor-auth y Django REST Framework.