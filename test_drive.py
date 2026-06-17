from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# -----------------------------
# CONFIG
# -----------------------------
SERVICE_ACCOUNT_FILE = "biblioteca-akf-b75b8dd4cc20.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

ROOT_FOLDER_ID = "1Rw_J6y1Bmavo5QeYqlyswG74DLuMkwo_"

# -----------------------------
# AUTH
# -----------------------------
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build("drive", "v3", credentials=credentials)

# -----------------------------
# 1. LEER CARPETAS PRINCIPALES
# -----------------------------
query_root = f"'{ROOT_FOLDER_ID}' in parents and trashed = false"

root_items = service.files().list(
    q=query_root,
    fields="files(id, name, mimeType)"
).execute().get("files", [])

carpetas = [
    c for c in root_items
    if c["mimeType"] == "application/vnd.google-apps.folder"
]

# -----------------------------
# 2. ESTRUCTURA FINAL
# -----------------------------
por_letra = {}
# --------------------

EXTENSIONES_VALIDAS = {
    ".7z",
    ".zip",
    ".rar"
}

archivos_vistos = set()

# -----------------------------
# 3. RECORRER CARPETAS
# -----------------------------
for carpeta in carpetas:

    carpeta_id = carpeta["id"]
    carpeta_nombre = carpeta["name"]

    query = f"'{carpeta_id}' in parents and trashed = false"

    files = service.files().list(
        q=query,
#        fields="files(id, name, mimeType, appProperties)"
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute().get("files", [])

    lista_archivos = []

    for f in files:

        if f["mimeType"] == "application/vnd.google-apps.folder":
            continue

        nombre = f["name"]
        file_id = f["id"]
        
        if nombre in archivos_vistos:
        
            print()
            print("----------------------------------------")
            print("AVISO DUPLICADO")
            print()
            print(nombre)
            print(f"Carpeta: {carpeta_nombre}")
            print("----------------------------------------")
        
        else:
            archivos_vistos.add(nombre)
        
        fecha_mod = f["modifiedTime"]

        # extensión (si existe)
        _, ext = os.path.splitext(nombre)
        
        ext = ext.lower()
        
        if ext not in EXTENSIONES_VALIDAS:
        
            print()
            print("----------------------------------------")
            print("AVISO EXTENSIÓN NO PERMITIDA")
            print()
            print(nombre)
            print(f"Extensión: {ext}")
            print(f"Carpeta: {carpeta_nombre}")
            print("----------------------------------------")

        lista_archivos.append({
            "nombre": nombre,
            "id": file_id,
            "fecha_mod": fecha_mod
        })

    por_letra[carpeta_nombre] = lista_archivos

# -----------------------------
# 4. PRUEBA FINAL
# -----------------------------
#for letra in sorted(por_letra.keys()):
#
#    print(f"\n{letra} ({len(por_letra[letra])})")
#
#    for item in por_letra[letra]:
#        print("   ", item["nombre"])
total = sum(len(lista) for lista in por_letra.values())
print(f"Carpetas procesadas: {len(por_letra)}")
print(f"Archivos encontrados: {total}")

# Crear el archivo biblioteca.json

with open("biblioteca.json", "w", encoding="utf-8") as f:
    json.dump(por_letra, f, ensure_ascii=False, indent=4)