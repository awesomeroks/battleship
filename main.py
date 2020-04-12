'''
ship sprites from: https://www.vecteezy.com/free-vector/frigate - Frigate Vectors by Vecteezy

'''

import pygame
import random
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
    9: pygame.color.Color("red"),
    8: pygame.color.Color(195, 253, 255),
    "text": pygame.color.Color("black"),
    "gridOverlay": pygame.color.Color(93, 153, 198),
    "bg": pygame.color.Color(195, 253, 255),
    0:pygame.color.Color(144,202,249),
    1:pygame.color.Color(195, 253, 255),
    5.0:pygame.color.Color(0, 253, 255),
    4.0:pygame.color.Color(0, 100, 255),
    3.0:pygame.color.Color(0, 0, 255),
    3.1:pygame.color.Color(0, 0, 0),
    2.0:pygame.color.Color(195, 0, 255),


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


userTurn = False
huntMode = False
probabilityMap = []
y = []
z = []
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
def destroyTarget():
    global prevc, prevr, huntMode, acquiredDirection, currentShipDirection, destroySteps, backTracking, availableDirections
    print("DESTROYING", (prevc, prevr), currentShipDirection)
    setAvailableDirections()
    destroySteps +=1
    if(currentShipDirection == "LEFT" and "LEFT" in availableDirections):
        prevc -= 1
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "RIGHT"
            prevc += destroySteps + 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return
            backTracking = True
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            huntMode = False
            acquiredDirection = False
    elif(currentShipDirection == "RIGHT" and "RIGHT" in availableDirections):
        prevc += 1
        if(computerGrid[prevc][prevr] == 0):
            computerGrid[prevc][prevr] = 8
            currentShipDirection = "LEFT"
            prevc -= destroySteps + 1
            destroySteps = 0
            if(backTracking):
                huntMode = False
                acquiredDirection = False
                currentShipDirection = "NONE"
                return
            backTracking = True
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            huntMode = False
            acquiredDirection = False
    elif(currentShipDirection == "UP" and "UP" in availableDirections):
        prevr -= 1
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
            backTracking = True
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            acquiredDirection = False
            huntMode = False

    elif(currentShipDirection == "DOWN" and "DOWN" in availableDirections):
        prevr += 1
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
            backTracking = True
            print("BACKTRACKING")
        elif(computerGrid[prevc][prevr] != 8):
            computerGrid[prevc][prevr] = 9
            acquiredDirection = False
            huntMode = False
    else:
        acquiredDirection = False
        destroySteps = 0
        huntMode = False


def setAvailableDirections():
    global availableDirections
    availableDirections = {"UP", "DOWN", "LEFT", "RIGHT"}
    print("Dir: ", currentShipDirection)
    print("NOT Possible:", end ="")
    if(prevc == 0 or computerGrid[prevc-1][prevr] in [8,9]): #previously hit or if at unmovable location
        print("LEFT, ", end ="")
        availableDirections.remove("LEFT")
    elif(prevc == 9 or computerGrid[prevc+1][prevr] in [8,9]):
        print("RIGHT, ", end ="")
        availableDirections.remove("RIGHT")
    if(prevr == 0 or computerGrid[prevc][prevr-1] in [8,9]):
        print("UP, ", end ="")
        availableDirections.remove("UP")
    elif(prevr ==9  or computerGrid[prevc][prevr+1] in [8,9]):
        print("DOWN ")
        availableDirections.remove("DOWN")
    print()
    print("AVAILABLE DIRECTIONS:", availableDirections)
    if(availableDirections == set()):
        huntMode = False
        acquiredDirection = False



def huntTarget():
    global prevc, prevr, huntDirection, acquiredDirection, currentShipDirection, availableDirections
    if(acquiredDirection == True):
        destroyTarget()
        return
    setAvailableDirections()
    if(availableDirections == set()):
        return
    randomDirection = random.choice(list(availableDirections))
    print("CHECKING: " + randomDirection)
    if(randomDirection == "LEFT"):
        prevc -= 1
        print("HIT ATTEMPT AT ", (prevc, prevr))
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
    coin = random.randint(0,1)
    for i in ships:
        coin = random.randint(0,1)
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
                        for k in range(c,c + int(i.shipType)):
                            userGrid[k][r] = i.shipType
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
                        for k in range(r,r + int(i.shipType)):
                            userGrid[c][k] = i.shipType

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
        else:
            print("GAME OVER - You win")
        closePygame()

