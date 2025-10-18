

from typing import List, Tuple

def main(s: str, e: str) -> Tuple[List[List[bool]], List[List[bool]], List[List[bool]], List[List[bool]], List[List[bool]]]:

    edges = [tuple(map(int, line.split(','))) for line in s.strip().split('\n')]
    nodes = sorted(set(sum(([u, v] for u, v in edges), [])))
    n = max(nodes)

    adj = {i: [] for i in nodes}
    for u, v in edges:
        adj[u].append(v)

    def init_matrix():
        return [[False] * n for _ in range(n)]

    M1 = init_matrix()
    for u, v in edges:
        M1[u-1][v-1] = True

    M2 = init_matrix()
    def dfs(u, visited, parent):
        for v in adj[u]:
            if not M2[parent-1][v-1]:
                M2[parent-1][v-1] = True
                dfs(v, visited, parent)
    for node in nodes:
        dfs(node, set(), node)

    M3 = [[M2[j][i] for j in range(n)] for i in range(n)]

    M4 = [[M2[i][j] or M3[i][j] for j in range(n)] for i in range(n)]

    M5 = [[not M4[i][j] and i != j for j in range(n)] for i in range(n)]

    return M1, M2, M3, M4, M5

# Пример из задачи
if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    root = "1"
    result = main(s, root)
    for i, matrix in enumerate(result, start=1):
        print(f"\nMatrix {i}:")
        for row in matrix:
            print(row)
