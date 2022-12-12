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
import random
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
globalTargetNode = 0

def getRandomPosition():
    randIndex = random.randrange(len(tiles))
    loopBool = True
    while(loopBool):
        if(tiles[randIndex] == 1):
            loopBool = False
            global globalTargetNode
            globalTargetNode = randIndex
            return globalTargetNode
        else:
            loopBool = True
            if randIndex >= 399:
                randIndex = 0
            randIndex += 1


    

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

#TODO almost never goes right, not sure why but gotta fix this
def getBestDirection(targetTileIndex, currentTileIndex):
    absoluteValDiffUP = absoluteValDiffDOWN = absoluteValDiffLEFT = absoluteValDiffRIGHT = 999
    if (getMazeUP(currentTileIndex) != -1 and getMazeUP(currentTileIndex) not in lastTileVisted):
        absoluteValDiffUP = abs(targetTileIndex - getMazeUP(currentTileIndex))
    if (getMazeDOWN(currentTileIndex) != -1 and getMazeDOWN(currentTileIndex) not in lastTileVisted):
        absoluteValDiffDOWN = abs(targetTileIndex - getMazeDOWN(currentTileIndex))
    if (getMazeLEFT(currentTileIndex) != -1 and getMazeLEFT(currentTileIndex) not in lastTileVisted):
        absoluteValDiffLEFT = abs(targetTileIndex - getMazeLEFT(currentTileIndex))
    if (getMazeRIGHT(currentTileIndex) != -1 and getMazeRIGHT(currentTileIndex) not in lastTileVisted):
        absoluteValDiffRIGHT = abs(targetTileIndex - getMazeRIGHT(currentTileIndex))

    directionsList = [absoluteValDiffUP, absoluteValDiffDOWN, absoluteValDiffLEFT, absoluteValDiffRIGHT]
    print(directionsList)  
    bestChoice = min(directionsList)
    if(directionsList.index(bestChoice) == 0):
        return "UP"
    elif(directionsList.index(bestChoice) == 1):
        return "DOWN"
    elif(directionsList.index(bestChoice) == 2):
        return "LEFT"
    else:
        return "RIGHT"
    

# def getBestDirection(targetTileIndex, currentTileIndex, lastTileIndex):
#     absoluteValDiffUP = absoluteValDiffDOWN = absoluteValDiffLEFT = absoluteValDiffRIGHT = 999
#     foundUP = foundDOWN = foundLEFT = foundRIGHT = False
#     if(len(moveForwardStack) > 4):
#         for i in range(1,5):
#             i = i*-1
#             if(moveForwardStack[i] == getMazeUP(currentTileIndex)):
#                 foundUP = True
#                 break
#         for i in range(1,5):
#             i = i*-1
#             if(moveForwardStack[i] == getMazeDOWN(currentTileIndex)):
#                 foundDOWN = True
#                 break
#         for i in range(1,5):
#             i = i*-1
#             if(moveForwardStack[i] == getMazeLEFT(currentTileIndex)):
#                 foundLEFT = True
#                 break
#         for i in range(1,5):
#             i = i*-1
#             if(moveForwardStack[i] == getMazeRIGHT(currentTileIndex)):
#                 foundRIGHT = True
#                 break
#     if (not foundUP):
#         absoluteValDiffUP = abs(targetTileIndex - getMazeUP(currentTileIndex))
#     if (not foundDOWN):
#         absoluteValDiffDOWN = abs(targetTileIndex - getMazeDOWN(currentTileIndex))
#     if (not foundLEFT):
#         absoluteValDiffLEFT = abs(targetTileIndex - getMazeLEFT(currentTileIndex))
#     if (not foundRIGHT):
#         absoluteValDiffRIGHT = abs(targetTileIndex - getMazeRIGHT(currentTileIndex))

#     directionsList = [absoluteValDiffUP, absoluteValDiffDOWN, absoluteValDiffLEFT, absoluteValDiffRIGHT]
#     bestChoice = min(directionsList)
#     if(directionsList.index(bestChoice) == 0):
#         return "UP"
#     elif(directionsList.index(bestChoice) == 1):
#         return "DOWN"
#     elif(directionsList.index(bestChoice) == 2):
#         return "LEFT"
#     else:
#         return "RIGHT"


#pac man starts at index 268
def getAdjacentTiles(currentLocation, lastLocation):
    if(getMazeUP(currentLocation) != lastLocation and getMazeUP(currentLocation) != -1):
        if(len(moveForwardStack) > 4):
            foundUP = False
            for i in range(1,5):
                i = i*-1
                if(moveForwardStack[i] == getMazeUP(currentLocation)):
                    foundUP = True
                    break
            
            if(foundUP == False):
                moveForwardStack.append(getMazeUP(currentLocation))
                
                
                    





        elif(len(moveForwardStack) > 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeUP(currentLocation)):
            
                moveForwardStack.append(getMazeUP(currentLocation))
        elif(len(moveForwardStack) == 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeUP(currentLocation)):
            
                moveForwardStack.append(getMazeUP(currentLocation))
        else:
            moveForwardStack.append(currentLocation)
