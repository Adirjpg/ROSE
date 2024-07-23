from rose.common import obstacles, actions

driver_name = "bengervir"

def avoid(obstacle):
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.CRACK:
        return actions.JUMP

def safe_zone(world, x, y):
    """
    Check both left and right sides to find a clear path.
    """
    try:
        left_obstacle = world.get((x - 1, y))
    except IndexError:
        left_obstacle = obstacles.BARRIER  # Treat out of bounds as a barrier

    try:
        right_obstacle = world.get((x + 1, y))
    except IndexError:
        right_obstacle = obstacles.BARRIER  # Treat out of bounds as a barrier

    if left_obstacle in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
        return actions.RIGHT
    elif right_obstacle in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
        return actions.LEFT
    else:
        return actions.NONE  # If neither side is preferable, do nothing

def find_penguin_route(world, x, y):
    """
    Scan the upcoming positions to locate penguins and prioritize driving towards them,
    but also consider obstacles.
    """
    for i in range(1, 6):
        try:
            left_obstacle = world.get((x - 1, y - i))
            if left_obstacle == obstacles.PENGUIN:
                if not any(world.get((x - 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.LEFT  # Move left if there's a penguin ahead with no blocking obstacles
        except IndexError:
            pass

        try:
            right_obstacle = world.get((x + 1, y - i))
            if right_obstacle == obstacles.PENGUIN:
                if not any(world.get((x + 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.RIGHT  # Move right if there's a penguin ahead with no blocking obstacles
        except IndexError:
            pass

    return actions.NONE  # Default to moving forward if no penguins are found

def drive(world):
    x = world.car.x
    y = world.car.y

    next_position = (x, y - 1)
    
    try:
        obstacle = world.get(next_position)
    except IndexError:
        return actions.NONE

    if obstacle == obstacles.NONE:
        penguin_route = find_penguin_route(world, x, y)
        if penguin_route != actions.NONE:
            return penguin_route
        return actions.NONE  # Move forward if there's no obstacle and no better route
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP  # Pick up the penguin and move forward
    elif obstacle in [obstacles.WATER, obstacles.CRACK]:
        return avoid(obstacle)  # Avoid the obstacle based on its type
    elif obstacle in (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER):
        return safe_zone(world, x, y - 1)  # Check for a safe zone to turn
    else:
        return actions.NONE  # Default action if obstacle is unknown
