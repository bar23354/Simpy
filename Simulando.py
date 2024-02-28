# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos - 40
# Roberto Barreda - 23354

import simpy
import random
import math

RANDOM_SEED = 42
Procesos_Nuevos = 100
Procesos_entre_Intervalos = 10.0
Min_Espera = 1
Max_Espera = 3
RAM_CAPACITY = 100
CPU_SPEED = 3
tiempos_finalizacion = []

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

        # Pedir la memmoria
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
                    instrucciones_a_ejecutar = min(CPU_SPEED, self.instrucciones)
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
                        # Regresa a a estado de Ready nuevamente
                        print('%7.4f %s: Pasando a Ready' % (self.env.now, self.name))

                # Libera memoria y termina proceso
                yield self.ram.put(self.instrucciones)
                print('%7.4f %s: Liberando memoria y terminando' % (self.env.now, self.name))
                tiempos_finalizacion.append(self.env.now)