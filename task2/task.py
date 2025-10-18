from typing import List, Tuple
import math

def main(s: str, e: str) -> Tuple[float, float]:

    edges = [tuple(map(int, line.split(','))) for line in s.strip().split('\n')]
    nodes = sorted(set(sum(([u, v] for u, v in edges), [])))
    n = len(nodes)

    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v)

    out_degrees = [len(adj[i]) for i in nodes]
    total_edges = sum(out_degrees)

    p = [deg / total_edges for deg in out_degrees if total_edges > 0]

    H = -sum(pi * math.log2(pi) for pi in p if pi > 0)

    H_max = math.log2(n) if n > 1 else 0

    C_norm = (H / H_max) if H_max > 0 else 0

    return round(H, 1), round(C_norm, 1)


# Пример
if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    root = "1"
    entropy, complexity = main(s, root)
    print(f"Entropy: {entropy}, Normalized Complexity: {complexity}")
