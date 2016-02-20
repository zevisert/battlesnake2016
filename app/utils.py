SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'

# returns our snake from list of snakes
def find_my_snake(snakes):
    for s in snakes:
        if s.id == SNAKE_ID:
            return s

<<<<<<< HEAD
# returns true/false if coor is a wall
def is_wall(coor, walls):
    return coor in walls
=======
def closest_food(current_position, food_positions):
    """
    Given the current position, returns the closest food position
    """
    return food_positions[0]
>>>>>>> origin/master