class Ship(pygame.sprite.Sprite):
    def __init__(self, shipType, startpos,shipName):
        super().__init__()
        self.selected = False
        self.shipType = shipType
        self.rotated = False
        self.image = pygame.image.load("sprites/normal/" + shipName + ".png")
        self.rect = pygame.Rect(startpos[0], startpos[1], int(cellWidth*shipType), cellWidth)
        self.rotatedimage = pygame.image.load("sprites/rotated/" + shipName + ".png")
        self.rotatedrect = pygame.Rect(startpos[0], startpos[1],  cellWidth,int(cellWidth*shipType))
        self.height = cellWidth
        self.width = int(cellWidth*shipType)
        self.column = - 1
        self.row = -1
        self.set = False


    def updatePos(self,pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], int(cellWidth*self.shipType), cellWidth)
        self.rotatedrect = pygame.Rect(pos[0], pos[1], cellWidth, int(cellWidth*self.shipType))
    def checkHover(self):
        pass
        # if(self.rect.collidepoint(pygame.mouse.get_pos())):
        #     # print("HOVERING ON " + str(self.shipType))
        #     print("")
    def checkMouseDown(self, pos):
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
                computerGrid[i][self.row] = self.shipType
                print((i, self.row), end = " ")
            print(' ')
        else:
            for i in range(self.row,self.row + int(self.shipType)):
                computerGrid[self.column][i] = self.shipType
                print((self.column, i), end = " ")
            print(' ')
        gameStart = True
    def draw(self):
        self.checkHover()
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

battleShip = Ship(shipNames['BATTLESHIP'], (leftMargin  ,boardHeight +topMargin + 15), "battleship")
carrier = Ship(shipNames['CARRIER'], (leftMargin +150  ,boardHeight +topMargin + 15), "carrier")
patrolShip = Ship(shipNames['PATROL'], (leftMargin + 350 ,boardHeight  +topMargin+ 15), "patrol")
destroyer = Ship(shipNames['DESTROYER'], (leftMargin  +450  ,boardHeight +topMargin + 15), "destroyer")
submarine = Ship(shipNames['SUBMARINE'], (leftMargin   + 600,boardHeight +topMargin + 15), "submarine")
ships = [battleShip, carrier, patrolShip, destroyer, submarine]
def initPygame():
    global screen, font, displayHeight, displayWidth
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Montserrat", 14)

    displayWidth = 2 * (cellWidth + cellMargin) * \
        boardDimension + 2*(rightMargin + leftMargin)
    displayHeight = 1 * (cellWidth + cellMargin) * \
        boardDimension + topMargin + bottomMargin
    screen = pygame.display.set_mode(
        [displayWidth, displayHeight])
    screen.fill(colours['bg'])
    pygame.display.set_caption("BATTLESHIP: Battle of the Legends")


def get_input():
    global gameStart, userTurn
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()
            for i in ships:
                i.checkMouseDown((x,y))
            if(x < boardWidth + leftMargin  and x > leftMargin and y<boardHeight + topMargin and y>topMargin):
                x = x - leftMargin
                y = y - topMargin
                selectedColumn = x // (cellMargin + cellWidth)
                selectedRow = y //(cellMargin + cellWidth)
                if(userGrid[selectedColumn][selectedRow] not in [0,8,9]):
                    userGrid[selectedColumn][selectedRow] = 9 #hit
                    userTurn = False
                elif(userGrid[selectedColumn][selectedRow] == 0):
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
            if event.key == pygame.K_CAPSLOCK:
                print("READY")
                gameStart = True
                for i in ships:
                    i.finishSetup()
            else:
                print("ROTATE SHIP")
                for i in ships:
                    if(i.selected == True):
                        i.rotated = not i.rotated
        elif event.type == pygame.QUIT:
            closePygame()
    return None, None

def flipScreen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)
def drawBoard():

    pygame.draw.rect(screen, colours["gridOverlay"], pygame.Rect(
                (leftMargin-borderWidth  ,topMargin-borderWidth ), (boardWidth +2*borderWidth - cellMargin, 2*borderWidth+ boardWidth  - cellMargin)))
    pygame.draw.rect(screen, colours["gridOverlay"], pygame.Rect(
                (-borderWidth +boardWidth + 2*leftMargin  ,topMargin-borderWidth ), (boardWidth +2*borderWidth  - cellMargin, 2*borderWidth+ boardWidth - cellMargin)))
    for i in range(len(userGrid)):
        for j in range(len(userGrid[0])):
            pygame.draw.rect(screen, colours[userGrid[i][j]], pygame.Rect(
                (leftMargin + i*(cellWidth + cellMargin) , topMargin + j * (cellWidth+ cellMargin)), (cellWidth, cellWidth)))
    for i in range(len(computerGrid)):
        for j in range(len(computerGrid[0])):
            pygame.draw.rect(screen, colours[computerGrid[i][j]], pygame.Rect(
                (2*leftMargin + i*(cellWidth + cellMargin) + boardWidth , topMargin + j * (cellWidth+ cellMargin)), (cellWidth, cellWidth)))
def drawText():
    label = font.render("Your Attacks", True, colours["text"])
    screen.blit(label,(int(leftMargin + ( boardDimension/2)*(cellMargin + cellWidth) - label.get_width()/2), 15))
    label = font.render("Your Ships", True, colours["text"])
    screen.blit(label,(int(boardWidth+2*leftMargin + ( boardDimension/2)*(cellMargin + cellWidth) - label.get_width()/2), 15))



def draw():
    screen.fill(colours['bg'])
    drawBoard()
    drawText()
    for i in ships:
        i.draw()

    flipScreen()

def closePygame():
    pygame.display.quit()
    pygame.quit()

    exit(0)


def gameLoop():
    placeComputerShips()
    while True:
        draw()
        get_input()


if __name__ == "__main__":
    initPygame()
    gameLoop()
    closePygame()
