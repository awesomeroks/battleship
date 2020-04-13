'''
ship sprites from: https://www.vecteezy.com/free-vector/frigate - Frigate Vectors by Vecteezy

'''

import pygame
import random
import os
# import classes
x = []
userGrid = []
computerGrid = []

'''
5.0 - • Aircraft Carrier (size 5)
4.0 - • Battleship (size 4)
3.0 - • Submarine (size 3)
3.1 - • Destroyer (size 3)
2.0 - • Patrol boat (size 2)
0.0 - • Empty Tile
'''
shipNames = {
"CARRIER" : 5.0,
"BATTLESHIP" : 4.0,
"SUBMARINE" : 3.0,
"DESTROYER" : 3.1,
"PATROL" : 2.0,
}

colours = {
    "water": pygame.color.Color(144,202,249),
    "ship": pygame.color.Color("gray"),
    9: pygame.color.Color(120, 62, 0), #HIT
    8: pygame.color.Color(195, 253, 255), #miss
    "text": pygame.color.Color("black"),
    "gridOverlay": pygame.color.Color(93, 153, 198),
    "bg": pygame.color.Color(195, 253, 255),
    0:pygame.color.Color(144,202,249),
    1:pygame.color.Color(195, 253, 255),
    5.0:pygame.color.Color(93, 153, 198),
    4.0:pygame.color.Color(93, 153, 198),
    3.0:pygame.color.Color(93, 153, 198),
    3.1:pygame.color.Color(93, 153, 198),
    2.0:pygame.color.Color(93, 153, 198),


}


boardDimension = 10
cellWidth = 32
cellMargin = 3
topMargin = 50
leftMargin = 30
rightMargin = 15
bottomMargin = 60
borderWidth = 5

boardHeight =  boardDimension*(cellWidth + cellMargin)
boardWidth = boardDimension*(cellWidth + cellMargin)
font = None
screen = None
displayWidth = 0
displayHeight = 0

gameStart = False
pygame.mixer.init()
bgmusic = pygame.mixer.Sound('sounds/bgm.wav')
explosionMusic = pygame.mixer.Sound('sounds/gexpl.wav')


exp1 = pygame.image.load('sprites/exp1.png')
exp2 = pygame.image.load('sprites/exp2.png')
exp3 = pygame.image.load('sprites/exp3.png')
exp4 = pygame.image.load('sprites/exp4.png')
exp5 = pygame.image.load('sprites/exp5.png')
exp6 = pygame.image.load('sprites/exp6.png')


fire1 = pygame.image.load('sprites/fire1.png')
fire2 = pygame.image.load('sprites/fire2.png')
fire3 = pygame.image.load('sprites/fire3.png')
fire4 = pygame.image.load('sprites/fire4.png')
fire5 = pygame.image.load('sprites/fire5.png')
fires = [fire1, fire2, fire3, fire4, fire5]
rocket = pygame.image.load('sprites/rocket.png')
compRocket = pygame.image.load('sprites/comprocket.png')
explosion = [exp1,exp2,exp3,exp4,exp5]
pygame.mixer.Channel(0).play(bgmusic, -1)
userTurn = False
huntMode = False
probabilityMap = []
y = []
z = []
gothFont =  None
smallHeadFont = None
subtitleFont = None

for i in range(boardDimension):
    for j in range(boardDimension):
        x = x + [0]
        y = y + [0]
        z = z + [0]
    userGrid += [x]
    probabilityMap += [z]
    computerGrid += [y]
    x = []
    y = []
    z = []
def resetProbabilityMap():
    global probabilityMap
    z = [0]
    for i in range(boardDimension):
        for j in range(boardDimension):
            z = z + [0]
        probabilityMap += [z]
        z = []
    print("PROBABILITIES RESET: ", probabilityMap)

print("userGrid DIMENSIONS: " + str(len(userGrid)) + " x " + str(len(userGrid[-1])))

