import json
from typing import List, Union, Tuple, Set

RankItem = Union[int, List[int]]
Ranking = List[RankItem]


def _parse_ranking(json_str: str) -> Ranking:
    data = json.loads(json_str)
    ranking: Ranking = []
    for item in data:
        if isinstance(item, list):
            ranking.append([int(x) for x in item])
        else:
            ranking.append(int(item))
    return ranking


def _collect_objects(r1: Ranking, r2: Ranking) -> List[int]:
    objs: Set[int] = set()
    for r in (r1, r2):
        for item in r:
            if isinstance(item, list):
                objs.update(item)
            else:
                objs.add(item)
    return sorted(objs)


def _build_relation_matrix(r: Ranking, objects: List[int]) -> List[List[int]]:
    pos = {}
    for k, item in enumerate(r):
        if isinstance(item, list):
            for o in item:
                pos[o] = k
        else:
            pos[item] = k

    n = len(objects)
    Y = [[0] * n for _ in range(n)]
    for i, oi in enumerate(objects):
        for j, oj in enumerate(objects):
            if oi == oj:
                Y[i][j] = 1
                continue
            if oi not in pos or oj not in pos:
                continue
            if pos[oj] >= pos[oi]:
                Y[i][j] = 1
    return Y


def _transpose(M: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*M)]


def _bool_or(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[1 if A[i][j] or B[i][j] else 0 for j in range(n)] for i in range(n)]


def _bool_and(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[1 if A[i][j] and B[i][j] else 0 for j in range(n)] for i in range(n)]


def _warshall(E: List[List[int]]) -> None:
    n = len(E)
    for k in range(n):
        for i in range(n):
            if E[i][k]:
                for j in range(n):
                    if E[k][j]:
                        E[i][j] = 1


def _matrix_product_bool(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    m = len(B[0])
    kdim = len(B)
    R = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            v = 0
            for k in range(kdim):
                if A[i][k] and B[k][j]:
                    v = 1
                    break
            R[i][j] = v
    return R


def _kernel_of_contradictions(YA: List[List[int]], YB: List[List[int]]) -> List[Tuple[int, int]]:
    YAt = _transpose(YA)
    YBt = _transpose(YB)
    term1 = _matrix_product_bool(YA, YBt)
    term2 = _matrix_product_bool(YAt, YB)
    P = _bool_or(term1, term2)
    n = len(P)
    kernel = []
    for i in range(n):
        for j in range(i + 1, n):
            if P[i][j] == 0 and P[j][i] == 0:
                kernel.append((i, j))
    return kernel


def _build_consensus_ranking(YA: List[List[int]], YB: List[List[int]], objects: List[int]) -> Ranking:
    n = len(objects)

    C = _matrix_product_bool(YA, YB)

    kernel = _kernel_of_contradictions(YA, YB)
    for i, j in kernel:
        C[i][j] = 1
        C[j][i] = 1

    Ct = _transpose(C)
    E = _matrix_product_bool(C, Ct)
    _warshall(E)

    visited = [False] * n
    clusters: List[List[int]] = []
    for i in range(n):
        if not visited[i]:
            comp = []
            stack = [i]
            visited[i] = True
            while stack:
                v = stack.pop()
                comp.append(objects[v])
                for u in range(n):
                    if not visited[u] and E[v][u] and E[u][v]:
                        visited[u] = True
                        stack.append(u)
            comp.sort()
            clusters.append(comp)

    def cluster_before(a: List[int], b: List[int]) -> bool:
        idx = {obj: i for i, obj in enumerate(objects)}
        better_ab = 0
        better_ba = 0
        for oa in a:
            ia = idx[oa]
            for ob in b:
                ib = idx[ob]
                if C[ia][ib] and not C[ib][ia]:
                    better_ab += 1
                elif C[ib][ia] and not C[ia][ib]:
                    better_ba += 1
        return better_ab > better_ba

    ordered: List[List[int]] = []
    for cl in clusters:
        inserted = False
        for k in range(len(ordered)):
            if cluster_before(cl, ordered[k]):
                ordered.insert(k, cl)
                inserted = True
                break
        if not inserted:
            ordered.append(cl)

    result: Ranking = []
    for cl in ordered:
        if len(cl) == 1:
            result.append(cl[0])
        else:
            result.append(cl)
    return result


def main(ranking_a_json: str, ranking_b_json: str) -> str:
    rA = _parse_ranking(ranking_a_json)
    rB = _parse_ranking(ranking_b_json)
    objects = _collect_objects(rA, rB)
    YA = _build_relation_matrix(rA, objects)
    YB = _build_relation_matrix(rB, objects)
    consensus = _build_consensus_ranking(YA, YB, objects)
    return json.dumps(consensus, ensure_ascii=False)




