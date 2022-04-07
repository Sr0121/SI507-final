import collections
import pandas as pd
import json


def load_graph(credit_file_path):
    graph = collections.defaultdict(list)
    credit_data = pd.read_csv(credit_file_path)
    for _, row in credit_data.iterrows():
        casts = json.loads(row["cast"])
        for cast in casts:
            graph[row["title"]].append(cast["name"])
            graph[cast["name"]].append(row["title"])
        crews = json.loads(row["crew"])
        for crew in crews:
            graph[row["title"]].append(crew["name"])
            graph[crew["name"]].append(row["title"])
    return graph


def find_closest_staff(graph, staff, limit=50):
    if staff not in graph:
        return []
    queue = collections.deque([staff])
    visited = {staff}
    is_movie = True
    suggestions = []
    while queue and len(suggestions) < limit:
        s = len(queue)
        for _ in range(s):
            cur = queue.popleft()
            for neighbor in graph[cur]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if not is_movie:
                    suggestions.append(neighbor)
                queue.append(neighbor)
        is_movie = not is_movie
    if len(suggestions) >= limit:
        suggestions = suggestions[:limit]
    return suggestions

