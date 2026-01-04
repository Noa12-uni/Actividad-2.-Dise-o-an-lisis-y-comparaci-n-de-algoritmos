import math
import time
from common.geometry import segment_intersects_polygon


# ---------------- EXCEPCIÓN DE TIEMPO ----------------
class TimeLimitReached(Exception):
    pass


# ---------------- COSTE DE ARISTA ----------------
def edge_cost(u, v, nodes):
    dx = nodes[u]["x"] - nodes[v]["x"]
    dy = nodes[u]["y"] - nodes[v]["y"]
    distance = math.hypot(dx, dy)
    risk = 0.05 * distance
    battery = 0.2 * distance
    return distance, risk, battery


# ---------------- BRANCH & BOUND ----------------
def solve(instance, time_limit=120):  # 2 minutos
    start_time = time.time()

    nodes = instance["nodes"]
    no_fly = instance["no_fly_zones"]
    hub = instance["hub"]
    N = len(nodes)

    best_solutions = []
    best_distance = float("inf")

    def valid_edge(u, v):
        if not no_fly:
            return True

        p1 = (nodes[u]["x"], nodes[u]["y"])
        p2 = (nodes[v]["x"], nodes[v]["y"])

        for poly in no_fly:
            if segment_intersects_polygon(p1, p2, poly):
                return False
        return True

    def path_cost(path):
        d = r = b = 0
        for i in range(len(path) - 1):
            dist, risk, bat = edge_cost(path[i], path[i + 1], nodes)
            d += dist
            r += risk
            b += bat
        return d, r, b

    def lower_bound_distance(path):
        d, _, _ = path_cost(path)
        remaining = N - len(path) + 1  # volver al hub
        return d + remaining * 0.1

    def backtrack(path, visited):
        nonlocal best_distance

        # ⏱️ Límite de tiempo
        if time.time() - start_time > time_limit:
            raise TimeLimitReached

        # ✂️ Poda
        if lower_bound_distance(path) >= best_distance:
            return

        # ✅ Caso base
        if len(path) == N:
            if valid_edge(path[-1], hub):
                full_path = path + [hub]
                d, r, b = path_cost(full_path)

                if d <= best_distance:
                    best_distance = d
                    best_solutions.append((full_path, (d, r, b)))
            return

        # 🔁 Expansión
        for v in range(N):
            if v not in visited and valid_edge(path[-1], v):
                visited.add(v)
                backtrack(path + [v], visited)
                visited.remove(v)

    # -------- LLAMADA ÚNICA AL BACKTRACK --------
    try:
        backtrack([hub], {hub})
    except TimeLimitReached:
        pass

    return best_solutions