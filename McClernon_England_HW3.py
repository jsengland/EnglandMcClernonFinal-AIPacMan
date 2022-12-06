"""Pacman, classic arcade game.
Exercises
1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""
import keyboard
from random import choice
from turtle import *

from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# fmt: off
# 20 x 20 Array
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on

moveForwardStack = []
backtrackList = []
lastTileVisted = []

def getMazeUP(locationIndex):
    if(locationIndex >= 20):
        locationIndex -= 20
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#TODO - get this correct
def getMazeDOWN(locationIndex):
    if(locationIndex <= 379):
        locationIndex += 20
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#TODO - get this correct
def getMazeLEFT(locationIndex):
    if(locationIndex %20 != 0 and locationIndex != 0):
        locationIndex -= 1
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#TODO - get this correct
def getMazeRIGHT(locationIndex):
    if(locationIndex % 20 != 19 and locationIndex!= 19):
        locationIndex -= 1
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

def getAdjacentTiles(currentLocation, lastLocation):
    if(getMazeUP(currentLocation) != lastLocation):
        moveForwardStack.append(getMazeUP(currentLocation))

    if(getMazeLEFT(currentLocation != lastLocation)):
        moveForwardStack.append(getMazeLEFT(currentLocation))

    if(getMazeRIGHT(currentLocation) != lastLocation):
        moveForwardStack.append(getMazeRIGHT(currentLocation))

    if(getMazeDOWN(currentLocation != lastLocation)):
        moveForwardStack.append(getMazeDOWN(currentLocation))

#Send fake keys to system
def fakeKeys():
    #Move up section
    keyboard.press_and_release('left')
    pass


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    #print("printing index",index)
    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

# #TODO validPACMAN our func
# def validPACMAN(point):
#     """Return True if point is valid in tiles."""
#     index = offset(point)

#     if tiles[index] == 0 or tiles[index] == 3:
#         return False

#     index = offset(point + 19)

#     if tiles[index] == 0 or tiles[index] == 3:
#         return False

#     return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')



def move():
    print(moveForwardStack)
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()
    index = offset(pacman)
    lastTile = index
    lastTileVisted.append(lastTile)
    #TODO limit append to one per tile 
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)
    #timer??, for loop?? look at length of stack
    getAdjacentTiles(index, lastTile)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return
    #fakeKeys()
    ontimer(move, 50)

# def moveGHOSTS():
#     """Move pacman and all ghosts."""
    

#     #clear()

    

#     for point, course in ghosts:
#         if valid(point + course):
#             point.move(course)
#         else:
#             options = [
#                 vector(5, 0),
#                 vector(-5, 0),
#                 vector(0, 5),
#                 vector(0, -5),
#             ]
#             plan = choice(options)
#             course.x = plan.x
#             course.y = plan.y

#         up()
#         goto(point.x + 10, point.y + 10)
#         dot(20, 'red')

#     #update()

#     # for point, course in ghosts:
#     #     if abs(pacman - point) < 20:
#     #         return

#     #ontimer(moveGHOSTS, 100)

#TODO - only pacman calls this, the ghosts don't
# def movePACMAN():
#     """Move pacman and all ghosts."""
#     writer.undo()
#     writer.write(state['score'])

#     clear()
    
#     #PACMAN MOVEMENT
#     if validPACMAN(pacman + aim):
#         pacman.move(aim)

#     index = offset(pacman)

#     if tiles[index] == 1:
#         tiles[index] = 2
#         state['score'] += 1
#         x = (index % 20) * 20 - 200
#         y = 180 - (index // 20) * 20
#         square(x, y)

#     up()
#     goto(pacman.x + 10, pacman.y + 10)
#     dot(20, 'yellow')

#     # for point, course in ghosts:
#     #     if valid(point + course):
#     #         point.move(course)
#     #     else:
#     #         options = [
#     #             vector(5, 0),
#     #             vector(-5, 0),
#     #             vector(0, 5),
#     #             vector(0, -5),
#     #         ]
#     #         plan = choice(options)
#     #         course.x = plan.x
#     #         course.y = plan.y

#     #     up()
#     #     goto(point.x + 10, point.y + 10)
#     #     dot(20, 'red')

#     moveGHOSTS()
#     update()

#     # #TODO - FINISH THIS, FIGURE OUT HOW TO SET TILE BACK TO 1 OR 2
#     # for point, course in ghosts:
#     #     index = offset(point)
#     #     tiles[index] = 3
#     #     if abs(pacman - point) < 20:
#     #         return

#     ontimer(movePACMAN, 50)

#TODO - changed valid in this func
def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
#move()
move()
done()

#moves left by itself
#change(-5, 0)


    



