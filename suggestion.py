import collections
import pandas as pd
import json
import os


graph_path = "./cache/graph.json"


def build_graph(credit_file_path):
    """Given a file_path, using the file to create a graph

    Open the file, read each line of it and create a graph.
    graph[people1] = [movie1, movie2, movie3, ...]
    graph[movie1] = [people1, people2, people3, ...]

    Parameters
    ----------
    credit_file_path: str
        the file path that needs to load

    Returns
    -------
    graph: dict
        the dict to save the graph
    """
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

    with open(graph_path, "w") as f:
        json.dump(graph, f)


def load_graph(credit_file_path):
    if not os.path.exists(graph_path):
        build_graph(credit_file_path)

    with open(graph_path, "r") as f:
        return json.load(f)


def find_closest_people(graph, people, limit=50):
    """Using BFS to find the closest names

    Parameters
    ----------
    graph: dict
        the dict to save the graph
    people: str
        the target people
    limit: int
        the number of the closest peoples needed

    Returns
    -------
    list
        a list of names
    """
    if people not in graph:
        return []
    queue = collections.deque([people])
    visited = {people}
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

