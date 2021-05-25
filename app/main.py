from AStar import *
import bottle
import copy
import math
import os


SNEK_BUFFER = 3
ID = 'gs_thdfHpJPSb34vQbRjqBSq8tb'
SNAKE = 1
WALL = 2
FOOD = 3
SAFTEY = 5


def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == -1:
        return 'up'
    elif dy == 1:
        return 'down'

def distance(p, q):
    dx = abs(p['x'] - q['x'])
    dy = abs(p['y'] - q['y'])
    return dx + dy;

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    return {
            "apiversion": "1",
            "author": "kianapaz021",  # TODO: Your Battlesnake Username
            "color": "#556B2F",  # TODO: Personalize
            "head": "dead",  # TODO: Personalize
            "tail": "sharp",  # TODO: Personalize
        }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    snek = data['you']
    grid =  data['board']['width'], data['board']['height']

    #foreach snake
    for enemy in data['board']['snakes']:
        if (enemy['id'] == ID):
            continue
        if distance(snek['body'][0], enemy['body'][0]) > SNEK_BUFFER:
            continue
        if (len(enemy['body']) > len(snek['body'])-1):
            #dodge
            if enemy['body'][0]['y'] < data['board']['height']-1:
                grid[enemy['body'][0]['x']][enemy['body'][0]['y']+1] = SAFTEY
            if enemy['body'][0]['y'] > 0:
                grid[enemy['body'][0]['x']][enemy['body'][0]['y']-1] = SAFTEY

            if enemy['body'][0]['x'] < data['board']['width']-1:
                grid[enemy['body'][0]['x']+1][enemy['body'][0]['y']] = SAFTEY
            if enemy['body'][0]['x'] > 0:
                grid[enemy['body'][0]['x']-1][enemy['body'][0]['y']] = SAFTEY


    snek_head = snek['body'][0]
    snek_body = snek['body']
    path = None
    middle = [data['board']['width'] / 2, data['board']['height'] / 2]
    foods = sorted(data['board']['food'], key = lambda p: distance(p,middle))
    
    for food in foods:
        #print food
        tentative_path = a_star(snek_head, food, grid, snek_body)
        if not tentative_path:
            #print "no path to food"
            continue

        path_length = len(tentative_path)
        snek_length = len(snek_body) + 1

        dead = False
        for enemy in data['snakes']:
            if enemy['id'] == ID:
                continue
            if path_length > distance(enemy['body'][0], food):
                dead = True
        if dead:
            continue

        # Update snek
        if path_length < snek_length:
            remainder = snek_length - path_length
            new_snek_body = list(reversed(tentative_path)) + snek_body[:remainder]
        else:
            new_snek_body = list(reversed(tentative_path))[:snek_length]

        if grid[new_snek_body[0]['x']][new_snek_body[0]['y']] == FOOD:
            # we ate food so we grow
            new_snek_body.append(new_snek_body[-1])

        # Create a new grid with the updates snek positions
        new_grid = copy.deepcopy(grid)

        for coord in snek_body:
            new_grid[coord[0]][coord[1]] = 0
        for coord in new_snek_body:
            new_grid[coord[0]][coord[1]] = SNAKE

        #printg(grid, 'orig')
        #printg(new_grid, 'new')

        #print snek['body'][-1]
        foodtotail = a_star(food,new_snek_body[-1],new_grid, new_snek_body)
        if foodtotail:
            path = tentative_path
            break
        #print "no path to tail from food"



    if not path:
        path = a_star(snek_head, snek['body'][-1], grid, snek_body)

    despair = not (path and len(path) > 1)

    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_body, [1,2,5]):
            path = a_star(snek_head, neighbour, grid, snek_body)
            #print 'i\'m scared'
            break

    despair = not (path and len(path) > 1)


    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_body, [1,2]):
            path = a_star(snek_head, neighbour, grid, snek_body)
            #print 'lik so scared'
            break

    if path:
        assert path[0] == tuple(snek_head)
        assert len(path) > 1

    return {
        'move': direction(path[0], path[1]),
        'taunt': 'TRAITOR!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
'''
import os
import random
import json
import cherrypy

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

        # removing falling off the board
        if head['x'] == 0:
            possible_moves.remove('left')
        elif head['x'] == 10:
            possible_moves.remove('right')
        if head['y'] == 0:
            possible_moves.remove('down')
        elif head['y'] == 10:
            possible_moves.remove('up')

        print("POSSIBLE MOVES after board info")
        print(possible_moves)

        possible_moves = get_moves(possible_moves, head, second_body_part)
        
        for body_part in body[1:]:
            
            if body_part['x'] == head['x']:
                print(f" the part:x==: {body_part} the head{head}")
                possible_moves = get_moves(possible_moves, head, body_part)
                print(possible_moves)

            elif body_part['y'] == head['y']:
                print(f" the part:y: {body_part} the head{head}")
                possible_moves = get_moves(possible_moves, head, body_part)
                print(possible_moves)
            
        the_move = random.choice(possible_moves)
        print(possible_moves)
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
'''