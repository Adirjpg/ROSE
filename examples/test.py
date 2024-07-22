from rose.common import obstacles, actions
import heapq

driver_name = "Michael Schumacher"

def get_points(obstacle):
    if obstacle == obstacles.NONE:
        return 10
    elif obstacle == obstacles.PENGUIN:
        return 20
    elif obstacle == obstacles.WATER:
        return 4
    elif obstacle == obstacles.CRACK:
        return 5
    else:
        return -10

def get_neighbors(pos, width):
    x, y = pos
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y - 1, actions.LEFT))
    if x < width - 1:
        neighbors.append((x + 1, y - 1, actions.RIGHT))
    neighbors.append((x, y - 1, actions.NONE))
    return neighbors

def heuristic(pos):
    x, y = pos
    return y

def a_star(start, world):
    width = world.width
    open_set = []
    heapq.heappush(open_set, (0, start, [], 0))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}

    while open_set:
        _, current, path, current_points = heapq.heappop(open_set)

        if current[1] == 0:
            return path, current_points

        for neighbor in get_neighbors(current, width):
            x, y, action = neighbor
            if y < 0 or x < 0 or x >= width:
                continue

            try:
                obstacle = world.get((x, y))
            except IndexError:
                continue

            tentative_g_score = g_score[current] + 1
            tentative_points = current_points + get_points(obstacle)

            if (x, y) not in g_score or tentative_g_score < g_score[(x, y)]:
                came_from[(x, y)] = (current, action)
                g_score[(x, y)] = tentative_g_score
                f_score[(x, y)] = tentative_g_score + heuristic((x, y))
                heapq.heappush(open_set, (f_score[(x, y)], (x, y), path + [action], tentative_points))

    return [], 0

def drive(world):
    x = world.car.x
    y = world.car.y
    start = (x, y)
    path, points = a_star(start, world)

    if path:
        return path[0]
    else:
        return actions.NONE
