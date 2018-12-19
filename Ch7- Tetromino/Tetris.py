import time, pygame, sys, random
from pygame.locals import *

FPS = 50
windowWidth = 780
windowHeight = 640
boxSize = 20
boardWidth = 10
boardHeight = 25
blank = "."

moveSideWaysFreq = 0.15
moveDownFreq = 0.1

xMargin = int((windowWidth - boardWidth * boxSize)/2)
topMargin = windowHeight - (boardHeight * boxSize) - 14

white = (255, 255, 255)
gray  = (185, 185, 185)
black = (0, 0, 0)
red = (104, 0, 0)
lightRed = (175, 20, 20)
green = (0, 145, 0)
lightGreen = (20, 175, 20)
blue = (0, 0, 145)
lightBlue = (20, 20, 175)
yellow = (155, 155, 0)
lightYellow = (175, 175, 20)
purple = (76, 0, 153)

borderColor = gray
bgColor = black
textColor = white
textShadowColor = gray
lightColors = (blue, green, red, yellow)
colors = (lightBlue, lightGreen, lightRed, lightYellow)
assert len(colors) == len(lightColors)

templateWidth = 5
templateHeight = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                    '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                     ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '...O.',
                      '.....'],
                     ['.....',
                      '..O..',
                      '..O..',
                      '.OO..',
                      '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

shapes = {"S": S_SHAPE_TEMPLATE,
          "Z": Z_SHAPE_TEMPLATE,
          "J": J_SHAPE_TEMPLATE,
          "L": L_SHAPE_TEMPLATE,
          "I": I_SHAPE_TEMPLATE,
          "O": O_SHAPE_TEMPLATE,
          "T": T_SHAPE_TEMPLATE
         }


def main():
    global fpsClock, displaysurf, basicFont, bigFont
    pygame.init()
    fpsClock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowWidth, windowHeight))
    basicFont = pygame.font.Font("freesansbold.ttf", 16)
    bigFont = pygame.font.Font("freesansbold.ttf", 50)
    pygame.display.set_caption("Tetromino: A Tetris Clone")

    showTextScreen("Tetrimono")
    while True:
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load("sound/tetrisb.mid")
        else:
            pygame.mixer.music.load("sound/tetrisc.mid")
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen("Game Over")


def runGame():

    # variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()

    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()

            if not isValidPosition(board, fallingPiece):
                return

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    # pause game
                    displaysurf.fill(bgColor)
                    pygame.mixer.music.stop()
                    showTextScreen("Paused")

                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                elif event.key == K_LEFT or event.key == K_a:
                    movingLeft = False
                elif event.key == K_RIGHT or event.key == K_d:
                    movingRight = False
                elif event.key == K_DOWN or event.key == K_s:
                    movingDown = False

            # Moving the block sideways
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX = -1):
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece["x"] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # Rotating the block only if there is room
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece["rotation"] = (fallingPiece["rotation"] + 1) % len(shapes[fallingPiece["shape"]])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece["rotation"] = (fallingPiece["rotation"] - 1) % len(shapes[fallingPiece["shape"]])

                # Rotate the other
                elif (event.key == K_q):
                    fallingPiece["rotation"] = (fallingPiece["rotation"] - 1) % len(shapes[fallingPiece["shape"]])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece["rotation"] = (fallingPiece["rotation"] + 1) % len(shapes[fallingPiece["shape"]])

                # increase speed that block is falling with down_key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True

                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece["y"] += 1
                    lastMoveDownTime = time.time()

                # Move current block all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, boardHeight):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece["y"] += i - 1

        # Handle moving the block because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > moveSideWaysFreq:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece["x"] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece["x"] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > moveDownFreq and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece["y"] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, place on board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, continue to move block down
                fallingPiece["y"] += 1
                lastFallTime = time.time()

        # Output on the screen
        displaysurf.fill(bgColor)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        fpsClock.tick(FPS)


