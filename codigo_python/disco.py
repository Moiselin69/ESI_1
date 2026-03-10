import psutil
import os
class Disco:
    """
    Clase para recolectar métricas de almacenamiento y rendimiento del disco.
    Por defecto, evaluaremos la partición principal ('/').
    """
    def __init__(self):
        self.space_total_mb = 0 # 1. espacio total del disco
        self.space_used_mb = 0 # 2. espacio del disco utilizado
        self.space_used_percent = 0 # 3. porcentaje de disco utilizado
        self.inodes_total = 0 # 4. total de inodos 
        self.inodes_used = 0 # 5. total de inodos utilizados
        self.inodes_used_percent = 0 # 6. porcentaje de inodos utilizados
        self.iops_read = 0 # 7. Total de operaciones de lectura (acumulado)
        self.iops_write = 0 # 8. Total de operaciones de escritura (acumulado)
        self.latency_read_ms = 0.0 # 9. Tiempo total de lectura en ms (acumulado)
        self.latency_write_ms = 0.0 # 10. Tiempo total de escritura en ms (acumulado)

    def recolectarMetricas(self):
        uso_disco = psutil.disk_usage('/')  # Espacio en disco
        self.space_total_mb = uso_disco.total / (1024 * 1024)
        self.space_used_mb = uso_disco.used / (1024 * 1024)
        self.space_used_percent = uso_disco.percent
        
        st = os.statvfs('/') # Inodos
        self.inodes_total = st.f_files
        self.inodes_used = st.f_files - st.f_ffree

        io_counters = psutil.disk_io_counters() # IOPS y Latencias
        if io_counters:
            self.iops_read = io_counters.read_count
            self.iops_write = io_counters.write_count
            self.latency_read_ms = float(io_counters.read_time)
            self.latency_write_ms = float(io_counters.write_time)