prevc = -1
prevr = -1
huntDirection =  {"UP", "DOWN", "LEFT", "RIGHT"}
availableDirections = set()
currentShipDirection = "NONE"
acquiredDirection = False
destroySteps = 0
backTracking = False
def animateExplosion(board, column, row): # board = 0 for left, 1 for right
    if(board == 1):
        r = compRocket
        endLocationx = int(leftMargin + boardWidth*board + (column+0.5)*(cellWidth + cellMargin))
        endLocationy = int(topMargin + (row +0.0 )*(cellWidth + cellMargin))
        distance = endLocationy - 40
        startLocationx = int(endLocationx - distance)
        startLocationy = endLocationy - distance
        for i in range(0,  distance,16):
            # pygame.time.Clock().tick(60)
            draw()
            screen.blit(r,( startLocationx + i, startLocationy + i))
            flipScreen(customTick = 60)
    else:
        r = rocket
        endLocationx = int(leftMargin + boardWidth*board + (column+0.0 )*(cellWidth + cellMargin))
        endLocationy = int(topMargin + (row +0.0 )*(cellWidth + cellMargin))
        distance = endLocationy - 40
        startLocationx = int(endLocationx + distance)
        startLocationy = endLocationy - distance
        for i in range(0,  distance,16):
            # pygame.time.Clock().tick(60)
            draw()
            screen.blit(r,( startLocationx - i, startLocationy + i))
            flipScreen(customTick = 60)
    draw()
    flipScreen()
    pygame.mixer.Channel(2).play(explosionMusic)
    for i in explosion:
            pygame.time.Clock().tick(12)
            pygame.display.update(screen.blit(i,(leftMargin  + (boardWidth + leftMargin)*board + column*(cellWidth + cellMargin),topMargin + row*(cellWidth + cellMargin))))
currentDestroyedNumber = 0
prevDestroyedNumber = 0
def getActiveShipNumber():
    global computerShips, prevDestroyedNumber, currentDestroyedNumber
    currentDestroyedNumber = 0
    for i in ships:
        if(i.destroyed == True):
            currentDestroyedNumber += 1
    print(currentDestroyedNumber, prevDestroyedNumber)
def chooseRandom():
    global acquiredDirection, huntMode, prevc, prevr
    huntMode = False
    acquiredDirection = False
    c = random.randint(0,boardDimension-1)
    r = random.randint(0,boardDimension-1)
    while(computerGrid[c][r] == 9 or computerGrid[c][r] == 8):
        c = random.randint(0,boardDimension-1)
        r = random.randint(0,boardDimension-1)
    animateExplosion(1, c, r)
    if(computerGrid[c][r] == 0):
        computerGrid[c][r] = 8
        huntMode = False
        acquiredDirection = False
    else:
        computerGrid[c][r] = 9
        prevc = c
        prevr = r
        print("HIT THE SUCKER AT", (c,r))
        huntMode = True
    userTurn = True

def destroyTarget():
    global prevc, prevr, huntMode, acquiredDirection, currentShipDirection, destroySteps, backTracking, availableDirections, prevDestroyedNumber, currentDestroyedNumber
    print("DESTROYING", (prevc, prevr), currentShipDirection)
    if(setAvailableDirections()):
        return
    prevDestroyedNumber = currentDestroyedNumber
    getActiveShipNumber()
    destroySteps +=1
    if(prevDestroyedNumber != currentDestroyedNumber):
        chooseRandom()
        huntMode = False
        acquiredDirection = False
        userTurn = True
        return
    if(currentShipDirection == "LEFT" and "LEFT" in availableDirections):
        prevc -= 1
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0 ):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "RIGHT"
            prevc += destroySteps + 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return
            if(computerGrid[prevc+1 %9][prevr] not in [8,9]):
                backTracking = True
            else:
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
    elif(currentShipDirection == "RIGHT" and "RIGHT" in availableDirections):
        prevc += 1
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0 ):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "LEFT"
            prevc -= destroySteps + 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return
            print(computerGrid[prevc-1 %9][prevr] , (prevc-1, prevr))
            if(computerGrid[prevc-1 %9][prevr] not in [8,9]):
                backTracking = True
            else:
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
    elif(currentShipDirection == "UP" and "UP" in availableDirections):
        prevr -= 1
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "DOWN"
            prevr += destroySteps+ 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return

            print(computerGrid[prevc][prevr+1 %9], (prevc, prevr+1))
            if(computerGrid[prevc][prevr+1 %9] not in [8,9] ):
                backTracking = True
            else:
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9

    elif(currentShipDirection == "DOWN" and "DOWN" in availableDirections):
        prevr += 1
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "UP"
            prevr -= destroySteps + 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return
            print(computerGrid[prevc][prevr-1 %9], (prevc, prevr-1))
            if(computerGrid[prevc][prevr-1 %9] not in [8,9]):
                backTracking = True
            else:
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
    else:
        acquiredDirection = False
        destroySteps = 0
        huntMode = False


