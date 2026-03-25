import os
import sys
from pathlib import Path
import django
from django.db import connection

# Add project root to sys.path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria.settings')
django.setup()

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]
        with open('scripts/tables_list.txt', 'w') as f:
            for table in sorted(tables):
                f.write(f"{table}\n")
        print(f"List of {len(tables)} tables saved to scripts/tables_list.txt")

if __name__ == "__main__":
    list_tables()
