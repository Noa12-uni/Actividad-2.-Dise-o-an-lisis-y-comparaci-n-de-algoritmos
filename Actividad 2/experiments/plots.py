import matplotlib.pyplot as plt
import math


# --------------------------------------------------
# Diversidad de la frontera de Pareto (2D)
# --------------------------------------------------
def diversity_2d(pareto):
    """
    Calcula la diversidad como la distancia media euclídea
    entre soluciones consecutivas de la frontera de Pareto.
    """
    if len(pareto) < 2:
        return 0

    pareto = sorted(pareto, key=lambda x: x[0])  # ordenar por distancia
    distances = []

    for i in range(len(pareto) - 1):
        d1, r1 = pareto[i]
        d2, r2 = pareto[i + 1]
        distances.append(math.hypot(d2 - d1, r2 - r1))

    return sum(distances) / len(distances)


# --------------------------------------------------
# Hipervolumen dominado (2D)
# --------------------------------------------------
def hypervolume_2d(pareto, ref):
    """
    Calcula el hipervolumen en 2D (distancia, riesgo)
    pareto: lista de (distancia, riesgo)
    ref: punto de referencia (dist_ref, risk_ref)
    """
    pareto = sorted(pareto, key=lambda x: x[0])
    hv = 0
    prev_d = ref[0]

    for d, r in pareto:
        hv += (prev_d - d) * (ref[1] - r)
        prev_d = d

    return hv


# --------------------------------------------------
# Gráficas principales
# --------------------------------------------------
def plot_results(all_results):
    Ns = []

    times_bb, times_geo, times_sa = [], [], []
    best_bb, geo_dist, sa_dist = [], [], []
    hypervolumes = []
    diversities = []

    # ===============================
    # Recogida de datos
    # ===============================
    for N, bb_res, geo_res, sa_res in all_results:
        Ns.append(N)

        # ---------- TIEMPOS ----------
        times_bb.append(bb_res[1] if bb_res[0] else None)
        times_geo.append(geo_res[1])
        times_sa.append(sa_res[1])

        # ---------- DISTANCIA ----------
        # Branch & Bound
        if bb_res[0]:
            best_bb.append(min(sol[1][0] for sol in bb_res[0]))
        else:
            best_bb.append(None)

        # GEO y SA (evaluados a posteriori)
        geo_dist.append(geo_res[3][0])
        sa_dist.append(sa_res[3][0])

        # ---------- HIPERVOLUMEN y DIVERSIDAD (BB) ----------
        if bb_res[0]:
            pareto = [(sol[1][0], sol[1][1]) for sol in bb_res[0]]

            ref_dist = max(p[0] for p in pareto) * 1.1
            ref_risk = max(p[1] for p in pareto) * 1.1

            hv = hypervolume_2d(pareto, (ref_dist, ref_risk))
            div = diversity_2d(pareto)
        else:
            hv = 0
            div = 0

        hypervolumes.append(hv)
        diversities.append(div)

    # ===============================
    # GRÁFICA 1: TIEMPO vs N (LOG)
    # ===============================
    plt.figure()
    plt.plot(Ns, times_bb, marker="o", label="BB")
    plt.plot(Ns, times_geo, marker="o", label="GEO")
    plt.plot(Ns, times_sa, marker="o", label="SA")
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Tiempo medio (s)")
    plt.yscale("log")
    plt.title("Tiempo de ejecución vs N (escala logarítmica)")
    plt.legend()
    plt.savefig("grafica_tiempos.png")
    plt.close()
    print("📁 Guardada: grafica_tiempos.png")

    # ===============================
    # GRÁFICA 2: CALIDAD (DISTANCIA)
    # ===============================
    plt.figure()
    plt.plot(Ns, best_bb, marker="o", label="BB (mejor)")
    plt.plot(Ns, geo_dist, marker="o", label="GEO")
    plt.plot(Ns, sa_dist, marker="o", label="SA")
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Distancia total")
    plt.title("Calidad de las soluciones")
    plt.legend()
    plt.savefig("grafica_calidad.png")
    plt.close()
    print("📁 Guardada: grafica_calidad.png")

    # ===============================
    # GRÁFICA 3: HIPERVOLUMEN
    # ===============================
    plt.figure()
    plt.plot(Ns, hypervolumes, marker="o", label="BB")
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Hipervolumen")
    plt.title("Hipervolumen dominado (Branch & Bound)")
    plt.legend()
    plt.savefig("grafica_hipervolumen.png")
    plt.close()
    print("📁 Guardada: grafica_hipervolumen.png")

    # ===============================
    # GRÁFICA 4: DIVERSIDAD
    # ===============================
    plt.figure()
    plt.plot(Ns, diversities, marker="o", label="BB")
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Diversidad media")
    plt.title("Diversidad de la frontera de Pareto (Branch & Bound)")
    plt.legend()
    plt.savefig("grafica_diversidad.png")
    plt.close()
    print("📁 Guardada: grafica_diversidad.png")