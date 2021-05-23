import os
import random

import cherrypy

width = 0
height = 0
snake_name = 'nake'
taunt_count = 0
last_circle_move = 'down'
head = []

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "kianapaz021",  # TODO: Your Battlesnake Username
            "color": "#556B2F",  # TODO: Personalize
            "head": "dead",  # TODO: Personalize
            "tail": "sharp",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)
        '''
        pacman_x, pacman_y = [ int(i) for i in raw_input().strip().split() ]
        food_x, food_y = [ int(i) for i in raw_input().strip().split() ]
        x,y = [ int(i) for i in raw_input().strip().split() ]
        
        grid = []
        for i in xrange(0, x):
            grid.append(list(raw_input().strip()))
        '''
        print(f"food {data['board']['food']}") 
        print(f"mroe food: {data['board']['food']}") 
        print("HELLLLOOOO")
        grid = [data['board']['height'], data['board']['width']]

        food = data['board']['food'][0]
        food_x, food_y = food.get('x'), food.get('y')

        pacman_x, pacman_y = data['you']['head'].get('x'), data['you']['head'].get('y')
        print(f"snake {data['you']['head']}")
        print(f"FOOD: {food_x}")
        print(grid)

        
        print(f"MOVE: {move}")
        #return {"move": move}

        print('WIDTH: ' + str(width))
        print('HEIGHT: ' + str(height))

        #data = bottle.request.json

        print(data)
        print(data['board']['snakes'])
        print('==================')

        snake_butts = []

        # get data for my snake, target snake
        #my_snake = next(x for x in data['board']['snakes'] if x.get('name') == snake_name)
        
        my_snake = data['you']

        head = my_snake.get('head') #'coords'][0]
        my_data = my_snake
        my_length = my_snake.get('length')  
        # hungry = len(my_snake['coords']) == 3 or (my_snake['health_points'] < 60)
        hungry = my_length == 3 or (my_snake.get('health') < 60)
        print('HUNGRY IS ' + str(hungry))
        print('HEALTHPOINTS ' + str(my_snake.get('health')) )

        final_countdown = False

        # find the snake_butts
        # if there are more than two snakes 
        if len(data['board']['snakes']) > 2 or len(my_snake.get('body')) > 15:
            # follow a snake
            for snake in data['board']['snakes']:
            # if snake isn't me
                if snake.get('name') != snake_name:
                    snake_butt, snake_head = find_snake_parts(snake)
                    # don't append if snake is adjacent and growing
                    if square_adjacent(snake_butt, head) and snake_butt == snake.get('body')[len(snake.get('body'))-2]:
                        print('WATCH OUT IT\'S GROWING!!!')
                    else:
                        print('we\'ve got a new butt')
                        snake_butts.append(snake_butt)
                else:
                    final_countdown = True


        food = data['board']['food']

        print('HEAD IS')
        print(head)
        safe_squares = find_safe_square(head, data)
        print('safe_squares', safe_squares)


        # if hungry or snake i'm following is growing, find food.
        if hungry or snake_butts == []:
            print('SNAKE BUTS IS ' + str(snake_butts))
            
            closest_food = find_closest(food, head)
            print('CLOSEST FOOD')
            print( closest_food)
            
            best_move = find_closest(safe_squares, closest_food)
        # otherwise follow a snake
        else:
            closest_butt = find_closest(snake_butts, head)
            print('snake_butts', snake_butts)
            print('closest', closest_butt)

            if square_adjacent(head, snake_butt) and snake_butt in snake_butts:
                safe_squares.append(snake_butt)

            best_move = find_closest(safe_squares, snake_butt)

        print('best_move', best_move
)
        # convert best move from coordinates into a string
        best_move = convert_coord_to_move(best_move, head)
        print('best move', best_move)

        return {"move": best_move}


    def square_adjacent(head, snake_butt):
        adj = False

        x = head[0]
        y = head[1]

        left = [x-1, y]
        right = [x+1, y]
        up = [x, y-1]
        down = [x, y+1]

        if snake_butt == left or snake_butt == right or snake_butt == up or snake_butt == down:
            adj = True

        return adj

    def find_closest(choices, coord):
        temp_closest = choices[0]
        temp_min_dist = pow(width,2)
        for c in choices:
            a = abs(c[1] - coord[1])
            b = abs(c[0] - coord[0])
            distance = math.sqrt( pow(a, 2) + pow(b, 2))
            if distance < temp_min_dist:
                temp_min_dist = distance
                temp_closest = c
        return temp_closest

    def adjacent_square_safe(point, data):
        x = point[0]
        y = point[1]

        left = [x-1, y]
        right = [x+1, y]
        up = [x, y-1]
        down = [x, y+1]

        directions = [left, right, up, down]

        safe_sq = True

        for direction in directions:
            if direction[0] < (width) and direction[0] >=0:
                if direction[1] < (height) and direction[1] >= 0:
                    if not square_empty(direction, data):
                        print('SQUARE NOT EMPTY!!')
                        safe_sq = False
        return safe_sq

    def find_safe_square(head, data):
        global width, height
        x = head[0]
        y = head[1]

        left = [x-1, y]
        right = [x+1, y]
        up = [x, y-1]
        down = [x, y+1]

        directions = [left, right, up, down]

        safe_sq = []

        for direction in directions:
            if direction[0] < (width) and direction[0] >= 0:
                if direction[1] < (height) and direction[1] >= 0:
                    if square_empty(direction, data):
                        safe_sq.append(direction)

        if safe_sq == []:
            print('No Safe Squares')
            print(adjacent)
        return safe_sq

    def find_snake_parts(snake):
        snake_butt = snake.get('body')[-1]
        snake_head = snake.get('body')[0]
        print('FINDING SNAKE PARTS: ' + str(snake_butt) + str(snake_head))
        return snake_butt, snake_head


    def convert_coord_to_move(best_move, head):
        x = head[0]
        y = head[1]

        left = [x-1, y]
        right = [x+1, y]
        up = [x, y-1]
        down = [x, y+1]

        if best_move == left:
            return 'left'
        elif best_move == right:
            return 'right'
        elif best_move == up:
            return 'up'
        elif best_move == down:
            return 'down'
        else:
            print('you fucked up')

    def square_empty(square, data):
        empty = True
        for snake in data['board']['snakes']:
            if square in snake.get('body'):
                empty = False
            return empty
        return empty

    def get_next_circle_move():
        global last_circle_move

        if last_circle_move == 'down':
            last_circle_move = 'left'
            return 'left'
        elif last_circle_move == 'left':
            last_circle_move = 'up'
            return 'up'
        elif last_circle_move == 'up':
            last_circle_move = 'right'
            return 'right'
        else:
            last_circle_move = 'down'
            return 'down'

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
