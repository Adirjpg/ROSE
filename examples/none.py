"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA
def safe_zone(world):
    x = world.car.x
    y = world.car.y

    if(world.get(x - 1, y) == obstacles.NONE):
        return actions.LEFT
    elif(world.get(x + 1, y) == obstacles.NONE):
        return actions.RIGHT

driver_name = "Negev Driver"

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
        return actions.NONE  # No obstacle, continue moving forward
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP  # Pick up the penguin and move forward
    elif obstacle == obstacles.WATER:
        return actions.BRAKE  # Brake to avoid water
    elif obstacle == obstacles.CRACK:
        return actions.JUMP  # Jump over the crack
    elif obstacle == obstacles.TRASH or obstacle == obstacles.BARRIER or obstacle == obstacles.BIKE:
        return safe_zone(world)
    else:
        return actions.NONE  # Default action if obstacle is unknown

