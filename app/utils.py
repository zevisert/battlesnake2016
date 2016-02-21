from math import sqrt
from random import randint, choice

import game

SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'
FOOD_THRESH = 30
ATTACK_THRESH = 2
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'


def get_taunt():
    """
    Randomly select a taunt from the list
    """
    s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie",
               "This cool guy my gardener met yesterday", "Superman"]
    p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats",
               "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people",
               "Supermen"]
    s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on",
               "retards", "meows on", "flees from", "tries to automate", "explodes"]
    p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard",
               "meow on", "flee from", "try to automate", "explode"]
    infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.",
                   "to be able to make toast explode.", "to know more about archeology."]

    return str(choice(s_nouns) + choice(s_verbs) + choice(s_nouns).lower())


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
    x_square = (coord1[0] - coord2[0]) ** 2
    y_square = (coord1[1] - coord2[1]) ** 2
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


def get_attack_head(snakes):
    """
    Gives snakes
    returns coords of head of snake we can kill
    """
    my_snake = find_my_snake(snakes)
    my_length = get_snake_length(my_snake)
    my_head = get_snake_head(my_snake)
    min_distance = float("inf")
    attack_snake = None
    for s in snakes:
        if s is not my_snake:
            length = get_snake_length(s)
            if my_length > length + ATTACK_THRESH:
                enemy_head = get_snake_head(s)
                d = distance(my_head, enemy_head)
                if d < min_distance:
                    min_distance = d
                    attack_snake = enemy_head
    return attack_snake


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


def is_challenged(coord, snakes):
    x = coord[0]
    y = coord[1]
    surrounding_coords = [
        [x + 1, y],
        [x - 1, y],
        [x, y + 1],
        [x, y - 1]
    ]
    my_snake = find_my_snake(snakes)
    my_head = get_snake_head(my_snake)
    for snake in snakes:
        head = get_snake_head(snake)
        if head in surrounding_coords and not head == my_head and len(snake['coords']) >= len(my_snake['coords']):
            return True
    return False


def is_valid(size, coord, snakes, walls, safety_check=True):
    """
    Returns true/false if coord is a valid position to move to
    """
    x = coord[0]
    y = coord[1]
    width = size[0]
    height = size[0]

    if x >= 0 and x < width and y >= 0 and y < height:
        if not is_snake(coord, snakes) and not is_wall(coord, walls) and not is_challenged(coord, snakes):
            if not safety_check:
                return True
            else:
                return is_safe(size, coord, snakes, walls)

    return False


def is_safe(size, coord, snakes, walls):
    """
    Checks if the coord is safe to move to (i.e. not surrounded)
    """
    x = coord[0]
    y = coord[1]
    surrounding_coords = [
        [x + 1, y],
        [x - 1, y],
        [x, y + 1],
        [x, y - 1]
    ]
    invalid_count = 0
    for coord in surrounding_coords:
        if not is_valid(size, coord, snakes, walls, safety_check=False):
            invalid_count += 1

    return invalid_count != 4


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
    if my_snake.get("health") < FOOD_THRESH or my_snake_length < (average_snake_length(snakes) + 2):
        return True
    return False


def direction_to_move(my_coord, destination):
    x_dist = my_coord[0] - destination[0]
    y_dist = my_coord[1] - destination[1]

    abs_x = abs(x_dist)
    abs_y = abs(y_dist)

    directions = []

    if abs_x > abs_y:
        directions = [WEST] if x_dist > 0 else [EAST]

        if y_dist > 0:
            directions.append(NORTH)
        else:
            directions.append(SOUTH)
    else:
        directions = [NORTH] if y_dist > 0 else [SOUTH]

        if x_dist > 0:
            directions.append(WEST)
        else:
            directions.append(EAST)

    return directions


def coord_in_safe_area(coord, walls, snakes, size):
    board = [[0 for j in range(0, size[0])] for i in range(0, size[1])]
    for wall in walls:
        board[wall[0]][wall[1]] = 1
    for snake in snakes:
        for snake_body in snake.get('coords'):
            board[snake_body[0]][snake_body[1]] = 1

    res = floodfill(board, coord[0], coord[1])
    area_to_dest = len(list(yeild_walls(res)))

    size_of_board = size[0] * size[1]
    for snake in snakes:
        for snake_body in snake.get('coords'):
            size_of_board -= 1

    for wall in walls:
        size_of_board -= 1

    if area_to_dest < size_of_board:
        print "Flood area is smaller than game board"



def floodfill(board_matrix, x, y):
    """
    #recursively invoke flood fill on all surrounding cells:
    """
    matrix = board_matrix
    if matrix[y][x] == 0:
        matrix[y][x] = -1

        if x > 0:
            matrix = floodfill(matrix, x - 1, y)
        if x < len(matrix[y]) - 1:
            matrix = floodfill(matrix, x + 1, y)
        if y > 0:
            matrix = floodfill(matrix, x, y - 1)
        if y < len(matrix) - 1:
            matrix = floodfill(matrix, x, y + 1)
    return matrix

def yeild_walls(matrix, value=-1):
    for row in matrix:
        for i in row:
            if i == value:
                yield i