def makeTextObjs(text, font, obj_color):
    surf = font.render(text, True, obj_color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # draw shadow
    titleSurf, titleRect = makeTextObjs(text, bigFont, red)
    titleRect.center = (int(windowWidth/2), int(windowHeight/2))
    displaysurf.blit(titleSurf, titleRect)

    # draw text
    titleSurf, titleRect = makeTextObjs(text, bigFont, textColor)
    titleRect.center = (int(windowWidth/2) - 3, int(windowHeight/2) - 3)

    displaysurf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs("Press a key to begin!", basicFont, textColor)
    pressKeyRect.center = (int(windowWidth / 2), int(windowHeight/2) + 100)
    displaysurf.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        fpsClock.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()

        pygame.event.post(event)


# return the level the player is on and how many seconds has passed until piece falls
def calculateLevelAndFallFreq(score):
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


# return random piece
def getNewPiece():
    shape = random.choice(list(shapes.keys()))
    newPiece = {"shape": shape,
                "rotation": random.randint(0, len(shapes[shape]) - 1),
                "x": int(boardWidth/2) - int(templateWidth/2),
                "y": -2,  # start at the top of the board
                "color": random.randint(0, len(colors) - 1) }
    return newPiece


# fill board based on piece's location, shape, and rotation
def addToBoard(board, piece):
    for x in range(templateWidth):
        for y in range(templateHeight):
            if shapes[piece["shape"]][piece["rotation"]][y][x] != blank:
                board[x + piece["x"]][y + piece["y"]] = piece["color"]


def getBlankBoard():
    board = []
    for i in range(boardWidth):
        board.append([blank] * boardHeight)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < boardWidth and y < boardHeight


def isValidPosition(board, piece, adjX=0, adjY=0):
    for x in range(templateWidth):
        for y in range(templateHeight):
            isAboveBoard = y + piece["y"] + adjY < 0
            if isAboveBoard or shapes[piece["shape"]][piece["rotation"]][y][x] == blank:
                continue
            if not isOnBoard(x + piece["x"] + adjX, y + piece["y"] + adjY):
                return False

            if board[x + piece["x"] + adjX][y + piece["y"] + adjY] != blank:
                return False

    return True


# Line is filled with no gaps
def isCompleteLine(board, y):
    for x in range(boardWidth):
        if board[x][y] == blank:
            return False

    return True


def removeCompleteLines(board):
    numLinesRemoved = 0
    y = boardHeight - 1 # start at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # remove line and pull down boxes
            for pullDownY in range(y, 0, -1):
                for x in range(boardWidth):
                    board[x][pullDownY] = board[x][pullDownY-1]

            # set very top line to blank
            for x in range(boardWidth):
                board[x][0] = blank
            numLinesRemoved += 1

        else:
            y -= 1 # Check next row above
    return numLinesRemoved


# convert coordinates of the board to coordinates of the lation on the screen
def convertToPixelCoords(box_x, box_y):
    return (xMargin + (box_x * boxSize)), (topMargin + (box_y * boxSize))


# draw single boxes to create the piece
def drawBox(box_x, box_y, color, pixelx=None, pixely=None):
    if color == blank:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(box_x, box_y)

    pygame.draw.rect(displaysurf, colors[color], (pixelx + 1, pixely + 1, boxSize - 4, boxSize - 4))


# draw border around board
def drawBoard(board):
    pygame.draw.rect(displaysurf, borderColor, (xMargin - 3, topMargin - 7, (boardWidth * boxSize) + 8, (boardHeight * boxSize) + 8), 5)

    # fill background
    pygame.draw.rect(displaysurf, bgColor, (xMargin, topMargin, boxSize * boardWidth, boxSize * boardHeight))

    # draw the individual boxes
    for x in range(boardWidth):
        for y in range(boardHeight):
            drawBox(x, y, board[x][y])


# Score and level indicator
def drawStatus(score, level):
    scoreSurf = basicFont.render("Score: %s" % score, True, textColor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windowWidth - 150, 20)
    displaysurf.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = basicFont.render("Level: %s" % level, True, textColor)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (windowWidth - 150, 50)
    displaysurf.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = shapes[piece["shape"]][piece["rotation"]]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece["x"], piece["y"])

    # draw each of the blocks that create the piece
    for x in range(templateWidth):
        for y in range(templateHeight):
            if shapeToDraw[y][x] != blank:
                drawBox(None, None, piece["color"], pixelx + (x * boxSize), pixely + (y * boxSize))


# draw the "next" text
def drawNextPiece(piece):
    nextSurf = basicFont.render("Next: ", True, textColor)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (windowWidth - 120, 80)
    displaysurf.blit(nextSurf, nextRect)

    # draw the "next" piece
    drawPiece(piece, pixelx=windowWidth-120, pixely=100)


if __name__ == '__main__':
    main()
