from math import sqrt

SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'
WIDTH = 0
HEIGHT = 0

# returns our snake from list of snakes
def find_my_snake(snakes):
    for s in snakes:
        if s.id == SNAKE_ID:
            return s

def get_snake_head(snake):
    """
    Returns position of snake head
    """
    return snake.coords[0]

def is_wall(coor, walls):
    """
    returns true/false if coor is a wall
    """
    return coor in walls

def distance(coor1, coor2):
    """
    Returns euclidian distance from coor1 to coor2
    """
    x_square = (coor1[0] - coor2[0])**2
    y_square = (coor1[1] - coor2[1])**2
    return sqrt(x_square + y_square)

def closest_gold(snake, golds):
    """
    Returns closest gold position to snake
    """
    head = get_snake_head(snake)
    min_gold = None
    min_distance = float("inf")
    for g in golds:
        d = distance(head, g)
        if d < min_distance:
            min_distance = d
            min_gold = g
    return min_gold

def closest_food(snake, foods):
    """
    Given the current position, returns the closest food position
    """
    head = get_snake_head(snake)
    min_food = None
    min_distance = float("inf")
    for f in foods:
        d = distance(head, f)
        if d < min_distance:
            min_distance = d
            min_food = f
    return min_food

def is_snake(coord, snakes):
    """
    Given a specific coordinate,
    return if that cell is occupied by a snake's body (head inclusive)
    """
    for s in snakes:
        for body in s.coords:
            if coord == body:
                return True
    return False

def is_snake_head(coord, snakes):
    """
    Given a specific coordinate,
    return if that cell is occupied by a snake's head
    """
    for s in snakes:
        if s.coords[0] == coord:
            return True
    return False
