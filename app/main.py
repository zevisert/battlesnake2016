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
        'taunt': '*taunt*'
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
    foods = data.get('food', [])
    golds = data.get('gold', [])

    # TODO: Do things with data
    snake = utils.find_my_snake(snakes)
    snake_head = utils.get_snake_head(snake)

    # possible_pos = possible_positions(walls=walls, snakes=snakes, head=snake_head)

    # print(possible_pos)
    size = (data.get('width'), data.get('height'))
    destination = get_destination(snakes, walls, foods, golds)
    direction = get_next_position(size, destination, snakes, walls)
    # game.games[game_name].set_last_direction(direction)

    return {
        'move': direction,
        'taunt': utils.get_taunt()
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    gaming = False

    return {
        'taunt': 'we probably won'
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

    close_gold = utils.closest_gold(my_snake, golds)
    if close_gold:
        # print "going for gold at {}".format(close_gold)
        return close_gold
    else:
        if utils.need_food(snakes):
            close_food = utils.closest_food(my_snake, foods)
            # print "going for food at {}".format(close_food)
            return close_food
        else:
            attack_head = utils.get_attack_head(snakes)
            if attack_head:
                # print "going for enenmy at {}".format(attack_head)
                return attack_head
    return None


def get_next_position(size, destination, snakes, walls):
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
    directions_to_move = []
    if destination is not None:
        directions_to_move = utils.direction_to_move(head, destination)

    directions = {}
    directions[EAST] = [head[0] + 1, head[1]]
    directions[WEST] = [head[0] - 1, head[1]]
    directions[NORTH] = [head[0], head[1] - 1]
    directions[SOUTH] = [head[0], head[1] + 1]

    # remove last direction from positions and place at front of list
    # if last_direction in positions:
    #     positions.remove(last_direction)
    #     positions = [last_direction] + positions

    # remove destination from positions and place at front of list
    if destination and len(directions_to_move) > 0:
        for dir in directions_to_move:
            if dir in positions:
                positions.remove(dir)
        positions = directions_to_move + positions
    print positions

    # loop through positions and move where we can
    for p in positions:
        new_coord = directions[p]
        if utils.is_valid(size, new_coord, snakes, walls):
            # print "{} is a valid direction to move".format(p)
            return p
    return positions[0]


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
