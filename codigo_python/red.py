import psutil

class Red:
    def __init__(self):
        self.interfaces = {}
        self.active_connections_total = 0 # 5. Las conexiones activas del controlador
    def recolectar_metricas(self):
        self.interfaces = {}
        net_io = psutil.net_io_counters(pernic=True) # Obtenemos los contadores de red separados por tarjeta de red (pernic=True)
        for interface_name, counters in net_io.items():
            dropped = counters.dropin + counters.dropout # Sumamos los paquetes descartados de entrada (dropin) y salida (dropout)
            errors = counters.errin + counters.errout # Sumamos los errores de entrada y salida
            self.interfaces[interface_name] = {
                'bytes_sent': counters.bytes_sent, # 1. Bytes enviados por el controlador de red
                'bytes_recv': counters.bytes_recv, # 2. Bytes recibidos por el controlador
                'packets_dropped': dropped, # 3. Paquetes droppeados por el controlador
                'packets_errors': errors # 4. Error de paquetes
            }
        try:
            conexiones = psutil.net_connections(kind='inet') # kind='inet' filtra solo conexiones IPv4 e IPv6 (ignora sockets internos de UNIX)
            self.active_connections_total = sum(1 for c in conexiones if c.status == 'ESTABLISHED') # Contamos solo las conexiones que están realmente establecidas y transmitiendo
        except psutil.AccessDenied: # Si el script no corre como root, algunos procesos ocultan sus sockets
            self.active_connections_total = 0