# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos - 40
# Roberto Barreda - 23354

import simpy
import random
import math
import matplotlib.pyplot as plt

RANDOM_SEED = 42

class Proceso:
    def __init__(self, env, name, procesador, ram, time_in_processor, instrucciones):
        self.env = env
        self.name = name
        self.procesador = procesador
        self.ram = ram
        self.time_in_processor = time_in_processor
        self.instrucciones = instrucciones

    def run(self):
        Llegada = self.env.now
        print('%7.4f %s: Entrando' % (Llegada, self.name))

        # Pedir la memoria
        with self.ram.get(self.instrucciones) as req:
            yield req  # esta parte es para esperar

            # Proceso en estado "ready"
            print('%7.4f %s: Listo para ejecutar' % (self.env.now, self.name))

            # Uso del CPU
            with self.procesador.request() as req_cpu:
                yield req_cpu  # Espera
                print('%7.4f %s: Utilizando CPU' % (self.env.now, self.name))

                # Instrucciones
                while self.instrucciones >= 3:
                    instrucciones_a_ejecutar = min(self.instrucciones, CPU_SPEED)
                    self.instrucciones -= instrucciones_a_ejecutar

                    # Simulación del tiempo de ejecución
                    yield self.env.timeout(instrucciones_a_ejecutar / CPU_SPEED)

                    # Simulación de posibles transiciones (waiting, ready, terminated)
                    if random.randint(1, 21) == 1:
                        # Pasando a estado de Waiting para I/O
                        print('%7.4f %s: Pasando a Waiting' % (self.env.now, self.name))
                        yield self.env.timeout(random.uniform(1, 21))
                        print('%7.4f %s: Regresando a Ready desde Waiting' % (self.env.now, self.name))
                    elif random.randint(1, 2) == 2:
                        # Regresa a estado de Ready nuevamente
                        print('%7.4f %s: Pasando a Ready' % (self.env.now, self.name))

                # Libera memoria y termina proceso
                yield self.ram.put(1)
                print('%7.4f %s: Liberando memoria y terminando' % (self.env.now, self.name))
                TiempoConcluido.append(self.env.now)


def source(env, number, interval, procesador, ram):
    for i in range(number):
        instrucciones = random.randint(1, 10)
        p = Proceso(env, 'Proceso%02d' % i, procesador, ram, time_in_processor=3.0, instrucciones=instrucciones)
        env.process(p.run())
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def run_simulation(num_procesos, intervalo_llegada, RAM_CAPACITY, CPU_SPEED):
    global TiempoConcluido

    TiempoConcluido = []

    print(f"Simulación con {num_procesos} procesos, intervalo de llegada {intervalo_llegada}, capacidad de RAM {RAM_CAPACITY}, velocidad de CPU {CPU_SPEED}")

    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    procesador = simpy.Resource(env, capacity=1)
    env.process(source(env, num_procesos, intervalo_llegada, procesador, ram))
    env.run()

    # Stats
    media = sum(TiempoConcluido) / len(TiempoConcluido)
    print("Media de los tiempos de finalización:", media)

    diferencias_cuadradas = [(tiempo - media) ** 2 for tiempo in TiempoConcluido]
    media_cuadrados_diferencias = sum(diferencias_cuadradas) / len(diferencias_cuadradas)
    desviacion_estandar = math.sqrt(media_cuadrados_diferencias)
    print("Desviación estándar de los tiempos de finalización:", desviacion_estandar)

    # Crear histograma del tiempo de finalización
    plt.hist(TiempoConcluido, bins=20, edgecolor='black')
    plt.title('Histograma del Tiempo de Finalización')
    plt.xlabel('Tiempo de Finalización')
    plt.ylabel('Frecuencia')
    plt.show()

    # Crear gráfica de línea del tiempo promedio
    NumListaProceso = [25, 50, 100, 150, 200]  # Puedes ajustar esta lista según tus experimentos
    AverageTime = []

    for num_proceso in NumListaProceso:
        tiempos_finalizacion = []
        env = simpy.Environment()
        ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
        procesador = simpy.Resource(env, capacity=1)
        env.process(source(env, num_proceso, intervalo_llegada, procesador, ram))
        env.run()
        AverageTime.append(sum(tiempos_finalizacion) / len(tiempos_finalizacion))

    plt.plot(NumListaProceso, AverageTime, marker='o')
    plt.title('Número de Procesos vs Tiempo Promedio de Ejecución')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Tiempo Promedio de Ejecución')
    plt.show()


# Parámetros iniciales
NuevoProceso = 100
IntervalosProcesos = 10.0
RAM_CAPACITY = 100
CPU_SPEED = 3

# Correr la simulación con los parámetros iniciales
run_simulation(NuevoProceso, IntervalosProcesos, RAM_CAPACITY, CPU_SPEED)
