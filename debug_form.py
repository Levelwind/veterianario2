import os
import django
import sys

# Setup Django environment
sys.path.insert(0, r"c:\Users\Sebas\Downloads\veterinaria\veterinaria")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "veterinaria.settings")
django.setup()

from apps.usuarios.forms import CrearVeterinarioForm

# Mock POST data for the form
data = {
    'first_name': 'Juan',
    'last_name': 'Perez',
    'email': 'juan@veterinaria.test',
    'telefono': '3001234567',
    'numero_licencia': 'VET-12345',
    'especialidad': 'general',
    'password1': 'Admin2024!',
    'password2': 'Admin2024!'
}

form = CrearVeterinarioForm(data)
if form.is_valid():
    print("Form is valid.")
    # Try to save without committing to check for IntegrityErrors
    try:
        user = form.save(commit=False)
        print("User object created:", user)
    except Exception as e:
        print("Error during save:", e)
else:
    print("Form is INVALID.")
    print("Errors:", form.errors)
