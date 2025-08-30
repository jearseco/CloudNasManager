# 📌 Changelog - CloudNasManager

## 🟢 Versión 1.1 (2025-08-27)
### ✨ Nuevas Funcionalidades
- Ahora el programa pregunta al usuario la **carpeta de destino** antes de iniciar la copia.  
- Se agregó soporte para **directorios dinámicos** (no requiere modificar el código).  
- Mejoras en los **mensajes de estado**:  
  - ✅ Copia realizada con éxito.  
  - ❌ Error de ruta.  
  - ⏳ Mensaje de espera entre ciclos.  
- Optimización en la validación de rutas de **origen** y **destino**.  

### 🛠️ Mejoras
- Código más **robusto y fácil de mantener**.  
- Reducción de posibles errores al permitir rutas personalizadas de destino.  

---

## 🟡 Versión 1.0 (2025-08-26)
### ✨ Funcionalidades iniciales
- Copia automática de archivos desde una carpeta de **origen definida por el usuario** hacia un destino **fijo en red** (`\\192.168.101.9\DatosPrincipales\Respaldos`).  
- Ciclo automático de copias cada **30 minutos**.  
- Validación de existencia de la carpeta **origen** y **destino**.  
- Mensajes básicos de estado en consola.  

---

## 🔄 Comparación de versiones
| Característica | v1.0 | v1.1 |
|----------------|------|------|
| Selección de carpeta de origen | ✅ | ✅ |
| Selección de carpeta de destino | ❌ (fijo en red) | ✅ (dinámico, preguntado al usuario) |
| Ciclo automático de copias | ✅ (cada 30 min) | ✅ (cada 30 min) |
| Validación de rutas | ✅ básica | ✅ mejorada |
| Mensajes de estado | Básicos | Más detallados |
| Facilidad de configuración | Limitada | Flexible |

---