def setAvailableDirections():
    global availableDirections, prevc, prevr
    availableDirections = {"UP", "DOWN", "LEFT", "RIGHT"}
    print("Dir: ", currentShipDirection)
    print("NOT Possible:", end ="")
    if(prevc == 0 or computerGrid[prevc-1][prevr] in [8,9]): #previously hit or if at unmovable location
        print("LEFT, ", end ="")
        availableDirections.remove("LEFT")
    if(prevc == 9 or computerGrid[prevc+1][prevr] in [8,9]):
        print("RIGHT, ", end ="")
        availableDirections.remove("RIGHT")
    if(prevr == 0 or computerGrid[prevc][prevr-1] in [8,9]):
        print("UP, ", end ="")
        availableDirections.remove("UP")
    if(prevr ==9  or computerGrid[prevc][prevr+1] in [8,9]):
        print("DOWN ")
        availableDirections.remove("DOWN")
    print()
    print("AVAILABLE DIRECTIONS:", availableDirections)
    if(availableDirections == set()):
        chooseRandom()
        return True
    return False



def huntTarget():
    global prevc, prevr, huntDirection, acquiredDirection, currentShipDirection, availableDirections
    if(acquiredDirection == True):
        destroyTarget()
        return
    if(setAvailableDirections()):
        return
    randomDirection = random.choice(list(availableDirections))
    print("CHECKING: " + randomDirection)
    if(randomDirection == "LEFT"):
        prevc -= 1
        print("HIT ATTEMPT AT ", (prevc, prevr))
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            prevc +=1
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            acquiredDirection = True
            print("HIT!")
            currentShipDirection = "LEFT"
    elif(randomDirection == "RIGHT"):
        prevc += 1
        print("HIT ATTEMPT AT ", (prevc, prevr))
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            prevc -= 1
        elif(computerGrid[prevc][prevr] != 8):
            print("HIT!")
            computerGrid[prevc][prevr] = 9
            acquiredDirection = True
            currentShipDirection = "RIGHT"
    elif(randomDirection == "UP"):
        prevr -= 1
        print("HIT ATTEMPT AT ", (prevc, prevr))
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            prevr +=1
        elif(computerGrid[prevc][prevr] != 8):
            print("HIT!")
            computerGrid[prevc][prevr] = 9
            acquiredDirection = True
            currentShipDirection = "UP"
    elif(randomDirection == "DOWN"):
        prevr += 1
        print("HIT ATTEMPT AT ", (prevc, prevr))
        animateExplosion(1, prevc, prevr)
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            prevr -= 1
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            print("HIT")
            currentShipDirection = "DOWN"
            acquiredDirection = True
    print("SHIP IS IN DIRECTION: ", currentShipDirection)


