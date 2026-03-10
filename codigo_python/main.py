import time
import socket
from datetime import datetime
from cpu import CPU
from disco import Disco
from memoria import Memoria
from procesos import Procesos
from red import Red
from sistema import Sistema
import mysql.connector

def inicializarVariables():
    hostname = socket.gethostname()
    cpu = CPU()
    disco = Disco()
    memoria = Memoria()
    procesos = Procesos()
    red = Red()
    sistema = Sistema()
    return hostname, cpu, disco, memoria, procesos, red, sistema

def conectar_base_datos():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="usuario",
            password="PIM0203",
            database="esi_1"
        )
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

def recolectarMetricas(cpu:CPU, disco:Disco, memoria:Memoria, procesos:Procesos, red:Red, sistema:Sistema):
    cpu.recolectar_metricas()
    disco.recolectarMetricas()
    memoria.recolectarMetricas()
    procesos.recolectar_metricas()
    red.recolectar_metricas()
    sistema.recolectarMetricas()
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def guardarMetricas(db, cursor, timestamp, hostname, cpu:CPU, disco:Disco, memoria:Memoria, procesos:Procesos, red:Red, sistema:Sistema):
    """
    Inserta todos los datos de las clases en sus respectivas tablas MySQL.
    """
    try:
        # --- TABLA CPU ---
        sql_cpu = """INSERT INTO Cpu (fecha_creacion, hostname, cpu_load_percent, cpu_freq_mhz, cpu_user_percent, 
                     cpu_kernel_percent, cpu_iowait_percent, cpu_steal_percent, cpu_inactive_percent, cpu_interrupts, 
                     cpu_context_switches, load_avg_1m, load_avg_5m, load_avg_15m) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val_cpu = (timestamp, hostname, cpu.cpu_load_percent, cpu.cpu_freq_mhz, cpu.cpu_user_percent, 
                   cpu.cpu_kernel_percent, cpu.cpu_iowait_percent, cpu.cpu_steal_percent, cpu.cpu_inactive_percent, 
                   cpu.cpu_interrupts, cpu.ctx_switches, cpu.load_avg_1m, cpu.load_avg_5m, cpu.load_avg_15m)
        cursor.execute(sql_cpu, val_cpu)

        # --- TABLA MEMORIA ---
        sql_memoria = """INSERT INTO Memoria (fecha_creacion, hostname, ram_total_mb, ram_used_mb, ram_used_percent, 
                         swap_total_mb, swap_used_mb, swap_used_percent, cache_used_mb, cache_used_ram_mb, page_faults_major) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val_memoria = (timestamp, hostname, memoria.ram_total_mb, memoria.ram_used_mb, memoria.ram_used_percent, 
                       memoria.swap_total_mb, memoria.swap_used_mb, memoria.swap_used_percent, memoria.cache_used_mb, 
                       memoria.cache_used_ram_mb, memoria.page_faults_major)
        cursor.execute(sql_memoria, val_memoria)

        # --- TABLA SISTEMA ---
        sql_sistema = """INSERT INTO Sistema (fecha_creacion, hostname, total_processes, total_threads, active_users, uptime_seconds) 
                         VALUES (%s, %s, %s, %s, %s, %s)"""
        val_sistema = (timestamp, hostname, sistema.total_processes, sistema.total_threads, sistema.active_users, sistema.uptime_seconds)
        cursor.execute(sql_sistema, val_sistema)

        # --- TABLA DISCO ---
        # Como por defecto la clase Disco lee la ruta raíz ('/'), lo ponemos como device_name
        sql_disco = """INSERT INTO Disco (fecha_creacion, hostname, device_name, space_total_mb, space_used_mb, space_used_percent, 
                       inodes_total, inodes_used, inodes_used_percent, iops_read, iops_write, latency_read_ms, latency_write_ms) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val_disco = (timestamp, hostname, '/', disco.space_total_mb, disco.space_used_mb, disco.space_used_percent, 
                     disco.inodes_total, disco.inodes_used, disco.inodes_used_percent, disco.iops_read, disco.iops_write, 
                     disco.latency_read_ms, disco.latency_write_ms)
        cursor.execute(sql_disco, val_disco)

        # --- TABLA RED (Múltiples interfaces) ---
        sql_red = """INSERT INTO Red (fecha_creacion, hostname, interface_name, bytes_sent, bytes_recv, packets_dropped, packets_errors, active_connections) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        valores_red = []
        for interface_name, metricas in red.interfaces.items():
            valores_red.append((timestamp, hostname, interface_name, metricas['bytes_sent'], metricas['bytes_recv'], 
                                metricas['packets_dropped'], metricas['packets_errors'], red.active_connections_total))
        cursor.executemany(sql_red, valores_red)

        # --- TABLA PROCESOS (Usando tu modelo "metricas_procesos" del historial) ---
        sql_procesos = """INSERT INTO Procesos (fecha_creacion, hostname, pid, process_name, cpu_usage_percent, ram_usage_mb, threads_count) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        valores_procesos = [
            (timestamp, hostname, p['pid'], p['process_name'], p['cpu_usage_percent'], p['ram_usage_mb'], p['threads_count'])
            for p in procesos.lista_procesos
        ]
        cursor.executemany(sql_procesos, valores_procesos)

        # Confirmamos la transacción (fundamental en InnoDB)
        db.commit()
        print(f"[{timestamp}] - Métricas insertadas correctamente en MySQL.")

    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
        # En caso de error, hacemos rollback para no dejar inserciones corruptas a medias
        if db:
            db.rollback()

def main():
    print("Iniciando agente de monitorización (Intervalo: 60s)")
    hostname, cpu, disco, memoria, procesos, red, sistema = inicializarVariables()
    
    print("Conectando a la base de datos...")
    db, cursor = conectar_base_datos()
    
    if not db:
        print("Saliendo. No se pudo establecer conexión con MySQL.")
        return

    while True:
        try:
            print("Recolectando métricas...")
            timestamp_actual = recolectarMetricas(cpu=cpu, disco=disco, memoria=memoria, procesos=procesos, red=red, sistema=sistema)
            guardarMetricas(db, cursor, timestamp_actual, hostname, cpu, disco, memoria, procesos, red, sistema)
        except Exception as e:
            print(f"Fallo en el bucle principal: {e}")
            try:
                db.ping(reconnect=True, attempts=3, delay=5)
            except:
                pass

        # Esperamos 60 segundos antes de la siguiente recolección
        time.sleep(60)

if __name__ == '__main__':
    main()