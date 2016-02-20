games = {}

class Game(object):

    def __init__(self, game_name, width, height, mode='advanced'):
        self.game_name = game_name
        self.width = width
        self.height = height
        self.mode = mode
        self.last_direction = ''

    def get_last_direction(self):
        return self.last_direction

    def get_board_size(self):
        return self.width, self.height

    def set_last_direction(self, direction):
        self.direction = direction