def computerAlgo():
    global userTurn, gameStart, huntMode, huntDirection, acquiredDirection, prevc, prevr

    if(userTurn == False and gameStart == True):
        if(huntMode == True):
            huntTarget()
            userTurn = True
            return
        else:
            huntMode = False
            acquiredDirection = False
            huntDirection = ["LEFT", "RIGHT", "UP", "DOWN"]
        c = random.randint(0,boardDimension-1)
        r = random.randint(0,boardDimension-1)
        while(computerGrid[c][r] == 9 or computerGrid[c][r] == 8):
            c = random.randint(0,boardDimension-1)
            r = random.randint(0,boardDimension-1)
        animateExplosion(1, c, r)
        if(computerGrid[c][r] == 0):
            computerGrid[c][r] = 8
        else:
            computerGrid[c][r] = 9
            prevc = c
            prevr = r
            print("HIT THE SUCKER AT", (c,r))
            huntMode = True
        userTurn = True


def placeComputerShips():
    # 0 - horizontal, 1 - vertical

    #battleship
    c = random.randint(0,boardDimension-1)
    r = random.randint(0,boardDimension-1)
    for i in computerShips:
        coin = random.randint(0,1) # orientation
        if(coin == 0):
            z = True
            while z:
                c = random.randint(0, boardDimension  - int(i.shipType))
                r = random.randint(0,boardDimension-1)
                for k in range(c,c + int(i.shipType) + 1):
                    if(k > boardDimension-1):
                        break
                    if(userGrid[k][r] != 0):
                        z = True
                        break
                    if(k == c+int(i.shipType)):
                        z = False
                        i.column = c
                        i.row = r
                        i.rotated = False
                        i.finishSetup()
        else:
            z = True
            while z:
                c = random.randint(0, boardDimension-1)
                r = random.randint(0,boardDimension  - int(i.shipType))
                for k in range(r,r + int(i.shipType) + 1):
                    if(k > boardDimension -1 ):
                        break
                    if(userGrid[c][k] != 0):
                        z = True
                        break
                    if(k == r+int(i.shipType)):
                        z = False
                        i.column = c
                        i.row = r
                        i.rotated = True
                        i.finishSetup()
                        print(i.cells)

def checkFinished():
    if(not gameStart):
        return
    end1 = True
    end = True
    for i in range(boardDimension):
        for j in range(boardDimension):
            if(userGrid[i][j] not in [0,9,8] ):
                end = False
            if(computerGrid[i][j] not in [0,9,8] ):
                end1 = False

    if(end == True or end1 == True):
        if(end1):
            print("GAME OVER - Computer wins")
            label = gothFont.render("You Lose!",  True, colours["text"],)
        else:
            print("GAME OVER - You win")
            label = gothFont.render("You Win!", True, colours["text"])
        while(True):
            screen.fill(colours['bg'])
            screen.blit(label,(int((displayWidth - label.get_width())/2),int(displayHeight/2 - label.get_height()/2)))
            flipScreen()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT or event.type == pygame.KEYDOWN):
                    closePygame()

