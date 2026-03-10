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
        print("Error al conectar a la base de datos")
        return 

def recolectarMetricas(cpu:CPU, disco:Disco, memoria:Memoria, procesos:Procesos, red:Red, sistema:Sistema):
    cpu.recolectar_metricas()
    disco.recolectarMetricas()
    memoria.recolectarMetricas()
    procesos.recolectar_metricas()
    red.recolectar_metricas()
    sistema.recolectarMetricas()
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    print(f"Iniciando agente de monitorización (Intervalo: 60s)")
    hostname, cpu, disco, memoria, procesos, red, sistema = inicializarVariables()
    print("Conectando a la base de datos")
    db, cursor = conectar_base_datos()
    while True:
        print("Recolectando Metricas")
        timestamp_actual = recolectarMetricas(cpu=cpu, disco=disco, memoria=memoria, procesos=procesos, red=red, sistema=sistema)
if __name__ == '__main__':
    main()