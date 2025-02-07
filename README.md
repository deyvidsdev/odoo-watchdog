# **Watchdog Docker Container Restarter Odoo**

Este script en Python monitoriza los cambios en los archivos `.py` dentro de un directorio específico. Cuando detecta modificaciones, creaciones o eliminaciones de estos archivos, reinicia automáticamente el contenedor Docker asociado, optimizando el proceso y eliminando la necesidad de hacerlo manualmente.

## **¿Qué hace este script?**

El script utiliza la librería `watchdog` para observar un directorio específico y detectar eventos en los archivos `.py` (modificación, creación o eliminación). Cuando uno de estos eventos ocurre, se reinicia automáticamente el contenedor Docker que se especifica.

### **Objetivos principales:**
- **Monitorear cambios** en los archivos `.py` dentro de un directorio.
- **Reiniciar el contenedor Docker** automáticamente cuando se detecta un cambio.
- **Evitar reinicios repetidos** en intervalos de tiempo muy cortos gracias a la función de debounce.

## **Requisitos**

Antes de ejecutar este script, asegúrate de tener los siguientes requisitos:

- Python 3.x
- Docker instalado en tu máquina.
- La librería `watchdog` de Python instalada.

Puedes instalar `watchdog` con el siguiente comando:

```bash
pip install watchdog
```

## **Configuración**

1. **Nombre del contenedor Docker**:
   - Cambia el valor de `CONTAINER_NAME` para que coincida con el nombre del contenedor que deseas reiniciar.

2. **Directorio a monitorear**:
   - Modifica la variable `DIRECTORY_TO_WATCH` con la ruta absoluta del directorio que contiene los archivos `.py` que quieres monitorear.

3. **Archivo de log**:
   - Los eventos y reinicios se registran en el archivo `watchdog_logger.log`. Puedes cambiar el nombre del archivo o la ubicación si lo deseas.

## **Cómo ejecutar el script**

Para ejecutar el script:

1. Clona este repositorio en tu máquina:

   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   ```

2. Navega al directorio donde guardaste el archivo:

   ```bash
   cd <directorio_del_repositorio>
   ```

3. Ejecuta el script:

   ```bash
   python monitor.py
   ```

   Esto comenzará a monitorear los cambios en el directorio especificado y reiniciará el contenedor Docker cuando se detecten cambios en los archivos `.py`.

## **Cómo funciona el script**

1. **Monitoreo de eventos**:
   El script utiliza la clase `watchdog.observers.Observer` para monitorear un directorio y detectar los siguientes eventos en los archivos `.py`:
   - **Creación de archivo** (`on_created`)
   - **Modificación de archivo** (`on_modified`)
   - **Eliminación de archivo** (`on_deleted`)

2. **Debounce**:
   Se implementa un sistema de debounce que evita reinicios rápidos y repetidos. Si el contenedor fue reiniciado recientemente, el script no realizará otro reinicio hasta que haya pasado el tiempo especificado en `DEBOUNCE_TIME`.

3. **Reinicio del contenedor**:
   Cuando el script detecta un evento en los archivos `.py`, ejecuta el comando `docker restart` para reiniciar el contenedor configurado en la variable `CONTAINER_NAME`.

## **Ejemplo de salida**

Cuando el script detecta un cambio en un archivo `.py`, verás en el archivo de log algo como esto:

```
2025-02-07 14:12:34 - INFO - Archivo modificado: C:/ruta/a/archivo.py
2025-02-07 14:12:34 - INFO - Reiniciando contenedor nombre-contenedor
```

### **📩 Contacto**  

Si tienes preguntas o sugerencias, puedes contactarme en:  
📧 **Correo electrónico:** [deyvidsalvino@gmail.com](mailto:deyvidsalvino@gmail.com)

## **Licencia**

Este proyecto está bajo la Licencia MIT.