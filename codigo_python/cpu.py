import psutil

class CPU:
    def __init__(self, porcentajeUsoCpu, frecuenciaCpu, tiempoUsuario, tiempoKernel, tiempoDisco, tiempoRobado, tiempoDesactivado, interrupciones, cambiosContexto, carga1min, carga5min, carga15min):
        self.cpu_load_percent = porcentajeUsoCpu # porcentaje de uso de la cpu
        self.cpu_freq_mhz = frecuenciaCpu # frecuencia de la cpu
        self.cpu_user_percent = tiempoUsuario # porcentaje de tiempo que la cpu está con programas de usuario
        self.cpu_kernel_percent = tiempoKernel # porcentaje de tiempo que está la cpu con el kernel
        self.cpu_iowait_percent = tiempoDisco # porcentaje de tiempo inactivo esperando disco duro
        self.cpu_steal_percent = tiempoRobado # porcentaje de tiempo perdido esperando a que el servidor fisico nos asigne recursos
        self.cpu_inactive_percent = tiempoDesactivado # porcentaje de tiempo que la cpu estuvo libre, sin hacer nada
        self.cpu_interrupts = interrupciones # Cantidad de interrupciones, ya sean de teclado, de ratón etc
        self.ctx_switches = cambiosContexto # cantidad de cambios de contexto 
        self.load_avg_1m = carga1min
        self.load_avg_5m = carga5min
        self.load_avg_15m = carga15min

def recolectar_metricas(): # recoleccion de metricas de cpu
    cpu_load = psutil.cpu_percent(interval=1) # Porcentaje de uso de la cpu
    freq_info = psutil.cpu_freq() # frecuencia de la cpu
    cpu_freq = int(freq_info.current) if freq_info else 0 # si hay algún problema que devuelva cero
    
    cpu_times = psutil.cpu_times_percent(interval=None) # Devuelve porcentajes de tiempo
    time_user = cpu_times.user         # Porcentaje de tiempo dedicado a procesos de usuario (tus aplicaciones).
    time_kernel = cpu_times.system     # Porcentaje de tiempo dedicado a procesos internos del sistema operativo (kernel).
    time_waiting_disk = cpu_times.iowait # Porcentaje de tiempo inactivo esperando a que el disco duro/SSD responda.
    time_steal = cpu_times.steal       # Porcentaje de tiempo perdido esperando porque el servidor físico atendía a otra máquina virtual.
    time_inactivo = cpu_times.idle     # Porcentaje de tiempo en el que la CPU estuvo totalmente libre, sin hacer nada.
    
    cpu_stats = psutil.cpu_stats() # Devuleve contadores absolutos
    interrupts = cpu_stats.interrupts # interrupciones como pueden ser de teclado, de ratón etc. Valores discontinuos podrían ser ataques de red
    ctx_switches = cpu_stats.ctx_switches # la cantidad de veces que la cpu ha guardado el estado de un programa, lo ha pausado y ha cargado el estado de otro programa ejectuado. Valores altos significa que la cpu está perdiendo demasiado tiempo   
    
    load_1m, load_5m, load_15m = psutil.getloadavg()
    # cuenta cuantos procesos están exigiendo atención a la CPU o están atascados esperando al disco duro
    # load_1m es lo que ha ocurrido en el último minuto
    # load_5m si genera numeros altos significa que el esfuerzo del servidor no fue de un solo segundo
    # load_15m si en los tres valores los rangos son altos ALERTA, signifca que hay algun proceso bloqueando la cpu
    return CPU(porcentajeUsoCpu=cpu_load, frecuenciaCpu=cpu_freq, tiempoUsuario=time_user, tiempoKernel=time_kernel, tiempoDisco=time_waiting_disk, tiempoRobado=time_steal, tiempoDesactivado=time_inactivo, interrupciones=interrupts, cambiosContexto=ctx_switches, carga1min=load_1m, carga5min=load_5m, carga15min=load_15m)