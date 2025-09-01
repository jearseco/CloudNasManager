# ☁️ CloudNasManager V1.2.2

![Version](https://img.shields.io/badge/version-1.2.2-blue.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)
![UI](https://img.shields.io/badge/UI-Tkinter-orange.svg)

---

## 📌 Descripción
**CloudNasManager** es una herramienta con interfaz gráfica que facilita la conexión y gestión de servidores **NAS (Network Attached Storage)**.  
Permite agregar múltiples servidores/IP y muestra el estado de conexión en tiempo real, diferenciando entre servidores **activos (verde)** y **no disponibles (gris)**.

---

## ✨ Novedades de la versión 1.2.2
- ✅ Botón **"Agregar más servidores/IP"** desde la interfaz gráfica.  
- ✅ Estado visual del servidor:  
  - 🟢 **Activo**: carpeta encontrada correctamente.  
  - ⚪ **N/A**: servidor no disponible o carpeta inaccesible.  
- ✅ Correcciones menores de rendimiento y estabilidad.  
- ✅ Empaquetado en **.exe** para fácil distribución.  

---

## 🖥️ Requisitos del sistema
- **Sistema operativo**: Windows 10/11 (x64).  
- **Python**: 3.9 o superior (si se ejecuta como script).  
- **Dependencias**:
  - `tkinter`
  - `os`
  - `subprocess`
  - `PIL (Pillow)`  

⚠️ Si ejecutas la versión empaquetada (`.exe`), no necesitas instalar Python ni librerías adicionales.

---

## 🛠️ Solución de problemas

| Problema | Posible Causa | Solución |
|----------|---------------|----------|
| ❌ No se conecta al servidor | La IP ingresada es incorrecta o el servidor está apagado | Verifica la IP y el estado del servidor |
| ⚪ Estado muestra "N/A" | Carpeta compartida no encontrada | Asegúrate de que el recurso compartido está configurado correctamente |
| El programa no abre en Windows | Falta de permisos o antivirus bloqueando | Ejecutar como **Administrador** o añadir a excepciones del antivirus |
| Error con `PIL` o `tkinter` | Librerías no instaladas (modo script) | Instalar dependencias con `pip install pillow` |

---

## 📂 Información del proyecto
- **Nombre:** CloudNasManager  
- **Versión:** 1.2.2  
- **Licencia:** Propietaria (NRC Originals Enterprise)  
- **Estado:** Estable  
- **Lenguaje principal:** Python 3.9+  
- **Interfaz gráfica:** Tkinter  

---

## 🤝 Contribuciones y soporte
Este proyecto es **propietario**, pero se aceptan sugerencias de mejoras y reportes de errores a través de:  

- 📧 **Soporte:** support@nrcoriginals.com  
- 📝 **Issues de GitHub:** [Repositorio oficial](https://github.com/jearseco/CloudNasManager)  
- 🔧 **Pull Requests:** No disponibles (proyecto cerrado).  

---

## 👨‍💻 Desarrollado por
**NRC Originals Enterprise**  
By: *Jearse* 🎶💻  

---
