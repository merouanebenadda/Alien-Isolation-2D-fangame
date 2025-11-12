import heapq
import math

inf = 1e12

def coordinate_to_index(i, j, width):
    return i + width*j

def index_to_coordinate(n, width):
    return (n%width, n//width)

def position(node, density):
    i, j = node
    return (density * i + density / 2, density * j + density / 2)

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path

def euclidian_distance(node, goal, density):
    x1, y1 = position(node, density)
    x2, y2 = position(goal, density)

    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def A_star(start, goal, mesh):
    density = mesh.density
    open_set = []
    closed_set = set()
    heapq.heapify(open_set)

    came_from = {}

    g_score = {(i, j): inf for i in range(mesh.width) for j in range(mesh.height)}
    g_score[start] = 0

    f_score = {(i, j): inf for i in range(mesh.width) for j in range(mesh.height)}
    f_score[start] = euclidian_distance(start, goal, density)

    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        
        if current in closed_set:
            continue
        closed_set.add(current)

        for neighbor in mesh.adjacency_map[current]:
            ((i, j), w) = neighbor
            tentative_g_score = g_score[current] + w
            if tentative_g_score < g_score[(i, j)]:
                came_from[(i, j)] = current
                g_score[(i, j)] = tentative_g_score
                f_score[(i, j)] = tentative_g_score + euclidian_distance((i,j), goal, density)
                if g_score[(i, j)] < inf:
                    heapq.heappush(open_set, (f_score[(i, j)], (i, j)))

    raise ValueError("A_star failed to find a path")