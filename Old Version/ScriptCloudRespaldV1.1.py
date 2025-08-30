import shutil
import time
import os

# Pregunta al usuario la ruta de origen
origen = input("📂 Ingresa la ruta de ORIGEN (ejemplo: C:\\Users\\TuUsuario\\Documentos): ")

# Pregunta al usuario la ruta de destino
destino = input("💾 Ingresa la ruta de DESTINO (ejemplo: \\\\192.168.101.9\\DatosPrincipales\\Respaldos): ")

# Verificar que el origen existe
if not os.path.exists(origen):
    print("❌ La ruta de ORIGEN no existe.")
    exit()

# Verificar que el destino existe
if not os.path.exists(destino):
    print("❌ La ruta de DESTINO no existe.")
    exit()

while True:
    try:
        # Copiar archivos y carpetas
        shutil.copytree(origen, destino, dirs_exist_ok=True)
        print("✅ Copia realizada con éxito.")
    except Exception as e:
        print(f"⚠️ Error al copiar: {e}")

    # Esperar 30 minutos (1800 segundos)
    print("⏳ Esperando 30 minutos para la próxima copia...")
    time.sleep(1800)