class Ship(pygame.sprite.Sprite):
    def __init__(self, shipType, startpos,shipName, visible = True):
        super().__init__()
        self.selected = False
        self.shipType = shipType
        self.rotated = False
        self.image = pygame.image.load("sprites/normal/" + shipName + ".png")
        self.rect = pygame.Rect(startpos[0], startpos[1], int(cellWidth*shipType), cellWidth)
        self.rotatedimage = pygame.image.load("sprites/rotated/" + shipName + ".png")
        self.rotatedrect = pygame.Rect(startpos[0], startpos[1],  cellWidth,int(cellWidth*shipType))
        self.computerShip = not visible
        if(self.computerShip):
            self.image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
            self.rotatedimage.fill((255,255,255, 100), special_flags=pygame.BLEND_ADD)


        self.height = cellWidth
        self.width = int(cellWidth*shipType)
        self.cells = []
        self.destroyed = False
        self.column = -1
        self.row = -1
        self.set = False
        self.visible = visible

    def updatePos(self,pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], int(cellWidth*self.shipType), cellWidth)
        self.rotatedrect = pygame.Rect(pos[0], pos[1], cellWidth, int(cellWidth*self.shipType))
    def computerShipUpdatePos(self):
        pos = [leftMargin + (cellWidth + cellMargin)*self.column, topMargin + (cellWidth + cellMargin)*self.row]
        self.updatePos(pos)
    def checkDestroyed(self):
        if(self.computerShip):
            killed = 0
            for i in self.cells:
                if(userGrid[i[0]][i[1]] == 9):
                    killed += 1
            if(int(self.shipType) == killed):
                self.destroyed = True
                self.visible = True
        else:
            killed = 0
            for i in self.cells:
                if(computerGrid[i[0]][i[1]] == 9):
                    killed += 1
            if(int(self.shipType) == killed):
                self.destroyed = True
                self.visible = True

    def checkMouseDown(self, pos):
        if(not self.computerShip):
            if(self.rotated):
                if(self.rotatedrect.collidepoint(pos)):
                    pygame.mouse.set_visible(self.selected)
                    self.selected = not self.selected
            else:
                if(self.rect.collidepoint(pos)):
                    pygame.mouse.set_visible(self.selected)
                    self.selected = not self.selected
    def finishSetup(self):
        print("SHIP: ", self.shipType, " STARTS AT: ",(self.column, self.row), ". LOCATIONS:", end = "")
        if(not self.rotated):
            for i in range(self.column,self.column + int(self.shipType)):
                if(self.computerShip):
                    userGrid[i][self.row] = self.shipType
                else:
                    computerGrid[i][self.row] = self.shipType
                self.cells += [[i, self.row]]
                print((i, self.row), end = " ")
            print(' ')
        else:
            for i in range(self.row,self.row + int(self.shipType)):
                if(self.computerShip):
                    userGrid[self.column][i] = self.shipType
                else:
                    computerGrid[self.column][i] = self.shipType
                self.cells += [[self.column, i]]
                print((self.column, i), end = " ")
            print(' ')
        if(self.computerShip):
            self.computerShipUpdatePos()
        gameStart = True
    def draw(self):
        self.checkDestroyed()
        if(self.visible):
            if(self.row != -1 and self.column != -1):
                self.set = True
            if(self.selected == True):
                x, y = pygame.mouse.get_pos()
                if(x > boardWidth + leftMargin + leftMargin and x < boardWidth + boardWidth + 2* leftMargin and y> topMargin and y< topMargin + boardHeight ):
                    l = x - 2*leftMargin - boardWidth
                    m = y - topMargin
                    selectedColumn = l // (cellMargin + cellWidth)
                    selectedRow = m //(cellMargin + cellWidth)
                    print(self.shipType, "PLACED AT", (self.column, self.row))
                    if(selectedColumn + int(self.shipType) <= boardDimension and self.rotated == False):
                        x = selectedColumn *(cellMargin  + cellWidth) + boardWidth + 2*leftMargin
                        y = selectedRow*(cellMargin + cellWidth) + topMargin
                        self.row = selectedRow
                        self.column = selectedColumn
                        self.updatePos((x, y))
                    elif(selectedRow + int(self.shipType) <= boardDimension and self.rotated == True):
                        x = selectedColumn *(cellMargin  + cellWidth) + boardWidth + 2*leftMargin
                        y = selectedRow*(cellMargin + cellWidth) + topMargin
                        self.row = selectedRow
                        self.column = selectedColumn
                        self.updatePos((x, y))
                else:
                    self.updatePos((x, y))
                    self.column = -1
                    self.row = -1
            if(self.rotated):
                screen.blit(self.rotatedimage, self.rotatedrect)
            else:
                screen.blit(self.image, self.rect)

