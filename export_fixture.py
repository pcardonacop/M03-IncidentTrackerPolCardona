import subprocess
import sys
import json

# Executa dumpdata i captura la sortida
result = subprocess.run(
    [sys.executable, 'manage.py', 'dumpdata', 'auth.User', '--natural-foreign', '--indent', '4'],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

if result.returncode != 0:
    print("Error en dumpdata:", result.stderr)
    sys.exit(1)

# Escriu el fitxer en UTF-8 sense BOM
with open('testdb.json', 'w', encoding='utf-8') as f:
    f.write(result.stdout)

print("Fitxer testdb.json generat correctament (UTF-8 sense BOM).")