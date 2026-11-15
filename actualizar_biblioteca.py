
import subprocess
import sys
from datetime import datetime
import time

# =========================
# HABILITAR COLORES ANSI
# =========================
if sys.platform == "win32":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    modo = ctypes.c_ulong()

    if kernel32.GetConsoleMode(handle, ctypes.byref(modo)):
        kernel32.SetConsoleMode(
            handle,
            modo.value | 0x0004
        )

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


def ejecutar_git(comando, descripcion):
    """Ejecuta un comando Git y comprueba su resultado."""

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        print(f"\n    {YELLOW}ERROR: {descripcion}{RESET}")

        if resultado.stdout.strip():
            print(resultado.stdout)

        if resultado.stderr.strip():
            print(resultado.stderr)

        input("\nAnota el error y pulsa ENTER para cerrar...")
        sys.exit(1)

    return resultado


# =========================
# GENERAR BIBLIOTECA
# =========================

print("Actualizando biblioteca.json...")

resultado = subprocess.run(
    [sys.executable, "test_drive.py"]
)

if resultado.returncode != 0:
    print(f"    {YELLOW}ERROR al generar biblioteca.json{RESET}")
    input("\nAnota el error y pulsa ENTER para cerrar...")
    sys.exit(1)


print("Generando index.html...")

resultado = subprocess.run(
    [sys.executable, "biblioteca_akf.py"]
)

if resultado.returncode != 0:
    print(f"    {YELLOW}ERROR al generar index.html{RESET}")
    input("\nAnota el error y pulsa ENTER para cerrar...")
    sys.exit(1)


# =========================
# PUBLICAR EN GITHUB
# =========================

print("Publicando en GitHub...")

# Identificar la rama actual.
rama = ejecutar_git(
    ["git", "branch", "--show-current"],
    "No se pudo identificar la rama actual."
)

rama = rama.stdout.strip()

if not rama:
    print(f"    {YELLOW}ERROR: No se pudo identificar la rama.{RESET}")
    input("\nAnota el error y pulsa ENTER para cerrar...")
    sys.exit(1)


# Consultar la última versión de GitHub.
ejecutar_git(
    ["git", "fetch", "origin"],
    "No se pudo consultar GitHub."
)


# Comprobar que existe la rama remota correspondiente.
ejecutar_git(
    ["git", "rev-parse", "--verify", f"origin/{rama}"],
    "No se encontró la rama correspondiente en GitHub."
)


# Actualizar la referencia local sin borrar los archivos generados.
ejecutar_git(
    ["git", "reset", "--mixed", f"origin/{rama}"],
    "No se pudo actualizar la referencia local."
)


# Preparar los cambios de archivos rastreados.
ejecutar_git(
    ["git", "add", "-u"],
    "No se pudieron preparar los archivos."
)


# Comprobar si hay cambios para publicar.
status = ejecutar_git(
    ["git", "status", "--porcelain"],
    "No se pudo comprobar el estado de los archivos."
)

if not status.stdout.strip():
    print(f"    {GREEN}No hay cambios para publicar.{RESET}")
    print(f"\n    {GREEN}Biblioteca ya actualizada.{RESET}")
    time.sleep(3)
    sys.exit(0)


# =========================
# CREAR COMMIT
# =========================

fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
mensaje = f"Actualización automática {fecha}"

ejecutar_git(
    ["git", "commit", "-m", mensaje],
    "No se pudo crear el commit."
)


# =========================
# PUBLICAR
# =========================

ejecutar_git(
    ["git", "push", "origin", rama],
    "No se pudo publicar la biblioteca en GitHub."
)


# =========================
# FINALIZACIÓN
# =========================

print(f"    {GREEN}Cambios publicados en GitHub.{RESET}")

print()
print(f"      {GREEN}==================================={RESET}")
print("        Biblioteca actualizada correctamente")
print(f"      {GREEN}==================================={RESET}")
print()
print(f"      {GREEN}Proceso completado correctamente.{RESET}")

time.sleep(3)
