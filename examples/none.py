from rose.common import obstacles, actions

driver_name = "zegrem"

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
    
    if left_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE] and right_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE]:
        return find_penguin_route(world, x, y)
    
    if left_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE]:
        return actions.LEFT
    elif right_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER, obstacles.NONE]:
        return actions.RIGHT
    else:
        # If both sides are not clear, choose an action based on the obstacle
        return actions.RIGHT if right_obstacle != obstacles.BARRIER else actions.LEFT

def find_penguin_route(world, x, y):
    """
    Scan the upcoming positions to locate penguins and prioritize driving towards them,
    but also consider obstacles.
    """
    # Scan up to 5 positions ahead to find the nearest penguin or obstacles
    for i in range(1, 6):
        try:
            left_obstacle = world.get((x - 1, y - i))
            if left_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER]:
                if not any(world.get((x - 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.LEFT  # Move left if there's a penguin ahead with no blocking obstacles
        except IndexError:
            continue

        try:
            right_obstacle = world.get((x + 1, y - i))
            if right_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER]:
                if not any(world.get((x + 1, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.RIGHT  # Move right if there's a penguin ahead with no blocking obstacles
        except IndexError:
            continue

        try:
            forward_obstacle = world.get((x, y - i))
            if forward_obstacle in [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER]:
                if not any(world.get((x, y - j)) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER] for j in range(1, i)):
                    return actions.NONE  # Move forward if there's a penguin ahead with no blocking obstacles
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
        # Check if there is a penguin route if no immediate obstacle
        penguin_action = find_penguin_route(world, x, y)
        if penguin_action != actions.NONE:
            return penguin_action
        return actions.NONE  # No obstacle, continue moving forward
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP  # Pick up the penguin and move forward
    elif obstacle == obstacles.WATER:
        return actions.BRAKE  # Brake to avoid water
    elif obstacle == obstacles.CRACK:
        return actions.JUMP  # Jump over the crack
    elif obstacle in (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER):
        return safe_zone(world, x, y - 1)  # Check for a safe zone to turn
    else:
        return actions.NONE  # Default action if obstacle is unknown
