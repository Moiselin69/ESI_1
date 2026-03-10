import psutil

class CPU:
    def __init__(self):
        self.cpu_load_percent = 0 # 1. porcentaje de uso de la cpu
        self.cpu_freq_mhz = 0 # 2. frecuencia de la cpu
        self.cpu_user_percent = 0 # 3. porcentaje de tiempo que la cpu está con programas de usuario
        self.cpu_kernel_percent = 0 # 4. porcentaje de tiempo que está la cpu con el kernel
        self.cpu_iowait_percent  = 0 # 5. porcentaje de tiempo inactivo esperando disco duro
        self.cpu_steal_percent = 0 # 6. porcentaje de tiempo perdido esperando a que el servidor fisico nos asigne recursos
        self.cpu_inactive_percent = 0 # 7. porcentaje de tiempo que la cpu estuvo libre, sin hacer nada
        self.cpu_interrupts  = 0 # 8. Cantidad de interrupciones, ya sean de teclado, de ratón etc
        self.ctx_switches = 0 # 9. cantidad de cambios de contexto 
        self.load_avg_1m = 0 # 10. los tres signfican los procesos que están exigigiendo atención a la CPU 
        self.load_avg_5m = 0 # 11
        self.load_avg_15m = 0 # 12

    def recolectar_metricas(self): # recoleccion de metricas de cpu
        self.cpu_load_percent = psutil.cpu_percent(interval=1) # Porcentaje de uso de la cpu
        freq_info = psutil.cpu_freq() # frecuencia de la cpu
        self.cpu_freq_mhz = int(freq_info.current) if freq_info else 0 # si hay algún problema que devuelva cero
        
        cpu_times = psutil.cpu_times_percent(interval=None) # Devuelve porcentajes de tiempo
        self.cpu_user_percent = cpu_times.user         # Porcentaje de tiempo dedicado a procesos de usuario (tus aplicaciones).
        self.cpu_kernel_percent = cpu_times.system     # Porcentaje de tiempo dedicado a procesos internos del sistema operativo (kernel).
        self.cpu_iowait_percent = cpu_times.iowait # Porcentaje de tiempo inactivo esperando a que el disco duro/SSD responda.
        self.cpu_steal_percent = cpu_times.steal       # Porcentaje de tiempo perdido esperando porque el servidor físico atendía a otra máquina virtual.
        self.cpu_inactive_percent = cpu_times.idle     # Porcentaje de tiempo en el que la CPU estuvo totalmente libre, sin hacer nada.
        
        cpu_stats = psutil.cpu_stats() # Devuleve contadores absolutos
        self.cpu_interrupts = cpu_stats.interrupts # interrupciones como pueden ser de teclado, de ratón etc. Valores discontinuos podrían ser ataques de red
        self.ctx_switches = cpu_stats.ctx_switches # la cantidad de veces que la cpu ha guardado el estado de un programa, lo ha pausado y ha cargado el estado de otro programa ejectuado. Valores altos significa que la cpu está perdiendo demasiado tiempo   
        
        self.load_avg_1m, self.load_avg_5m, self.load_avg_15m = psutil.getloadavg()
        # cuenta cuantos procesos están exigiendo atención a la CPU o están atascados esperando al disco duro
        # load_1m es lo que ha ocurrido en el último minuto
        # load_5m si genera numeros altos significa que el esfuerzo del servidor no fue de un solo segundo
        # load_15m si en los tres valores los rangos son altos ALERTA, signifca que hay algun proceso bloqueando la cpu