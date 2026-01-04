import json
import random

def generate_instance(n, filename):
    nodes = []
    for i in range(n):
        nodes.append({
            "id": i,
            "x": random.uniform(0, 10),
            "y": random.uniform(0, 10)
        })

    instance = {
        "hub": 0,
        "nodes": nodes,
        "no_fly_zones": [
            [[3, 3], [4, 3], [4, 4], [3, 4]]
        ]
    }

    with open(filename, "w") as f:
        json.dump(instance, f, indent=2)

for n in [10, 15, 20, 25]:
    generate_instance(n, f"instances/instance_{n}.json")