SNAKE_ID = 'ae68ef2a-2fc7-47a0-8b6b-cc7ae5b80d66'

# returns our snake from list of snakes
def find_my_snake(snakes):
    for s in snakes:
        if s.id == SNAKE_ID:
            return s