#############################################################################################
#LEFT
    if(getMazeLEFT(currentLocation) != lastLocation and getMazeLEFT(currentLocation) != -1):
        if(len(moveForwardStack) > 4):
            foundLEFT = False
            for i in range(1,5):
                i = i*-1
                if(moveForwardStack[i] == getMazeLEFT(currentLocation)):
                    foundLEFT = True
                    break
            
            if(foundLEFT == False):
                moveForwardStack.append(getMazeLEFT(currentLocation))
                
                
                    





        elif(len(moveForwardStack) > 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeLEFT(currentLocation)):
            
                moveForwardStack.append(getMazeLEFT(currentLocation))
        elif(len(moveForwardStack) == 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeLEFT(currentLocation)):
            
                moveForwardStack.append(getMazeLEFT(currentLocation))
        else:
            moveForwardStack.append(currentLocation)
##############################################################################################    
#RIGHT
    if(getMazeRIGHT(currentLocation) != lastLocation and getMazeRIGHT(currentLocation) != -1):
        if(len(moveForwardStack) > 4):
            foundRIGHT = False
            for i in range(1,5):
                i = i*-1
                if(moveForwardStack[i] == getMazeRIGHT(currentLocation)):
                    foundRIGHT = True
                    break
            
            if(foundRIGHT == False):
                moveForwardStack.append(getMazeRIGHT(currentLocation))
                
                
                    





        elif(len(moveForwardStack) > 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeRIGHT(currentLocation)):
            
                moveForwardStack.append(getMazeRIGHT(currentLocation))
        elif(len(moveForwardStack) == 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeRIGHT(currentLocation)):
            
                moveForwardStack.append(getMazeRIGHT(currentLocation))
        else:
            moveForwardStack.append(currentLocation)
 ##############################################################################################   
#DOWN
    if(getMazeDOWN(currentLocation) != lastLocation and getMazeDOWN(currentLocation) != -1):
        if(len(moveForwardStack) > 4):
            foundDOWN = False
            for i in range(1,5):
                i = i*-1
                if(moveForwardStack[i] == getMazeDOWN(currentLocation)):
                    foundDOWN = True
                    break
            
            if(foundDOWN == False):
                moveForwardStack.append(getMazeDOWN(currentLocation))
                
                
                    





        elif(len(moveForwardStack) > 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeDOWN(currentLocation)):
            
                moveForwardStack.append(getMazeDOWN(currentLocation))
        elif(len(moveForwardStack) == 1):
            if(moveForwardStack[len(moveForwardStack)-1] != getMazeDOWN(currentLocation)):
            
                moveForwardStack.append(getMazeDOWN(currentLocation))
        else:
            moveForwardStack.append(currentLocation)
    
#Send fake keys to system
def fakeKeys(directionSTR):
    #Move up section
    if(directionSTR == "UP"):
        keyboard.press_and_release('up')
    elif(directionSTR == "DOWN"):
        keyboard.press_and_release('down')
    elif(directionSTR == "LEFT"):
        keyboard.press_and_release('left')
    else:
        keyboard.press_and_release('right')



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
    global lastTileVisted
    if(len(lastTileVisted) >= 20):
        lastTileVisted = []

    print("new target node:", globalTargetNode)
    # print(moveForwardStack)
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
    if globalTargetNode in moveForwardStack:        #This sees if we already hit the target node and will select another if we need to.
        getRandomPosition()
        print("JUST GOT RAND POS")
        print("new target node:", globalTargetNode)
    
    match getBestDirection(globalTargetNode, index):
        case "UP":
            fakeKeys("UP")
        case "DOWN":
            fakeKeys("DOWN")
        case "LEFT":
            fakeKeys("LEFT")
        case "RIGHT":
            fakeKeys("RIGHT")

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    #GHOSTS- add this back when we want them
    # for point, course in ghosts:
    #     if valid(point + course):
    #         point.move(course)
    #     else:
    #         options = [
    #             vector(5, 0),
    #             vector(-5, 0),
    #             vector(0, 5),
    #             vector(0, -5),
    #         ]
    #         plan = choice(options)
    #         course.x = plan.x
    #         course.y = plan.y

    #     up()
    #     goto(point.x + 10, point.y + 10)
    #     dot(20, 'red')

    update()

    # for point, course in ghosts:
    #     if abs(pacman - point) < 20:
    #         return
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
getRandomPosition() #Gets initial random position for pacman
print("target node:", globalTargetNode)
move()
done()

#moves left by itself
#change(-5, 0)


    



