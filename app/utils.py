SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'

# returns our snake from list of snakes
def find_my_snake(snakes):
    for s in snakes:
        if s.id == SNAKE_ID:
            return s

def is_wall(coor, walls):
    """
    returns true/false if coor is a wall
    """
    return coor in walls

def closest_food(current_position, food_positions):
    """
    Given the current position, returns the closest food position
    """
    return food_positions[0]

# boolean result if a specified cell is a snake body
def is_snake(coord, snakes):
    for s in snakes:
        for body in s.coords:
            if coord == body:
                return True
    return False
