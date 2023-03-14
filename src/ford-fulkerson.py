import sys


def read_adjacency_array(get_line):
    adjacency_array = [int(x) for x in get_line().split()]
    while adjacency_array[-1] != 32767:
        adjacency_array += [int(x) for x in get_line().split()]
    return adjacency_array


def read(get_line):
    get_line()
    n = int(get_line())
    adjacency_array = read_adjacency_array(get_line)
    i, s, t = 0, -1, -2
    edges = set()
    X = []
    adjacency_lists = {s: set(), t: set()}
    while adjacency_array[i] != n:
        start_index = adjacency_array[i]
        end_index = adjacency_array[i + 1]
        v = str(i + 1)
        i += 1
        X.append(v)
        adjacency_lists[s].add((v, True))
        adjacency_lists[v] = {(s, False)}
        edges.add((s, v))
        if start_index == 0:
            continue
        for j in range(start_index, end_index):
            w = adjacency_array[j - 1]
            if w not in adjacency_lists:
                adjacency_lists[w] = set()
            edges.add((v, w))
            adjacency_lists[v].add((w, True))
            adjacency_lists[w].add((v, False))

            edges.add((w, t))
            adjacency_lists[w].add((t, True))
            adjacency_lists[t].add((w, False))

    return adjacency_lists, edges, X


def get_delta_for_chain(chain, flow, c):
    return min(get_delta_for_e(e, is_direct, flow, c) for e, is_direct in chain.values())


def get_delta_for_e(e, is_direct, flow, c):
    return c[e] - flow[e] if is_direct else flow[(e[1], e[0])]


def sgn(direct):
    return 1 if direct else -1


def update_flow(chain, flow, c):
    delta = get_delta_for_chain(chain, flow, c)
    for e, direct in chain.values():
        edge = e if direct else (e[1], e[0])
        flow[edge] = flow[edge] + delta * sgn(direct)
    return flow


def find_f_additional_chain(path, source, adjacency_lists, target, flow, c):
    if source == target:
        return path
    for neighbour, is_direct in adjacency_lists[source]:
        if neighbour in path:
            continue
        delta = get_delta_for_e((source, neighbour), is_direct, flow, c)
        if delta > 0:
            new_path = path.copy()
            new_path[source] = ((source, neighbour), is_direct)
            result = find_f_additional_chain(
                new_path, neighbour, adjacency_lists, target, flow, c)
            if result is not None:
                return result
    return None


def build_max_flow(edges, adjacency_lists, source, target, c):
    flow = {e: 0 for e in edges}
    chain = find_f_additional_chain({}, source, adjacency_lists, target, flow, c)
    while chain is not None:
        flow = update_flow(chain, flow, c)
        chain = find_f_additional_chain({}, source, adjacency_lists, target, flow, c)
    return flow


INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]


if __name__ == '__main__':
    with open(INPUT_FILE) as f:
        adjacency_lists, edges, X = read(f.readline)

    c = {e: 1 for e in edges}
    flow = build_max_flow(edges, adjacency_lists, -1, -2, c)
    matching = {}
    for k, value in flow.items():
        v, w = k
        if value > 0 and int(v) > 0 and int(w) > 0:
            matching[v] = w
    result = [str(matching[x]) if x in matching else '0' for x in X]

    with open(OUTPUT_FILE, 'w') as f:
        f.write(' '.join(result))
