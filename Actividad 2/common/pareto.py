def dominates(a, b):
    return all(x <= y for x,y in zip(a,b)) and any(x < y for x,y in zip(a,b))

def pareto_front(solutions):
    front = []
    for s in solutions:
        if not any(dominates(o[1], s[1]) for o in solutions):
            front.append(s)
    return front