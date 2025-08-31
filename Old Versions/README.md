![GitHub release](https://img.shields.io/badge/release-v1.1-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-brightgreen?style=for-the-badge)
![Build](https://img.shields.io/badge/build-passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)

---

## 🚀 Registro de cambios

### 🟢 Versión 1.1 (2025-08-27)
✨ **Nuevas funcionalidades**
- Ahora el programa pregunta al usuario la carpeta de destino antes de iniciar la copia.  
- Se agregó soporte para directorios dinámicos (no requiere modificar el código).  
- Mejoras en los mensajes de estado:  
  - ✅ Copia realizada con éxito.  
  - ❌ Error de ruta.  
  - ⏳ Mensaje de espera entre ciclos.  
- Optimización en la validación de rutas de origen y destino.  

🛠️ **Mejoras**
- Código más robusto y fácil de mantener.  
- Reducción de posibles errores al permitir rutas personalizadas de destino.  

---

### 🟡 Versión 1.0 (2025-08-26)
✨ **Funcionalidades iniciales**
- Copia automática de archivos desde una carpeta de origen definida por el usuario hacia un destino fijo en red (`\\192.168.101.9\DatosPrincipales\Respaldos`).  
- Ciclo automático de copias cada 30 minutos.  
- Validación de existencia de la carpeta origen y destino.  
- Mensajes básicos de estado en consola.  

---

## 🔄 Comparación de versiones

| Característica              | Versión 1.0 🟡 | Versión 1.1 🟢 |
|-----------------------------|----------------|----------------|
| Selección de carpeta origen | ✅             | ✅             |
| Selección de carpeta destino| ❌ (fijo)      | ✅ (dinámico)  |
| Ciclo automático de copias  | ✅ (30 min)    | ✅ (30 min)    |
| Validación de rutas         | ✅ básica      | ✅ mejorada    |
| Mensajes de estado          | Básicos        | Detallados     |
| Facilidad de configuración  | Limitada       | Flexible       |

---
## 👤 Desarrollador

**NRC Originals Enterprise**  
Desarrollado por *José Barragán (Jearse)*  

---
