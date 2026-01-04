import math
import time
from common.geometry import segment_intersects_polygon


def solve(instance, time_limit=10):
    """
    Heurística geométrica con límite de tiempo (1 minuto).
    """
    start_time = time.time()

    nodes = instance["nodes"]
    hub = instance["hub"]
    no_fly = instance["no_fly_zones"]

    unvisited = set(range(len(nodes)))
    path = [hub]
    unvisited.remove(hub)

    def dist(a, b):
        return math.hypot(
            nodes[a]["x"] - nodes[b]["x"],
            nodes[a]["y"] - nodes[b]["y"]
        )

    while unvisited:
        # ⏱️ COMPROBACIÓN DE TIEMPO
        if time.time() - start_time > time_limit:
            print("⏱️ GEO: límite de tiempo alcanzado (1 minuto)")
            break

        curr = path[-1]
        candidates = sorted(unvisited, key=lambda x: dist(curr, x))

        found = False
        for c in candidates:
            if time.time() - start_time > time_limit:
                print("⏱️ GEO: límite de tiempo alcanzado (1 minuto)")
                found = True
                break

            p1 = (nodes[curr]["x"], nodes[curr]["y"])
            p2 = (nodes[c]["x"], nodes[c]["y"])

            if not any(segment_intersects_polygon(p1, p2, poly) for poly in no_fly):
                path.append(c)
                unvisited.remove(c)
                found = True
                break

        if not found:
            # No se pudo avanzar (bloqueo geométrico)
            break

    path.append(hub)
    return [(path, None)]