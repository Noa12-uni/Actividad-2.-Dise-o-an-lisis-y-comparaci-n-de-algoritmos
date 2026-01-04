import random
import math

def edge_cost(u, v, nodes):
    dx = nodes[u]["x"] - nodes[v]["x"]
    dy = nodes[u]["y"] - nodes[v]["y"]
    distance = math.hypot(dx, dy)
    risk = 0.05 * distance
    battery = 0.2 * distance
    return distance, risk, battery


def solve(instance, T=1000, alpha=0.995, iters=5000):
    nodes = instance["nodes"]
    hub = instance["hub"]
    N = len(nodes)

    # Solución inicial aleatoria
    perm = list(range(N))
    perm.remove(hub)
    random.shuffle(perm)
    path = [hub] + perm + [hub]

    def cost(path):
        d = r = b = 0
        for i in range(len(path) - 1):
            dist, risk, bat = edge_cost(path[i], path[i+1], nodes)
            d += dist
            r += risk
            b += bat
        return d + r + b   # escalar para SA

    best = path[:]
    best_cost = cost(path)

    current = path[:]
    current_cost = best_cost

    for _ in range(iters):
        i, j = sorted(random.sample(range(1, N), 2))
        new = current[:]
        new[i:j] = reversed(new[i:j])

        new_cost = cost(new)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new
            current_cost = new_cost

            if new_cost < best_cost:
                best = new
                best_cost = new_cost

        T *= alpha

    return [(best, best_cost)]