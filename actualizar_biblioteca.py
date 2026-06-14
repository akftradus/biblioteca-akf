import subprocess
import sys

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

print()
print("===================================")
print("Biblioteca actualizada correctamente")
print("===================================")