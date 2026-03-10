import psutil
import time

class Sistema:
    def __init__(self):
        self.total_processes = 0 # 1. total de procesos en activo
        self.total_threads = 0 # 2. total de hilos en activo
        self.active_users = 0 # 3. usuarios que están activos
        self.uptime_seconds = 0 # 4. tiempo que lleva encendido el sistema

    def recolectarMetricas(self): 
        self.uptime_seconds = int(time.time() - psutil.boot_time()) # Restamos la hora actual menos la hora a la que arrancó el sistema
        self.active_users = len(psutil.users())
        procesos = 0
        hilos = 0
        for proc in psutil.process_iter(['num_threads']): # Iteramos sobre todos los procesos activos pidiendo solo su número de hilos
            try:
                procesos += 1
                hilos += proc.info['num_threads'] or 0
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Si el proceso se cerró justo al leerlo o no tenemos permisos, lo ignoramos
                pass
        self.total_processes = procesos
        self.total_threads = hilos