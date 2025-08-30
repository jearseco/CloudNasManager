import os
import shutil
import time

# Carpeta origen
origen = r"C:\Users\stewa\Videos\Versiones"

# Carpeta destino en la red
destino = r"\\192.168.101.10\DatosPrincipales\Respaldos"

# Intervalo en segundos (ejemplo: 600 = cada 10 min)
intervalo = 10 

usuario = "user"
clave = "1234"

def montar_red():
    try:
        # Primero desconectamos por si ya está montado
        os.system(f'net use {destino} /delete /y')
        # Conectamos con credenciales
        resultado = os.system(f'net use {destino} /user:{usuario} {clave}')
        if resultado == 0:
            print("✅ Conectado correctamente al recurso de red")
        else:
            print("⚠️ Error al conectar al recurso de red")
    except Exception as e:
        print(f"Error al montar red: {e}")

def copiar_directorio(origen, destino):
    try:
        for root, dirs, files in os.walk(origen):
            # Construye la ruta relativa desde origen
            rel_path = os.path.relpath(root, origen)
            destino_carpeta = os.path.join(destino, rel_path)

            # Crea la carpeta en el destino si no existe
            if not os.path.exists(destino_carpeta):
                os.makedirs(destino_carpeta)

            # Copia archivos
            for archivo in files:
                ruta_origen = os.path.join(root, archivo)
                ruta_destino = os.path.join(destino_carpeta, archivo)

                # Copiar solo si no existe o si fue modificado
                if (not os.path.exists(ruta_destino) or 
                    os.path.getmtime(ruta_origen) > os.path.getmtime(ruta_destino)):
                    shutil.copy2(ruta_origen, ruta_destino)
                    print(f"📂 Copiado/Actualizado: {ruta_destino}")
    except Exception as e:
        print(f"Error en copia: {e}")

# Bucle infinito
while True:
    print("🔄 Iniciando respaldo...")
    montar_red()
    copiar_directorio(origen, destino)
    print(f"⏳ Esperando {intervalo} segundos...\n")
    time.sleep(intervalo)
