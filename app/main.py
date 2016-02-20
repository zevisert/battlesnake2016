import bottle
import os

import utils

gaming = False
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'

LAST_DIRECTION = 'NORTH'

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

    # TODO: Do things with data

    gaming = True

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    snake = utils.find_my_snake(data.snakes)
    snake_head = utils.get_snake_head(snake)
    possible_pos = possible_positions(walls=data.walls, snakes=data.snakes, head=snake[0])
    direction = get_next_direction(possible_pos)
    LAST_DIRECTION = direction

    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    gaming = False

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))


def get_next_direction(possible_pos):
    direction = LAST_DIRECTION
    if direction in possible_pos:
        return direction
    else:
        return SOUTH # change this


def possible_positions(walls, snakes, head):
    """
    Returns up to three directions
    """
    possibilities = []
    directions = {}
    directions[EAST] = [head[0]+1, head[1]]
    directions[WEST] = [head[0]-1, head[1]]
    directions[NORTH] = [head[0], head[1]+1]
    directions[SOUTH] = [head[0], head[1]-1]

    for direction, pos in directions.items():
        if utils.is_wall(pos, walls) or utils.is_snake(pos, snakes):
            continue
        possibilities.append(direction)
    return possibilities