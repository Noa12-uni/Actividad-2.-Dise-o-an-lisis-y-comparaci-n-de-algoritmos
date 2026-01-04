import json
import time
import tracemalloc
from exact_bb.branch_and_bound import edge_cost

def evaluate_path(path, nodes):
    """
    Evalúa una ruta completa devolviendo
    (distancia, riesgo, batería)
    """
    d = r = b = 0
    for i in range(len(path) - 1):
        dist, risk, bat = edge_cost(path[i], path[i + 1], nodes)
        d += dist
        r += risk
        b += bat
    return d, r, b

def load_instance(path):
    with open(path) as f:
        return json.load(f)

def measure(func, *args):
    tracemalloc.start()
    start = time.time()

    result = func(*args)

    elapsed = time.time() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, elapsed, peak / 1024  # KB

