from rose.common import obstacles, actions
import queue

driver_name = "bengervir"
avoidable_obstacles = [obstacles.CRACK, obstacles.WATER]
prioQ = queue.Queue

def qInit(world, x, y, q: queue, rec_loop=5):
    pass  # Implementation needed based on game logic

def check_q(q:queue):
    if q.Empty():
        qInit()

def avoid(obstacle):
    """
    Define actions to avoid specific obstacles.
    """
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    else:
        return actions.NONE

def penguiner(world, x, y):
    """
    Check both left and right lanes to find the closest penguin.
    """
    left_penguin, right_penguin = float('inf'), float('inf')

    for i in range(1, 6):
        try:
            left_obstacle = world.get((x - 1, y - i))
            if left_obstacle == obstacles.PENGUIN:
                left_penguin = i
                break
        except IndexError:
            pass

        try:
            right_obstacle = world.get((x + 1, y - i))
            if right_obstacle == obstacles.PENGUIN:
                right_penguin = i
                break
        except IndexError:
            pass

    if left_penguin < right_penguin:
        return actions.LEFT
    elif right_penguin < left_penguin:
        return actions.RIGHT
    else:
        return actions.NONE

def safe_zone(world, x, y):
    """
    Check both left and right sides to find a clear path.
    """
    try:
        left_obstacle = world.get((x - 1, y))
    except IndexError:
        left_obstacle = obstacles.BARRIER

    try:
        right_obstacle = world.get((x + 1, y))
    except IndexError:
        right_obstacle = obstacles.BARRIER

    if left_obstacle in [obstacles.NONE, obstacles.PENGUIN] and right_obstacle in [obstacles.NONE, obstacles.PENGUIN]:
        return penguiner(world, x, y)

    if left_obstacle in [obstacles.NONE, obstacles.PENGUIN]:
        return actions.LEFT
    elif right_obstacle in [obstacles.NONE, obstacles.PENGUIN]:
        return actions.RIGHT
    else:
        return actions.NONE

def find_penguin_route(world, x, y):
    """
    Scan the upcoming positions to locate penguins and prioritize driving towards them,
    but also consider obstacles.
    """
    for i in range(1, 6):
        try:
            left_obstacle = world.get((x - 1, y - i))
            if left_obstacle == obstacles.PENGUIN or left_obstacle in avoidable_obstacles:
                if all(world.get((x - 1, y - j)) not in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.LEFT
        except IndexError:
            pass

        try:
            right_obstacle = world.get((x + 1, y - i))
            if right_obstacle == obstacles.PENGUIN or right_obstacle in avoidable_obstacles:
                if all(world.get((x + 1, y - j)) not in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.RIGHT
        except IndexError:
            pass

    return actions.NONE

def drive(world):
    """
    Main driving logic to navigate the car.
    """
    x, y = world.car.x, world.car.y

    next_position = (x, y - 1)
    
    try:
        obstacle = world.get(next_position)
    except IndexError:
        return actions.NONE

    if obstacle == obstacles.NONE:
        return find_penguin_route(world, x, y)
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle in avoidable_obstacles:
        return avoid(obstacle)
    elif obstacle in (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER):
        return safe_zone(world, x, y - 1)
    else:
        return actions.NONE
