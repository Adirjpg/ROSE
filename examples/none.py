from rose.common import obstacles, actions

driver_name = "bengervir"
avoidable_obstacles = [obstacles.CRACK, obstacles.WATER]

def avoid(obstacle):
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    return actions.JUMP


def penguiner(world, x, y):
    """
    Checking both left and right lanes to find the closest penguin.
    """
    left_penguin = 0
    right_penguin = 0

    left_flag = False
    right_flag = False

    for i in range(1, 6):
        try:# Locating the closest penguin in the left lane
            left_obstacle = world.get((x - 1, y - i))
        except IndexError:
            left_obstacle = obstacles.BARRIER  # Treat out of bounds as a barrier
        if left_obstacle in [obstacles.CRACK, obstacles.PENGUIN, obstacles.WATER] and not left_flag:
            left_penguin = i
            left_flag = True
            
        try:# Locating the closest penguin in the right lane
            right_obstacle = world.get((x + 1, y - i))
        except IndexError:
            right_obstacle = obstacles.BARRIER  # Treat out of bounds as a barrier
        if right_obstacle in [obstacles.CRACK, obstacles.PENGUIN, obstacles.WATER] and not right_flag:
            right_penguin = i
            right_flag = True
            
    
    if left_penguin < right_penguin:# Shifting the car based on the lane with the closest penguin
        return actions.LEFT
    return actions.RIGHT


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
    
    if left_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER] and right_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER]:
        return find_penguin_route(world, x, y + 1)
    
    if left_obstacle == right_obstacle == obstacles.NONE:# If both sides are completly clear
        return penguiner(world, x, y)
    
    if left_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE]:
        return actions.LEFT
    elif right_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE]:
        return actions.RIGHT
    else:
        return actions.NONE


def find_penguin_route(world, x, y):
    """
    Scan the upcoming positions to locate penguins and prioritize driving towards them,
    but also consider obstacles.
    """
    # Scan up to 5 positions ahead to find the nearest penguin or obstacles
    for i in range(1, 6):
        try:
            left_obstacle = world.get((x - 1, y - i))
            if left_obstacle == obstacles.PENGUIN:
                if not any(world.get((x - 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.LEFT  # Move left if there's a penguin ahead with no blocking obstacles
        except IndexError:
            continue

        try:
            right_obstacle = world.get((x + 1, y - i))
            if right_obstacle == obstacles.PENGUIN:
                if not any(world.get((x + 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.RIGHT  # Move right if there's a penguin ahead with no blocking obstacles
        except IndexError:
            continue

    return actions.NONE  # Default to moving forward if no penguins are found


def drive(world):
    x = world.car.x
    y = world.car.y

    # Move to the next position
    next_position = (x, y - 1)
    
    try:
        obstacle = world.get(next_position)
    except IndexError:
        # If the next position is out of the track, do nothing
        return actions.NONE

    if obstacle == obstacles.NONE:
        return find_penguin_route(world, x, y)
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP  # Pick up the penguin and move forward
    elif obstacle in avoidable_obstacles:
        return avoid(obstacle)# Avoid the obstacle based on it's type
    elif obstacle in (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER):
        return safe_zone(world, x, y - 1)  # Check for a safe zone to turn
    else:
        return actions.NONE  # Default action if obstacle is unknown
