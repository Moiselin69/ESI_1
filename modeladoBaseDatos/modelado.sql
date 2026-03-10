CREATE TABLE Cpu(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,

    cpu_load_percent DECIMAL(5,2) NOT NULL, -- 1. porcentaje de uso de la cpu
    cpu_freq_mhz DECIMAL(8,2) NOT NULL, -- 2. frecuencia de la cpu
    cpu_user_percent DECIMAL(5,2) NOT NULL, -- 3. porcentaje de tiempo que la cpu está con programas de usuario
    cpu_kernel_percent DECIMAL(5,2) NOT NULL, -- 4. porcentaje de tiempo que está la cpu con el kernel
    cpu_iowait_percent DECIMAL(5,2) NOT NULL, -- 5. porcentaje de tiempo inactivo esperando disco duro
    cpu_steal_percent DECIMAL(5,2) NOT NULL, -- 6. porcentaje de tiempo perdido esperando a que el servidor fisico nos asigne recursos
    cpu_inactive_percent DECIMAL(5,2) NOT NULL, -- 7. porcentaje de tiempo que la cpu estuvo libre, sin hacer nada
    cpu_interrupts BIGINT NOT NULL, -- 8. Cantidad de interrupciones, ya sean de teclado, de ratón etc 
    cpu_context_switches BIGINT NOT NULL, -- 9. cantidad de cambios de contexto 
    load_avg_1m DECIMAL(5,2) NOT NULL, -- 10. los tres signfican los procesos que están exigigiendo atención a la CPU 
    load_avg_5m DECIMAL(5,2) NOT NULL, -- 11
    load_avg_15m DECIMAL(5,2) NOT NULL, -- 12

    CONSTRAINT pk_cpu PRIMARY KEY(fecha_creacion, hostname)

)ENGINE=InnoDB;

CREATE TABLE Disco(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,
    device_name VARCHAR(50) NOT NULL,

    space_total_mb BIGINT NOT NULL, -- 1. espacio total del disco
    space_used_mb BIGINT NOT NULL, -- 2. espacio del disco utilizado
    space_used_percent DECIMAL(5,2) NOT NULL, -- 3. porcentaje de disco utilizado
    inodes_total BIGINT NOT NULL, -- 4. total de inodos 
    inodes_used BIGINT NOT NULL, -- 5. total de inodos utilizados
    inodes_used_percent DECIMAL(5,2) NOT NULL, -- 6. porcentaje de inodos utilizados
    iops_read INT NOT NULL, -- 7. Total de operaciones de lectura (acumulado)
    iops_write INT NOT NULL, -- 8. Total de operaciones de escritura (acumulado)
    latency_read_msDECIMAL(10,3) NOT NULL, -- 9. Tiempo total de lectura en ms (acumulado)
    latency_write_ms DECIMAL(8,2) NOT NULL, -- 10. Tiempo total de escritura en ms (acumulado)

    CONSTRAINT pk_disco PRIMARY KEY(fecha_creacion, hostname, device_name),
    INDEX idx_device_name (device_name)
)ENGINE=InnoDB;

CREATE TABLE Memoria(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL, 

    ram_total_mb BIGINT NOT NULL, -- 1. ram total de la maquina
    ram_used_mb BIGINT NOT NULL, -- 2. ram usado de la maquina
    ram_used_percent DECIMAL(5,2) NOT NULL, -- 3. porcentaje de ram usado
    swap_total_mb BIGINT NOT NULL, -- 4. espacio de swap total
    swap_used_mb BIGINT NOT NULL, -- 5. espacio de swap usado
    swap_used_percent DECIMAL(5,2) NOT NULL, -- 6. porcentaje de swap utilizado
    cache_used_mb BIGINT NOT NULL, -- 7. cache usado de la maquina
    cache_used_ram_mb BIGINT NOT NULL, -- 8. porcentaje de ram utilizada para cache
    page_faults_major INT NOT NULL, -- # 9. fallos de página

    CONSTRAINT pk_memoria PRIMARY KEY(fecha_creacion, hostname)
)ENGINE=InnoDB;

CREATE TABLE Procesos(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,

    pid INT NOT NULL, -- Identificador del proceso
    process_name VARCHAR(255) NOT NULL, -- Nombre del proceso (ej. mysql, apache2)
    
    cpu_usage_percent DECIMAL(5,2) NOT NULL, -- Porcentaje de uso de CPU
    ram_usage_mb DECIMAL(8,2) NOT NULL, -- Uso de memoria RAM en MB
    threads_count INT NOT NULL, -- Cantidad de hilos que está usando el proceso

    CONSTRAINT pk_procesos PRIMARY KEY(fecha_creacion, hostname, pid),
    INDEX idx_process_name (process_name) -- Índice muy útil para buscar en Grafana procesos concretos
)ENGINE=InnoDB;

CREATE TABLE Red(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,
    interface_name VARCHAR(50) NOT NULL,

    bytes_sent BIGINT NOT NULL, -- 1. Bytes enviados por el controlador de red
    bytes_recv BIGINT NOT NULL, -- 2. Bytes recibidos por el controlador
    packets_dropped INT NOT NULL, -- 3. Paquetes droppeados por el controlador
    packets_errors INT NOT NULL, -- 4. Error de paquetes
    active_connections INT NOT NULL, -- 5. Las conexiones activas del controlador

    CONSTRAINT pk_red PRIMARY KEY(fecha_creacion, hostname, interface_name)
)ENGINE=InnoDB;

CREATE TABLE Sistema(
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,

    total_processes INT NOT NULL, -- 1. total de procesos en activo
    total_threads INT NOT NULL, -- 2. total de hilos en activo
    active_users INT NOT NULL, -- 3. usuarios que están activos
    uptime_seconds BIGINT NOT NULL, -- 4. tiempo que lleva encendido el sistema

    CONSTRAINT pk_sistema PRIMARY KEY(fecha_creacion, hostname)
)ENGINE=InnoDB;
