# Actividad 2 – Planificación de rutas con restricciones

Este repositorio contiene la implementación de la Actividad 2 de la asignatura,
centrada en la planificación de rutas para un dron de reparto en un entorno
urbano con restricciones geométricas (zonas no-fly).

El problema se modela como un circuito Hamiltoniano multiobjetivo, donde se
minimizan simultáneamente la distancia recorrida, el riesgo acumulado y el
consumo de batería.

---

## 📂 Estructura del proyecto

- exact_bb/  
  Implementación del algoritmo exacto Branch & Bound con poda y límite de tiempo.

- geo_heuristic/  
  Heurística geométrica basada en visibilidad para la generación rápida de rutas.

- metaheuristic/  
  Implementación de la metaheurística Simulated Annealing.

- common/  
  Funciones auxiliares para evaluación de rutas, intersección geométrica y medida
  de tiempo y memoria.

- experiments/  
  Ejecución de experimentos y generación de gráficas.

- instances/  
  Conjunto de instancias del problema en formato JSON (N = 10, 15, 20, 25).

- main.py  
  Script principal para la ejecución de los algoritmos y los experimentos.

---

## ▶️ Ejecución

Para ejecutar los experimentos, basta con lanzar el script principal:

python main.py
