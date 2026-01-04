from common.utils import load_instance
from experiments.run_experiments import run
from experiments.plots import plot_results

INSTANCES = [
    ("instances/instance_10.json", 10),
    ("instances/instance_15.json", 15),
    ("instances/instance_20.json", 20),
    ("instances/instance_25.json", 25),
]

all_results = []

for path, N in INSTANCES:
    print("\n======================================")
    print(f"📦 INSTANCIA N = {N}")
    print("======================================")

    instance = load_instance(path)
    bb_res, geo_res, sa_res = run(instance)

    # ---------- MOSTRAR RESULTADOS POR PANTALLA ----------
    print("\n📌 RESULTADOS FINALES")

    # --- BB ---
    bb_solutions, bb_time, _ = bb_res
    print("\n🔵 Branch & Bound")

    print(f"  Tiempo de ejecución (s): {bb_time:.4f}")
    print(f"  Nº soluciones no dominadas: {len(bb_solutions)}")

    if bb_solutions:
        best_d = min(sol[1][0] for sol in bb_solutions)
        best_r = min(sol[1][1] for sol in bb_solutions)
        best_b = min(sol[1][2] for sol in bb_solutions)

        print(f"  Mejor distancia: {best_d:.2f}")
        print(f"  Riesgo asociado: {best_r:.2f}")
        print(f"  Batería consumida: {best_b:.2f}")
    else:
        print("  Mejor distancia: —")
        print("  Riesgo asociado: —")
        print("  Batería consumida: —")

    # --- GEO ---
    geo_solution, geo_time, geo_mem, geo_cost = geo_res
    geo_dist, geo_risk, geo_bat = geo_cost

    print("\n🟢 Heurística geométrica (GEO)")
    print(f"  Ruta: {geo_solution[0][0]}")
    print(f"  Distancia: {geo_dist:.2f}")
    print(f"  Riesgo: {geo_risk:.2f}")
    print(f"  Batería: {geo_bat:.2f}")
    print(f"  Tiempo de ejecución: {geo_time:.4f} s")

    # --- SA ---
    sa_solution, sa_time, sa_mem, sa_cost = sa_res
    sa_dist, sa_risk, sa_bat = sa_cost

    print("\n🟠 Simulated Annealing (SA)")
    print(f"  Ruta: {sa_solution[0][0]}")
    print(f"  Distancia: {sa_dist:.2f}")
    print(f"  Riesgo: {sa_risk:.2f}")
    print(f"  Batería: {sa_bat:.2f}")
    print(f"  Tiempo de ejecución: {sa_time:.4f} s")

    # Guardamos resultados para gráficas
    all_results.append((N, bb_res, geo_res, sa_res))

# ---------- GRÁFICAS ----------
print("\n📊 Generando gráficas con las 4 instancias...")
plot_results(all_results)
print("✅ Ejecución finalizada")