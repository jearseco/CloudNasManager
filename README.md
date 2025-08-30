# ☁️ CloudNasManager

![GitHub release (latest)](https://img.shields.io/github/v/release/jearseco/CloudNasManager?style=for-the-badge)  
![GitHub repo size](https://img.shields.io/github/repo-size/jearseco/CloudNasManager?style=for-the-badge)  
![GitHub stars](https://img.shields.io/github/stars/jearseco/CloudNasManager?style=for-the-badge)  
![GitHub issues](https://img.shields.io/github/issues/jearseco/CloudNasManager?style=for-the-badge)  
![GitHub license](https://img.shields.io/github/license/jearseco/CloudNasManager?style=for-the-badge)

---

## 📌 Descripción

**CloudNasManager** es una herramienta portable para **automatizar copias de seguridad** desde un directorio local hacia un destino en red (NAS/Servidor).  
Optimiza el respaldo copiando solo los archivos modificados y manteniendo la estructura original de carpetas.  

✅ **Características principales:**
- Copias automáticas cada cierto tiempo.  
- Soporte para destinos en red con autenticación (SMB).  
- Validación de rutas y permisos antes de ejecutar la copia.  
- Interfaz de mensajes claros para usuarios.  
- Configuración del destino disponible desde la v1.1.  

---

## ⚙️ Requisitos

- **Sistema:** Windows 10/11 (x64).  
- **Permisos:** lectura en la carpeta origen y escritura en el destino.  
- **Red (NAS):**
  - Acceso SMB habilitado.  
  - Credenciales válidas si no permite acceso como invitado.  
  - Posible mapeo previo con `net use` si tu entorno lo requiere.  
- **Espacio:** suficiente en el destino para respaldos.  

---

## 🧩 Notas técnicas

- Copia la **estructura completa de directorios**.  
- Solo reemplaza archivos cambiados (ahorra tiempo/E/S).  
- Intervalo de copia fijo: **30 min** (configurable en futuras versiones).  

---

## 🚀 Instalación

1. Descarga la última versión desde [Releases](../../releases).  
2. Extrae el contenido del `.zip`.  
3. Ejecuta **CloudNasManager.exe** (portable, no requiere instalación).  

---

## 🏳️ Flags (argumentos CLI)

Puedes lanzar el programa con las siguientes opciones:  

```bash
CloudNasManager.exe --help        # Muestra ayuda de comandos
CloudNasManager.exe --src <ruta>  # Define carpeta origen
CloudNasManager.exe --dst <ruta>  # Define carpeta destino
CloudNasManager.exe --interval 15 # Define intervalo (minutos)
CloudNasManager.exe --log         # Habilita registro detallado en log.txt

```
---
## 🧾 Changelog

Consulta el historial completo en [CHANGELOG.md](./Old-Version/README.md):

- **v1.0:** lanzamiento inicial (destino fijo, intervalos cada 30 min).  
- **v1.1:** destino configurable, mensajes mejorados y validaciones.

---

## 📄 Información

- **Nombre:** CloudNasManager  
- **Versión:** 1.1  
- **Formato:** `.exe` (portable)  
- **Tecnología de build:** PyInstaller  
- **Licencia:** Custom/Propietaria (ajústala si usas otra)  

---

## 👤 Desarrollador

**NRC Originals Enterprise**  
Desarrollado por *José Barragán (Jearse)*  

---

## ⭐ Contribución y soporte

Si tienes sugerencias, reportes de errores o mejoras:  
1. Abre un **Issue** en este repositorio.  
2. Propón un **Pull Request** con tus cambios.  

#💡 ¡Tu feedback ayuda a mejorar CloudNasManager!
