
def main(csv_graph: str) -> list[list[int]]:
    edges = []
    vertices = set()
    for line in csv_graph.strip().splitlines():
        v_start, v_end = map(int, line.strip().split(','))
        edges.append((v_start, v_end))
        vertices.add(v_start)
        vertices.add(v_end)

    vertices_sorted = sorted(vertices)
    v_idx = {v: i for i, v in enumerate(vertices_sorted)}
    n = len(vertices_sorted)


    matrix = [[0 for _ in range(n)] for _ in range(n)]


    for v_start, v_end in edges:
        i = v_idx[v_start]
        j = v_idx[v_end]
        matrix[i][j] = 1

    return matrix
