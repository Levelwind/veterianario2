"""
Script para crear datos de prueba.
Ejecutar con: python manage.py shell < scripts/crear_datos.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria.settings')
django.setup()

from apps.usuarios.models import Usuario, PerfilVeterinario
from apps.mascotas.models import Mascota
from apps.citas.models import Cita
from django.utils import timezone
from datetime import date, time, timedelta

print("🔧 Creando datos de prueba para VetCare...")

# ---- Admin ----
if not Usuario.objects.filter(email='admin@vetcare.com').exists():
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@vetcare.com',
        password='Admin2024!',
        first_name='Admin',
        last_name='VetCare',
        rol='administrador',
    )
    print(f"✅ Admin creado: admin@vetcare.com / Admin2024!")
else:
    admin = Usuario.objects.get(email='admin@vetcare.com')
    print("ℹ️  Admin ya existe.")

# ---- Veterinarios ----
vets_data = [
    {'email': 'dra.garcia@vetcare.com', 'first_name': 'María', 'last_name': 'García',
     'licencia': 'VET-001', 'especialidad': 'general'},
    {'email': 'dr.rodriguez@vetcare.com', 'first_name': 'Carlos', 'last_name': 'Rodríguez',
     'licencia': 'VET-002', 'especialidad': 'cirugia'},
    {'email': 'dra.lopez@vetcare.com', 'first_name': 'Sofía', 'last_name': 'López',
     'licencia': 'VET-003', 'especialidad': 'dermatologia'},
]

veterinarios = []
for v in vets_data:
    if not Usuario.objects.filter(email=v['email']).exists():
        vet = Usuario.objects.create_user(
            username=v['email'].split('@')[0],
            email=v['email'],
            password='Vet2024!',
            first_name=v['first_name'],
            last_name=v['last_name'],
            rol='veterinario',
        )
        PerfilVeterinario.objects.create(
            usuario=vet,
            numero_licencia=v['licencia'],
            especialidad=v['especialidad'],
            horario_inicio=time(8, 0),
            horario_fin=time(18, 0),
            dias_laborales=[0, 1, 2, 3, 4],
            duracion_cita=30,
        )
        veterinarios.append(vet)
        print(f"✅ Veterinario: {v['email']} / Vet2024!")
    else:
        veterinarios.append(Usuario.objects.get(email=v['email']))
        print(f"ℹ️  Veterinario {v['email']} ya existe.")

# ---- Clientes ----
clientes_data = [
    {'email': 'juan.perez@gmail.com', 'first_name': 'Juan', 'last_name': 'Pérez'},
    {'email': 'ana.martinez@gmail.com', 'first_name': 'Ana', 'last_name': 'Martínez'},
    {'email': 'pedro.gomez@gmail.com', 'first_name': 'Pedro', 'last_name': 'Gómez'},
]

clientes = []
for c in clientes_data:
    if not Usuario.objects.filter(email=c['email']).exists():
        cliente = Usuario.objects.create_user(
            username=c['email'].split('@')[0],
            email=c['email'],
            password='Cliente2024!',
            first_name=c['first_name'],
            last_name=c['last_name'],
            rol='cliente',
        )
        clientes.append(cliente)
        print(f"✅ Cliente: {c['email']} / Cliente2024!")
    else:
        clientes.append(Usuario.objects.get(email=c['email']))
        print(f"ℹ️  Cliente {c['email']} ya existe.")

# ---- Mascotas ----
mascotas_data = [
    {'dueno': clientes[0], 'nombre': 'Rocky', 'especie': 'perro', 'raza': 'Labrador', 'sexo': 'macho'},
    {'dueno': clientes[0], 'nombre': 'Luna', 'especie': 'gato', 'raza': 'Persa', 'sexo': 'hembra'},
    {'dueno': clientes[1], 'nombre': 'Max', 'especie': 'perro', 'raza': 'Golden Retriever', 'sexo': 'macho'},
    {'dueno': clientes[2], 'nombre': 'Mimi', 'especie': 'gato', 'raza': 'Siamés', 'sexo': 'hembra'},
]

mascotas = []
for m in mascotas_data:
    if not Mascota.objects.filter(nombre=m['nombre'], dueno=m['dueno']).exists():
        mascota = Mascota.objects.create(**m)
        mascotas.append(mascota)
        print(f"✅ Mascota: {m['nombre']} ({m['especie']}) de {m['dueno'].get_full_name()}")
    else:
        mascotas.append(Mascota.objects.get(nombre=m['nombre'], dueno=m['dueno']))

# ---- Cita de prueba (mañana) ----
manana = date.today() + timedelta(days=1)
if not Cita.objects.filter(mascota=mascotas[0], fecha=manana).exists():
    try:
        cita = Cita(
            mascota=mascotas[0],
            veterinario=veterinarios[0],
            cliente=clientes[0],
            fecha=manana,
            hora_inicio=time(10, 0),
            hora_fin=time(10, 30),
            tipo='consulta_general',
            estado='confirmada',
            motivo='Consulta de rutina y vacunación',
        )
        cita.full_clean()
        cita.save()
        print(f"✅ Cita de prueba creada para mañana ({manana})")
    except Exception as e:
        print(f"⚠️  No se pudo crear la cita de prueba: {e}")

print("\n🎉 Datos de prueba creados exitosamente.")
print("\n📋 CREDENCIALES DE ACCESO:")
print("  Admin:       admin@vetcare.com     / Admin2024!")
print("  Veterinario: dra.garcia@vetcare.com / Vet2024!")
print("  Cliente:     juan.perez@gmail.com  / Cliente2024!")
print("\n⚠️  IMPORTANTE: Cambia estas contraseñas en producción.")
