

from typing import List, Tuple

def parse_csv_to_adj_matrix(csv_graph: str) -> Tuple[List[List[int]], List[int]]:
    edges = []
    vertices = set()
    for line in csv_graph.strip().splitlines():
        v_start, v_end = map(int, line.replace(' ', '').split(','))
        edges.append((v_start, v_end))
        vertices.add(v_start)
        vertices.add(v_end)
    vertices_sorted = sorted(vertices)
    v_idx = {v: i for i, v in enumerate(vertices_sorted)}
    n = len(vertices_sorted)
    matrix = [[0]*n for _ in range(n)]
    for v_start, v_end in edges:
        matrix[v_idx[v_start]][v_idx[v_end]] = 1
    return matrix, vertices_sorted

def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*matrix)]

def is_symmetric(matrix: List[List[int]]) -> bool:
    return matrix == transpose_matrix(matrix)

def main(csv_graph: str):
    adj_matrix, vertices = parse_csv_to_adj_matrix(csv_graph)
    print("Матрица смежности:")
    for row in adj_matrix:
        print(' '.join(map(str, row)))
    adj_matrix_T = transpose_matrix(adj_matrix)
    print("\nТранспонированная матрица:")
    for row in adj_matrix_T:
        print(' '.join(map(str, row)))
    print("\nСимметрична ли матрица?:", is_symmetric(adj_matrix))
    return adj_matrix, adj_matrix_T