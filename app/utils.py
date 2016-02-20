from math import sqrt
from random import randint

import game

SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'
FOOD_THRESH = 30
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'

def get_taunt():
    """
    Randomly select a taunt from the list
    """
    taunts = [
        "AAA",
        "BBB",
        "CCC",
        "DDD"
    ]
    return taunts[randint(0, len(taunts) - 1)]


def find_my_snake(snakes):
    """
    Returns our snake from the snakes on the board
    """
    for s in snakes:
        if s.get('id') == SNAKE_ID:
            return s

def get_snake_head(snake):
    """
    Returns position of snake head
    """
    return snake.get('coords')[0]

def is_wall(coord, walls):
    """
    returns true/false if coord is a wall
    """
    return coord in walls

def distance(coord1, coord2):
    """
    Returns euclidian distance from coord to coord
    """
    x_square = (coord1[0] - coord2[0])**2
    y_square = (coord1[1] - coord2[1])**2
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
        for body in s.get('coords'):
            if coord == body:
                return True
    return False

def is_valid(game_name, coord, snakes, walls):
    """
    Returns true/false if coord is a valid position to move to
    """
    width, height = game.games[game_name].get_board_size()
    x = coord[0]
    y = coord[1]

    if x >= 0 and x < width and y >= 0 and y < height:
        if not is_snake(coord, snakes) and not is_wall(coord, walls):
            return True
    return False

def is_snake_head(coord, snakes):
    """
    Given a specific coordinate,
    return if that cell is occupied by a snake's head
    """
    for s in snakes:
        if s.get('coords')[0] == coord:
            return True
    return False

def get_snake_length(snake):
    """
    Given snake
    retuns snake length
    """
    return len(snake.get("coords"))

def average_snake_length(snakes):
    """
    Given snakes
    reutrns average snake length
    """
    length_sum = 0
    count = 0
    for s in snakes:
        if s is not find_my_snake(snakes):
            length_sum += get_snake_length(s)
            count += 1
    return int(length_sum / count)

def need_food(snakes):
    """
    Given snakes
    return if we should get food or not
    """
    my_snake = find_my_snake(snakes)
    my_snake_length = get_snake_length(my_snake)
    if my_snake.get("health") < FOOD_THRESH or my_snake_length < average_snake_length(snakes):
        return True
    return False


def direction_to_move(my_coord, destination):
    x_dist = my_coord[0]-destination[0]
    y_dist = my_coord[1]-destination[1]

    abs_x = abs(x_dist)
    abs_y = abs(y_dist)

    if abs_x > abs_y:
        return WEST if x_dist > 0 else EAST
    else:
        return NORTH if y_dist > 0 else SOUTH
