# CloudNasManager v2.

![Logo Imagen](https://github.com/jearseco/CloudNasManager/blob/63290920a5e83640457396933a5c29289b3cbfd9/Imagesl/extension_icon%40512px%20(1).png)

# Cloud NAS Manager v2.0 - Lista de Características

## Versión: 2.0

## Autor: Jose Barragan & Josip Polo

Fecha: 30 de Agosto de 2025

## Demo

Insert gif or link to demo


## Features

Cloud NAS Manager es una aplicación de escritorio diseñada para simplificar la administración y automatización de copias de seguridad en múltiples servidores NAS locales (como TrueNAS) dentro de una red.
## 1. Detección y Gestión de Servidores
Búsqueda Automática en la Red:

 - La aplicación escanea la red local para detectar automáticamente todos los servidores NAS que responden a las credenciales configuradas.

 - Utiliza un escaneo de puertos rápido y eficiente para minimizar los tiempos de espera.

 - Sistema de Caché Inteligente:

 - Guarda la lista de servidores encontrados en un archivo local. Esto permite que la aplicación se inicie de forma casi instantánea en usos posteriores.

 - Incluye un botón para "Volver a Escanear la Red" que fuerza una nueva búsqueda, ideal para cuando se añaden nuevos servidores.

## 1.2 Configuración Remota de Servidores:

 - Si se detecta un servidor accesible pero que no ha sido configurado, la aplicación lo marca como "No Configurado".

 - Permite al usuario asignar un nombre al servidor directamente desde la interfaz. La aplicación se conecta remotamente y crea los archivos de configuración (config.txt, backup.txt) necesarios, dejando el servidor listo para ser administrado.

## 1.3 Visualización Clara de Estados:

 - La lista principal muestra cada servidor con un estado visual claro:

 - Configurado (Verde): Servidor en línea y listo para administrar.

 - No Configurado (Naranja): Servidor en línea pero requiere configuración inicial.

 - Error de Conexión (Rojo): Servidor encontrado en el caché pero actualmente inaccesible.

## 2. Panel de Administración de NAS
Una vez que se selecciona un servidor configurado, se abre un potente panel de administración dedicado con las siguientes funciones:
Interfaz Multi-Panel Moderna:

 - Una ventana de gestión centralizada con un menú de navegación lateral que permite cambiar entre diferentes vistas ("Inicio", "Lista de Directorios") de forma fluida y sin abrir nuevas ventanas.

## 3.1Panel de "Inicio" (Dashboard Principal):

 - Muestra la información clave del servidor: Nombre, Dirección IP y Estado.

 - Ofrece un resumen de solo lectura de todas las tareas de respaldo activas e inactivas.

 - Incluye un botón para "REALIZAR COPIA AHORA", que ejecuta un respaldo manual inmediato de todas las carpetas activas.

## 3.2 Panel "Lista de Directorios" (Gestor de Tareas de Backup):

 - Es el centro de control para las copias de seguridad. Permite:

 - Agregar y Eliminar Tareas: Seleccionar carpetas locales para añadir a la cola de respaldo o eliminarlas.

 - Activar y Desactivar Tareas: Pausar una tarea de respaldo sin necesidad de borrarla.

## Configuración Centralizada: 

La lista de directorios se guarda en el archivo backup.txt directamente en el servidor NAS, asegurando que la configuración sea consistente desde cualquier PC que ejecute la aplicación.

## 3. Sistema de Copias de Seguridad (Backups)
Backups Manuales y Automáticos:

El sistema soporta tanto copias de seguridad manuales (iniciadas con un clic) como automáticas (programadas).

## 3.1 Programación de Backups Automáticos:

 - Permite configurar un intervalo de tiempo para que las copias de seguridad se realicen de forma automática en segundo plano.

 - Las opciones de intervalo son configurables (ej: 1 Minuto para pruebas, 10, 20, 30 min, 1 Hora).

## 3.2 Proceso en Segundo Plano (Multihilo):

 - Las copias de seguridad automáticas se ejecutan en un hilo de procesamiento separado. Esto garantiza que la interfaz de la aplicación nunca se congele y permanezca siempre fluida y receptiva, incluso durante copias de archivos grandes.

 - Se puede Iniciar y Detener el servicio de backup automático en cualquier momento.

## 3.3 Estructura de Carpetas Organizada:

Cada copia de seguridad se guarda en el servidor NAS dentro de una estructura de carpetas ordenada, que incluye el nombre de la carpeta original y la fecha y hora exactas del respaldo, facilitando la restauración de versiones anteriores.

```bash
\\IP_DEL_SERVIDOR\DatosPrincipales\Respaldos\[NombreCarpetaOriginal]\[Año-Mes-Día_Hora-Min-Seg]
```

## 4. Tecnología y Fiabilidad
Conectividad Robusta con Windows:

 - Utiliza el sistema nativo de mapeo de unidades de red de Windows (net use) para todas las operaciones de archivos. Esto elimina la dependencia de librerías externas complejas y garantiza una compatibilidad y fiabilidad máximas.

Arquitectura Centralizada:

 - Toda la configuración crítica ```(nombres de servidor, listas de directorios)``` se almacena en los propios servidores NAS, no en la computadora del usuario.



## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```

## Related

Here are some related projects

[Awesome README](https://github.com/matiassingers/awesome-readme)


## Authors

- [@octokatherine](https://www.github.com/jearseco)
