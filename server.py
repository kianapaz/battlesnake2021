import os
import random
import json
import cherrypy
import heapq

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

def get_moves(possible_moves, head, second_body_part):
    if head['x'] < second_body_part['x']:
        if 'right' in possible_moves:
            possible_moves.remove('right')
    elif head['x'] > second_body_part['x']:
        if 'left' in possible_moves:
            possible_moves.remove('left')
    if head['y'] < second_body_part['y']:
        if 'up' in possible_moves:
            possible_moves.remove('up')
    elif head['y'] > second_body_part['y']:
        if 'down' in possible_moves:
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
    
        data = cherrypy.request.json

        # Choose a random direction to move in
        print(data)
        print(data['board']['snakes'])
        print('==================')

        
        my_snake = data['you']
        head = my_snake['head'] 
        tail = my_snake['body'][-1]
        health = my_snake['health']
        length = my_snake['length']
        food = data['board']['food']
        body = my_snake['body']

        gameboard = data['board']['height'], data['board']['width']

        second_body_part = my_snake['body'][1]
        possible_moves = ["up", "down", "left", "right"]
        print("POSSIBLE MOVES")
        print(possible_moves)

        # removing falling off the board
        if head['x'] == 0:
            print("deleted left")
            if 'left' in possible_moves:
                possible_moves.remove('left')
        elif head['x'] == 10:
            print("deleted right")
            if 'right' in possible_moves:
                possible_moves.remove('right')
        if head['y'] == 0:
            print("deleted down")
            if 'down' in possible_moves:
                possible_moves.remove('down')
        elif head['y'] == 10:
            print("deleted up")
            if 'up' in possible_moves:
                possible_moves.remove('up')

        #possible_moves = get_moves(possible_moves, head, second_body_part)
        #possible_moves = get_moves(possible_moves, head, tail)
        for parts in body:
            if parts['x'] == head['x']+1 or parts['x'] == head['x']-1 and parts['y'] == head['y']+1 or parts['y'] == head['y']-1:
                print("hello")
                print(parts)
                possible_moves = get_moves(possible_moves, head, parts)
            if parts['x'] == head
            #if parts['y'] == head['y']+1 or parts['y'] == head['y']-1:
            #    print("yikkk")
            #    possible_moves = get_moves(possible_moves, head, parts)
        
        if tail['x'] == head['x']+1 or tail['x'] == head['x']-1 and tail['y'] == head['y']+1 or tail['y'] == head['y']-1:
            print("ahhh")
            possible_moves = get_moves(possible_moves, head, tail)
        #if tail['y'] == head['y']+1 or tail['y'] == head['y']-1:
        #    print("ohhh")
        #    possible_moves = get_moves(possible_moves, head, tail)
        

        #possible_moves = get_moves(possible_moves, head, tail)
        print('AFTER DELETING')
        print(possible_moves)
        

        the_move = random.choice(possible_moves)
        print(gameboard)
        print(possible_moves)
        print(the_move)
        return {"move": the_move}
        '''
        height = data["board"]["height"]
        width = data["board"]["width"]

        badCoords = []

        for x in range(width):
            bad = (x, -1)
            badCoords.append(bad)
            bad = (x, height)
            badCoords.append(bad)

        for y in range(width):
            bad = (-1, y)
            badCoords.append(bad)
            bad = (width, y)
            badCoords.append(bad)

        for snake in data["board"]["snakes"]:
            for xycoord in snake["body"]:
                bad = (xycoord["x"], xycoord["y"])
                badCoords.append(bad)
                
        # get coordinates of our snake head
        myHead = data["you"]["body"][0]

        possibleMoves = []

        # left
        coord = (myHead["x"]-1, myHead["y"])
        if coord not in badCoords:
            possibleMoves.append("left")
        
        # right
        coord = (myHead["x"]+1, myHead["y"])
        if coord not in badCoords:
            possibleMoves.append("right")

        # up
        coord = (myHead["x"], myHead["y"]-1)
        if coord not in badCoords:
            possibleMoves.append("up")

        # down
        coord = (myHead["x"], myHead["y"]+1)
        if coord not in badCoords:
            possibleMoves.append("down")

        # final decision
        if len(possibleMoves) > 0:
            finalMove = random.choice(possibleMoves)
        else:
            # doesn't really matter
            finalMove = random.choice(["left", "right", "up", "down"])

        print("badCoords={}".format(badCoords))
        print("possibleMoves={}".format(possibleMoves))
        print("finalMove={}".format(finalMove))
        return {"move": finalMove}
        '''
        

    

    

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
