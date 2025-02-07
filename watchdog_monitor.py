import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONTAINER_NAME = "container-name"  # Nombre del contenedor Docker a reiniciar
DIRECTORY_TO_WATCH = "path/to/directory"  # Directorio a monitorear
DEBOUNCE_TIME = 5  # Aumenta el tiempo de debounce a 5 segundos
LOG_FILE = "watchdog_logger.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
)

def reiniciar_contenedor(nombre_contenedor):
    """Reinicia un contenedor Docker."""
    try:
        comando = ["docker", "restart", nombre_contenedor]
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al reiniciar el contenedor {nombre_contenedor}: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al reiniciar el contenedor: {e}")

class PyFileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.debounce_time = DEBOUNCE_TIME
        self.last_event_times = {} 
        self.last_restart_time = 0 

    def _should_log_event(self, event_type, src_path):
        """Verifica si el evento debe ser logueado según el tiempo de debounce."""
        current_time = time.time()
        event_key = (event_type, src_path)
        last_time = self.last_event_times.get(event_key, 0)

        if (current_time - last_time) > self.debounce_time:
            self.last_event_times[event_key] = current_time
            return True
        return False

    def _handle_event(self, event, event_type):
        """Maneja eventos de modificación, creación y eliminación."""
        if event.src_path.endswith(".py"):
            if self._should_log_event(event_type, event.src_path):
                current_time = time.time()
                if (current_time - self.last_restart_time) > self.debounce_time:
                    logging.info(f"Archivo {event_type}: {event.src_path}")
                    reiniciar_contenedor(CONTAINER_NAME)
                    self.last_restart_time = current_time

    def on_modified(self, event):
        self._handle_event(event, "modificado")

    def on_created(self, event):
        self._handle_event(event, "creado")

    def on_deleted(self, event):
        self._handle_event(event, "eliminado")

def monitor_directory(path):
    """Monitorea un directorio en busca de cambios en archivos .py."""
    event_handler = PyFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoreo detenido por el usuario.")
    except Exception as e:
        logging.error(f"Error inesperado en el monitoreo: {e}")
    finally:
        observer.join()

if __name__ == "__main__":
    print(f"Monitoreando cambios en {DIRECTORY_TO_WATCH}...")
    monitor_directory(DIRECTORY_TO_WATCH)