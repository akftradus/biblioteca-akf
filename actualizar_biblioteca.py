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
status = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

if not status.stdout.strip():
    print("No hay cambios para publicar.")
    sys.exit(0)

# mensaje con fecha y hora
fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
mensaje = f"Actualización automática {fecha}"

# git commit
# Añadir SOLO cambios reales (no todo)
subprocess.run(["git", "add", "-u"])

fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
mensaje = f"Actualización automática {fecha}"

commit = subprocess.run(["git", "commit", "-m", mensaje])

if commit.returncode != 0:
    print("No hay cambios para commitear.")
    sys.exit(0)

push = subprocess.run(["git", "push"])

if push.returncode == 0:
    print("Cambios publicados en GitHub.")
else:
    print("ERROR al publicar en GitHub.")
    sys.exit(1)

print()
print("===================================")
print("Biblioteca actualizada correctamente")
print("===================================")
input()