import subprocess
import sys
from datetime import datetime
import time

# =========================
# COLORES
# =========================
BOLD = '\033[1m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
LIGHTBLUE = '\033[38;5;39m'
LIGHTORANGE = '\033[38;5;215m'
PINK = '\033[38;5;213m'
RESET = '\033[0m'

print("Actualizando biblioteca.json...")
resultado = subprocess.run(
    [sys.executable, "test_drive.py"]
)

if resultado.returncode != 0:
    print(f"    {YELLOW}ERROR al generar biblioteca.json{RESET}")
    sys.exit(1)

print("Generando index.html...")
resultado = subprocess.run(
    [sys.executable, "biblioteca_akf.py"]
)

if resultado.returncode != 0:
    print(f"    {YELLOW}ERROR al generar index.html{RESET}")
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
    print(f"    {YELLOW} al publicar en GitHub.{RESET}")
    sys.exit(1)

print()
print("===================================")
print("Biblioteca actualizada correctamente")
print("===================================")
print()
print(f"      {GREEN}Proceso completado correctamente.{RESET}")
time.sleep(2)