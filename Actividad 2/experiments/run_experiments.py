from common.utils import measure, evaluate_path
from exact_bb.branch_and_bound import solve as bb
from geo_heuristic.visibility_heuristic import solve as geo
from metaheuristic.simulated_annealing import solve as sa


def measure_n_times(func, instance, n=5):
    times = []
    last_result = None
    last_mem = None

    for _ in range(n):
        result, t, mem = measure(func, instance)
        times.append(t)
        last_result = result
        last_mem = mem

    return last_result, sum(times) / n, last_mem


def run(instance):
    nodes = instance["nodes"]

    # ---------- BB (1 VEZ) ----------
    print("▶️ Ejecutando Branch & Bound...")
    bb_res = measure(bb, instance)

    if not bb_res[0]:
        print("⏱️ BB detenido por límite de tiempo")

    print("✅ BB terminado")

    # ---------- GEO (5 VECES) ----------
    print("▶️ Ejecutando heurística geométrica (GEO)...")
    geo_res = measure_n_times(geo, instance)
    print("✅ GEO terminado")

    # ---------- SA (5 VECES) ----------
    print("▶️ Ejecutando Simulated Annealing (SA)...")
    sa_res = measure_n_times(sa, instance)
    print("✅ SA terminado")

    # ---- Evaluación completa GEO y SA (riesgo y batería) ----
    geo_result, geo_time, geo_mem = geo_res
    geo_path = geo_result[0][0]
    geo_cost = evaluate_path(geo_path, nodes)

    sa_result, sa_time, sa_mem = sa_res
    sa_path = sa_result[0][0]
    sa_cost = evaluate_path(sa_path, nodes)

    # Devolvemos resultados enriquecidos
    geo_res = (geo_result, geo_time, geo_mem, geo_cost)
    sa_res = (sa_result, sa_time, sa_mem, sa_cost)

    return bb_res, geo_res, sa_res