#---------------------------------------------------------------------------------------------------
#Authors    : Jason England & Tommy McClernon
#Date Due   : December 12th, 2022
#Description: This program takes will run a simplistic version of Pac-Man which was taken
#             from the "Freegames" library and will have our Informed best-first search algorithm
#             find the best path for Pac-man to take in order to get to its randomly selected
#             target pellet.
#    Freegames - https://grantjenks.com/docs/freegames/pacman.html
#---------------------------------------------------------------------------------------------------

#import section
import keyboard
from random import choice
import random
from turtle import *
from freegames import floor, vector

#Important Vars
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

moveForwardStack = []
backtrackList = []
lastTileVisted = []
globalTargetNode = 0

#Pac-man starting map
# fmt: off
# 20 x 20 Array
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
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


#This function will randomly select the index of a tile that still has a pellet and will return the index of that tile.
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


    
#This function will get and return the index of the tile that is adjacent to Pac-man in the UP direction.
def getMazeUP(locationIndex):
    if(locationIndex >= 20):
        locationIndex -= 20
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#This function will get and return the index of the tile that is adjacent to Pac-man in the DOWN direction.
def getMazeDOWN(locationIndex):
    if(locationIndex <= 379):
        locationIndex += 20
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#This function will get and return the index of the tile that is adjacent to Pac-man in the LEFT direction.
def getMazeLEFT(locationIndex):
    if(locationIndex %20 != 0 and locationIndex != 0):
        locationIndex -= 1
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#This function will get and return the index of the tile that is adjacent to Pac-man in the RIGHT direction.
def getMazeRIGHT(locationIndex):
    if(locationIndex % 20 != 19 and locationIndex!= 19):
        locationIndex += 1
        if tiles[locationIndex] != 0:
            return(locationIndex)
    return(-1)

#This function will calculate the hueristic (SLD) of each tile adjacent to Pac-man. The direction with the lowest heuristic will return a string saying the direction that Pac-man should go.
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
    print("Best choice value:", bestChoice)
    print("Best choice index:", directionsList.index(bestChoice))
    if(directionsList.index(bestChoice) == 0):
        return "UP"
    elif(directionsList.index(bestChoice) == 1):
        return "DOWN"
    elif(directionsList.index(bestChoice) == 2):
        return "LEFT"
    else:
        return "RIGHT"
    


#This function will get the adjacent tiles of Pac-man and put them onto the moveForward stack.
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


#This function will send out fake key signals when it is passed in a specific desired direction.
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


#Part of original code
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

#Part of original code
def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

#Part of original code
def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


#Part of original code
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


#Part of original code - main game loop that moves Pac-man and the ghosts.
def move():
    global lastTileVisted
    #Wipes the memory of Pac-man and gets a new target node after a certain length
    if(len(lastTileVisted) >= 120):
        lastTileVisted = []
        getRandomPosition()

    #DEBUG PRINT
    print("target node:", globalTargetNode)

    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()
    index = offset(pacman)
    lastTile = index
    lastTileVisted.append(lastTile)
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    #Gets the adjacent tiles
    getAdjacentTiles(index, lastTile)

    #This will check and see if we already hit the target node. If we have, then it will select another target node and it will clear Pac-man's recent tile memory.
    if globalTargetNode in lastTileVisted:
        getRandomPosition()
        lastTileVisted = []
        print("JUST GOT RAND POS")
        print("new target node:", globalTargetNode)
    

    #This will send the keyboard keys based on which direction was determined to be the best one for Pac-man to go.
    if(getBestDirection(globalTargetNode, index) == "UP"):
        fakeKeys("UP")
    elif(getBestDirection(globalTargetNode, index) == "DOWN"):
        fakeKeys("DOWN")
    elif(getBestDirection(globalTargetNode, index) == "LEFT"):
        fakeKeys("LEFT")
    else:
        fakeKeys("RIGHT")

    #Removes the pellet if Pac-man is on this tile.
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

    #ALSO GHOSTS
    # for point, course in ghosts:
    #     if abs(pacman - point) < 20:
    #         return

    #DEBUG PRINT
    print(lastTileVisted)

    #Loops the function every 50ms (20FPS)
    ontimer(move, 50)




#Part of original code
def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

#Setup and running the game
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
getRandomPosition() #Gets initial random position for pacman
print("target node:", globalTargetNode) #DEBUG PRINT
move()
done()
