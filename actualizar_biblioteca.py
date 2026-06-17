import subprocess
import sys
from datetime import datetime

print("Actualizando biblioteca.json...")
resultado = subprocess.run(
    [sys.executable, "test_drive.py"]
)

if resultado.returncode != 0:
    print("ERROR al generar biblioteca.json")
    sys.exit(1)

print("Generando index.html...")
resultado = subprocess.run(
    [sys.executable, "biblioteca_akf.py"]
)

if resultado.returncode != 0:
    print("ERROR al generar index.html")
    sys.exit(1)

print("Publicando en GitHub...")

# git add .
subprocess.run(["git", "add", "."])

# mensaje con fecha y hora
fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
mensaje = f"Actualización automática {fecha}"

# git commit
resultado = subprocess.run(
    ["git", "commit", "-m", mensaje]
)

# Si no hay cambios, Git devuelve error, pero no queremos detenernos
if resultado.returncode == 0:
    subprocess.run(["git", "push"])
    print("Cambios publicados en GitHub.")
else:
    print("No hay cambios para publicar.")

print()
print("===================================")
print("Biblioteca actualizada correctamente")
print("===================================")
input()