def initPygame():
    global screen, font, displayHeight, displayWidth, gothFont, smallHeadFont, subtitleFont
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("fonts/Montserrat-Regular.ttf", 14)
    gothFont =  pygame.font.Font("fonts/Montserrat-SemiBold.ttf", 40)
    smallHeadFont = pygame.font.Font("fonts/Montserrat-Regular.ttf", 17)
    subtitleFont = pygame.font.Font("fonts/Montserrat-SemiBold.ttf", 14)

    displayWidth = 2 * (cellWidth + cellMargin) * \
        boardDimension + 2*(rightMargin + leftMargin)
    displayHeight = 1 * (cellWidth + cellMargin) * \
        boardDimension + topMargin + bottomMargin
    screen = pygame.display.set_mode(
        [displayWidth, displayHeight])
    screen.fill(colours['bg'])
    pygame.display.set_caption("BATTLESHIP: Battle of the Legends")

def resetGrid():
    global computerGrid
    computerGrid = []
    x = []
    for i in range(boardDimension):
        for j in range(boardDimension):
            x = x + [0]
        computerGrid += [x]
def get_input():
    global gameStart, userTurn
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()
            for i in ships:
                i.checkMouseDown((x,y))
            if(x < boardWidth + leftMargin  and x > leftMargin and y<boardHeight + topMargin and y>topMargin):
                if(not gameStart):
                    return
                x = x - leftMargin
                y = y - topMargin
                selectedColumn = x // (cellMargin + cellWidth)
                selectedRow = y //(cellMargin + cellWidth)
                if(userGrid[selectedColumn][selectedRow] not in [0,8,9]):
                    animateExplosion(0, selectedColumn, selectedRow)
                    userGrid[selectedColumn][selectedRow] = 9 #hit
                    userTurn = False
                elif(userGrid[selectedColumn][selectedRow] == 0):
                    animateExplosion(0, selectedColumn, selectedRow)
                    userGrid[selectedColumn][selectedRow] = 8 #miss

                    userTurn = False
            elif (x>boardWidth + leftMargin + leftMargin and x < boardWidth + boardWidth  + 2* leftMargin and y>topMargin and y<boardHeight + topMargin):
                x = x - boardWidth
                y = y - topMargin
                selectedColumn = x // (cellMargin + cellWidth)
                selectedRow = y //(cellMargin + cellWidth)

                # computerGrid[selectedColumn][selectedRow] = 1
            checkFinished()
            computerAlgo()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                print("READY")
                for i in ships:
                    if(i.column == -1 or i.row == -1):
                        resetGrid()
                        return
                    i.finishSetup()
                gameStart = True
            else:
                print("ROTATE SHIP")
                for i in ships:
                    if(i.selected == True):
                        i.rotated = not i.rotated
        elif event.type == pygame.QUIT:
            closePygame()
    return None, None
battleShip = Ship(shipNames['BATTLESHIP'], (leftMargin  ,boardHeight +topMargin + 15), "battleship")
carrier = Ship(shipNames['CARRIER'], (leftMargin +150  ,boardHeight +topMargin + 15), "carrier")
patrolShip = Ship(shipNames['PATROL'], (leftMargin + 350 ,boardHeight  +topMargin+ 15), "patrol")
destroyer = Ship(shipNames['DESTROYER'], (leftMargin  +450  ,boardHeight +topMargin + 15), "destroyer")
submarine = Ship(shipNames['SUBMARINE'], (leftMargin   + 600,boardHeight +topMargin + 15), "submarine")
ships = [battleShip, carrier, patrolShip, destroyer, submarine]

computerBattleShip = Ship(shipNames['BATTLESHIP'], (-100, -100), "battleship", False)
computerCarrier = Ship(shipNames['CARRIER'], (-100, -100), "carrier", False)
computerPatrolShip = Ship(shipNames['PATROL'], (-100, -100), "patrol", False)
computerDestroyer = Ship(shipNames['DESTROYER'], (-100, -100), "destroyer", False)
computerSubmarine = Ship(shipNames['SUBMARINE'], (-100, -100), "submarine", False)
computerShips = [computerBattleShip, computerCarrier, computerPatrolShip, computerSubmarine, computerDestroyer]
def flipScreen(customTick = 60):
    pygame.display.flip()
    pygame.time.Clock().tick(customTick)
