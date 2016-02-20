import os

import bottle

import utils
import game

NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#F95759',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_name = data.get('game')
    mode = data.get('mode')
    height = data.get('height')
    width = data.get('width')
    current_game = game.Game(game_name=game_name, width=width, height=height, mode=mode)
    game.games[game_name] = current_game
    print game.games

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    """
    Find the game we're playing and calculate the move to make
    """
    data = bottle.request.json
    game_name = data.get('game')

    walls = data.get('walls', [])
    snakes = data.get('snakes', [])
    foods = data.get('foods', [])
    golds = data.get('golds', [])

    # TODO: Do things with data
    snake = utils.find_my_snake(snakes)
    snake_head = utils.get_snake_head(snake)
    
    # possible_pos = possible_positions(walls=walls, snakes=snakes, head=snake_head)

    # print(possible_pos)

    destination = get_destination(snakes, walls, foods, golds)
    direction = get_next_position(game_name, destination, snakes, walls, game.games[game_name].get_last_direction())
    game.games[game_name].set_last_direction(direction)

    return {
        'move': direction,
        'taunt': utils.get_taunt()
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    gaming = False
    game.games.pop(data.get('game'))

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))


def get_destination(snakes, walls, foods, golds):
    """
    Calculates the next direction the snake should go given data
    """
    my_snake = utils.find_my_snake(snakes)
    if utils.need_food(snakes):
        close_food = utils.closest_food(my_snake, foods)
        return close_food
    return None


def get_next_position(game_name, destination, snakes, walls, last_direction):
    """
    Given a destination coordinate, and all snakes and walls on board
    Find the direction (north, east, west, south) to move
    Prioritizes moving in the same direction as last
    Will not move into wall or off board
    """
    positions = [NORTH, EAST, SOUTH, WEST]

    my_snake = utils.find_my_snake(snakes)
    head = utils.get_snake_head(my_snake)

    # Find what direction we want to move in
    direction_to_move = None
    if destination is not None:
        direction_to_move = utils.direction_to_move(head, destination)

    directions = {}
    directions[EAST] = [head[0] + 1, head[1]]
    directions[WEST] = [head[0] - 1, head[1]]
    directions[NORTH] = [head[0], head[1] + 1]
    directions[SOUTH] = [head[0], head[1] - 1]

    # remove last direction from positions and place at front of list
    if last_direction in positions:
        positions.remove(last_direction)
        positions = [last_direction] + positions

    # remove destination from positions and place at front of list
    if destination is not None and direction_to_move in positions:
        positions.remove(direction_to_move)
        positions = [direction_to_move] + positions

    # loop through positions and move where we can
    for p in positions:
        new_coord = directions[p]
        if utils.is_valid(game_name, new_coord, snakes, walls):
            return p
    return last_direction


# def possible_positions(walls, snakes, head):
#     """
#     Returns up to three directions
#     """
#     possibilities = []
#     directions = {}
#     directions[EAST] = [head[0] + 1, head[1]]
#     directions[WEST] = [head[0] - 1, head[1]]
#     directions[NORTH] = [head[0], head[1] - 1]
#     directions[SOUTH] = [head[0], head[1] + 1]

#     for direction, pos in directions.items():
#         if not utils.is_valid(pos, snakes, walls):
#             continue
#         possibilities.append(direction)
#     return possibilities
