import psutil

class Procesos:
    def __init__(self):
        self.lista_procesos = []

    def recolectar_metricas(self):
        # Lista temporal para guardar TODOS los procesos antes de filtrar
        procesos_temporales = []
        
        campos_a_leer = ['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads']
        
        for proc in psutil.process_iter(campos_a_leer):
            try:
                info = proc.info
                
                # Calculamos RAM
                ram_mb = 0.0
                if info['memory_info']:
                    ram_mb = info['memory_info'].rss / (1024 * 1024)
                
                # Calculamos CPU
                cpu_uso = info['cpu_percent'] if info['cpu_percent'] is not None else 0.0
                
                procesos_temporales.append({
                    'pid': info['pid'],
                    'process_name': info['name'],
                    'cpu_usage_percent': cpu_uso,
                    'ram_usage_mb': ram_mb,
                    'threads_count': info['num_threads'] or 0
                })
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # --- AQUÍ APLICAMOS EL FILTRO TOP 10 ---
        
        # 1. Ordenamos por CPU (de mayor a menor) y sacamos los 10 primeros
        top_cpu = sorted(procesos_temporales, key=lambda x: x['cpu_usage_percent'], reverse=True)[:10]
        
        # 2. Ordenamos por RAM (de mayor a menor) y sacamos los 10 primeros
        top_ram = sorted(procesos_temporales, key=lambda x: x['ram_usage_mb'], reverse=True)[:10]
        
        # 3. Juntamos ambas listas evitando duplicados (por si el que más CPU usa es también el que más RAM usa)
        pids_vistos = set()
        self.lista_procesos = [] # Limpiamos la lista final
        
        for p in (top_cpu + top_ram):
            if p['pid'] not in pids_vistos:
                pids_vistos.add(p['pid'])
                self.lista_procesos.append(p)