def drawBoard():

    pygame.draw.rect(screen, colours["gridOverlay"], pygame.Rect(
                (leftMargin-borderWidth  ,topMargin-borderWidth ), (boardWidth +2*borderWidth - cellMargin, 2*borderWidth+ boardWidth  - cellMargin)))
    pygame.draw.rect(screen, colours["gridOverlay"], pygame.Rect(
                (-borderWidth +boardWidth + 2*leftMargin  ,topMargin-borderWidth ), (boardWidth +2*borderWidth  - cellMargin, 2*borderWidth+ boardWidth - cellMargin)))
    for i in range(len(userGrid)):
        for j in range(len(userGrid[0])):
            if(userGrid[i][j] in [8,9,0]):
                pygame.draw.rect(screen, colours[userGrid[i][j]], pygame.Rect(
                    (leftMargin + i*(cellWidth + cellMargin) , topMargin + j * (cellWidth+ cellMargin)), (cellWidth, cellWidth)))
            else:
                pygame.draw.rect(screen, colours[0], pygame.Rect(
                    (leftMargin + i*(cellWidth + cellMargin) , topMargin + j * (cellWidth+ cellMargin)), (cellWidth, cellWidth)))
    for i in range(len(computerGrid)):
        for j in range(len(computerGrid[0])):
            pygame.draw.rect(screen, colours[computerGrid[i][j]], pygame.Rect(
                (2*leftMargin + i*(cellWidth + cellMargin) + boardWidth , topMargin + j * (cellWidth+ cellMargin)), (cellWidth, cellWidth)))
def drawText():
    label = subtitleFont.render("Your Attacks", True, colours["text"])
    screen.blit(label,(int(leftMargin + ( boardDimension/2)*(cellMargin + cellWidth) - label.get_width()/2), 15))
    label = subtitleFont.render("Your Ships", True, colours["text"])
    screen.blit(label,(int(boardWidth+2*leftMargin + ( boardDimension/2)*(cellMargin + cellWidth) - label.get_width()/2), 15))
fireval = 0
def drawFire():
    global fireval
    for i in range(len(userGrid)):
        for j in range(len(userGrid[0])):
            if(computerGrid[i][j] == 9):
                screen.blit(fires[fireval],( 2*leftMargin + boardWidth + (i )*(cellWidth + cellMargin), topMargin + j*(cellWidth +cellMargin)))
            if(userGrid[i][j] == 9):
                screen.blit(fires[fireval],( leftMargin  + (i )*(cellWidth + cellMargin), topMargin + j*(cellWidth +cellMargin)))
    fireval += 1
    fireval %= 5

def draw():
    screen.fill(colours['bg'])
    drawBoard()
    
    drawText()
    
    for i in ships:
        i.draw()
    for i in computerShips:
        i.draw()
    drawFire()
    # getActiveShipNumber()
    flipScreen()

def closePygame():
    pygame.display.quit()
    pygame.quit()

    exit(0)


def gameLoop():
    showInstructions()
    placeComputerShips()
    while True:
        draw()
        get_input()

def showInstructions():
    while True:
        screen.fill(colours["bg"])
        label = gothFont.render("Battleship", True, colours["text"], )
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(25)))
        
        label = smallHeadFont.render("Battle of the Legends", True, colours["text"], )
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(70)))
        label = subtitleFont.render("Instructions", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(130)))
        label = font.render("1) Place your ships on the grid by selecting and deselecting at your desired location (right side grid).", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(160)))
        label = font.render("2) Press any key to rotate your ship.", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(190)))
        label = font.render("3) Press F1 to start the game after setting up your ships.", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(220)))
        label = font.render("4) Start destroying the AI!", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width())/2),int(250)))
        label = font.render("Music Credits - Gameboy (Battleship)", True, colours["text"])
        screen.blit(label,(int((displayWidth - label.get_width() - 30)),int(430)))
        flipScreen()
        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                return
            elif(event.type == pygame.QUIT):
                closePygame()

if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    initPygame()
    gameLoop()
    closePygame()
