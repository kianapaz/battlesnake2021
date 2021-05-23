import os
import random

import cherrypy


"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

def get_moves(possible_moves, head, second_body_part):
    if head.get('x') < second_body_part.get('x'):
        possible_moves.remove('right')
    elif head.get('x') > second_body_part.get('x'):
        possible_moves.remove('left')
    elif head.get('y') < second_body_part.get('y'):
        possible_moves.remove('up')
    elif head.get('y') > second_body_part.get('y'):
        possible_moves.remove('down')

    return possible_moves

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
        
        print(data)
        print(data['board']['snakes'])
        print('==================')

        
        my_snake = data['you']
        head = my_snake.get('head') 
        tail = my_snake.get('body')[-1]
        health = my_snake.get('health')
        length = my_snake.get('length')
        food = data['board']['food']

        gameboard = data['board'].get('height'), data['board'].get('width')

        second_body_part = my_snake.get('body')[1]
        

        possible_moves = get_moves(possible_moves, head, second_body_part)
        #possible_moves = get_moves(possible_moves, head, tail)
        
        # removing falling off the board
        if head.get('x') == 0:
            possible_moves.remove('left')
        elif head.get('x') == 10:
            possible_moves.remove('right')
        elif head.get('y') == 0:
            possible_moves.remove('down')
        elif head.get('y') == 10:
            possible_moves.remove('up')

        the_move = random.choice(possible_moves)
        print(gameboard)
        print(the_move)


        return {"move": the_move}

    

    

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
