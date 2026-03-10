import psutil

def obtenerFallosPagina():
    try:
        with open('/proc/vmstat', 'r') as f:
            for line in f:
                if line.startswith('pgmajfault'):
                    return int(line.split()[1])
    except FileNotFoundError:
        pass
    return 0

class Memoria:
    def __init__(self):
        self.ram_total_mb = 0 # 1. ram total de la maquina
        self.ram_used_mb = 0 # 2. ram usado de la maquina
        self.ram_used_percent = 0 # 3. porcentaje de ram usado
        self.swap_total_mb = 0 # 4. espacio de swap total
        self.swap_used_mb = 0 # 5. espacio de swap usado
        self.swap_used_percent = 0 # 6. porcentaje de swap utilizado
        self.cache_used_mb = 0 # 7. cache usado de la maquina
        self.cache_used_ram_mb = 0 # 8. porcentaje de ram utilizada para cache
        self.page_faults_major = 0 # 9. fallos de página
    """
    Major Page Fault: Ocurre cuando el sistema busca un dato en la RAM y no está, 
    teniendo que ir a buscarlo al disco duro (operación lenta).

    El tamaño de la cache en linux no existe. El límite teorico es el tamaño de la ram de la máquina
    Esto sucede porque linux utiliza dinámicamente cualquier cantidad de RAM libre que esté libre 
    para guardar datos en caché. 
    
    Al calcular el porcentaje de cache utilizado, lo que vamos a calcular es el porcentaje
    de ram utilizada para cache
    """
    def recolectarMetricas(self): # esta funcion es la que se llamaría para recolectar métricas
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        self.ram_total_mb = mem.total / (1024*1024)
        self.ram_used_mb = mem.used / (1024*1024)
        self.ram_used_percent = mem.percent
        self.swap_total_mb = swap.total / (1024*1024)
        self.swap_used_mb = swap.used / (1024*1024)
        self.swap_used_percent = swap.percent
        self.cache_used_mb = mem.cached / (1024*1024)
        self.cache_used_ram_mb = (mem.cached / mem.total)*100
        self.page_faults_major = obtenerFallosPagina()

