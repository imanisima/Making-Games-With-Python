import random, pygame, sys
from pygame.locals import *

"""
Memory Puzzle game
"""

FPS = 30
windowWidth = 640
windowHeight = 480
revealSpeed = 8  # the speed at which boxes are covered and uncovered

boxSize = 40  # width & height of boxes in pixels
gapSize = 10  # size of gaps between boxes

boardWidth = 8  # number of icons [cols]
boardHeight = 6  # number of icons [rows]

# Margins
assert (boardWidth * boardHeight) % 2 == 0, "Board must have an even number of boxes for matches."
x_margin = int((windowWidth - (boardWidth * (boxSize + gapSize))) / 2)
y_margin = int((windowHeight - (boardHeight * (boxSize + gapSize))) / 2)

# colors --  R    B    G
gray     = (100, 100, 100)
navyBlue = (60, 60, 100)
blue     = (0, 128, 0)
white    = (255, 255, 255)
red      = (128, 0, 0)
reddish     = (238, 98, 98)
green    = (0, 0, 128)
yellow   = (255,255, 0)
orange   = (255, 128, 0)
purple   = (255, 0, 255)
cyan     = (0, 255, 255)

bgColor = navyBlue
lightBgColor = gray
boxColor = white
highlightColor = blue

donut = "donut"
square = "square"
diamond = "diamond"
lines = "lines"
oval = "oval"

allColors = (red, green, blue, yellow, orange, purple, cyan)
allShapes = (donut, square, diamond, lines, oval)
assert len(allColors) * len(allShapes) * 2 >= boardHeight * boardWidth, "Board is too large for the number of shapes/colors defined!"


def main():
    global fpsClock, displaysurf, basicFont

    pygame.init()
    fpsClock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowWidth, windowHeight))
    basicFont = pygame.font.Font("freesansbold.ttf", 16)
    pygame.display.set_caption("Memory Game")

    pygame.mixer.music.load("royalty.mp3")
    pygame.mixer.music.play(-1, 0.0)

    # Capture mouse events
    mouse_x = 0
    mouse_y = 0

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    firstSelection = None
    displaysurf.fill(bgColor)

    while True:
        showStartScreen(mainBoard)
        showShuffleMsg()
        startGameAnimation(mainBoard)

        while True:
            mouseClicked = False

            displaysurf.fill(bgColor)
            showTitle()
            drawBoard(mainBoard, revealedBoxes)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    mouseClicked = True

            box_x, box_y = getBoxAtPixel(mouse_x, mouse_y)
            if box_x is not None and box_y is not None:
                # The mouse is currently over a box
                if not revealedBoxes[box_x][box_y]:
                    drawHighlightBox(box_x, box_y)

                if not revealedBoxes[box_x][box_y] and mouseClicked:
                    revealBoxesAnimation(mainBoard, [(box_x, box_y)])
                    revealedBoxes[box_x][box_y] = True  # set box as now revealed

                    if firstSelection is None:  # curr box was the first box clicked
                        firstSelection = (box_x, box_y)

                    else:  # curr box was the second box clicked
                        # check if there is a match
                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard, box_x, box_y)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # Icons do not match -> recover them
                            pygame.time.wait(1000) # 1000 milliseconds or 1 min

                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (box_x, box_y)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[box_x][box_y] = False

                        # Check if all pairs are found
                        elif hasWon(revealedBoxes):
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)

                            # Reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)

                            # Show the fully unrevealed board for 1 sec
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            # Replay the start game animation
                            startGameAnimation(mainBoard)

                        # Reset first selection var
                        firstSelection = None

            # Redraw the screen
            pygame.display.update()
            fpsClock.tick(FPS)


def showStartScreen(startboard):
    while True:
        showTitle()
        startGameAnimation(startboard)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return

        pygame.display.update()
        fpsClock.tick(FPS)


def showTitle():
    titleFont = pygame.font.Font("freesansbold.ttf", 30)
    titleSurf = titleFont.render("MEMORY GAME!", True, reddish, bgColor)

    titleRect = titleSurf.get_rect()
    titleRect.topright = (windowWidth - 200, windowHeight - 450)
    displaysurf.blit(titleSurf, titleRect)


def drawPressKeyMsg():
    pressKeySurf = basicFont.render("Press Any Key To Play!", True, white, bgColor)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (windowWidth - 400, windowHeight - 70)
    displaysurf.blit(pressKeySurf, pressKeyRect)


def showShuffleMsg():
    shuffleSurf = basicFont.render("Now shuffling the cards...", True, white, bgColor)
    shuffleRect = shuffleSurf.get_rect()
    shuffleRect.topright = (windowWidth - 200, windowHeight - 50)
    displaysurf.blit(shuffleSurf, shuffleRect)

    pygame.display.update()
    fpsClock.tick(FPS)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


# randomly reveal the boxes 8 at a time
def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(boardWidth):
        for y in range(boardHeight):
            boxes.append((x, y))
    random.shuffle(boxes)

    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


# flash the background color when player wins
def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = lightBgColor
    color2 = bgColor

    for i in range(13):
        color1, color2 = color2, color1
        displaysurf.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


# Return true if all boxes have been revealed
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


# Splits a list into a list of lists, where inner lists have at most n number of items
def splitIntoGroupsOf(groupSize, list):
    result = []
    for i in range(0, len(list), groupSize):
        result.append(list[i:i + groupSize])
    return result


def drawBoard(board, revealed):
    for box_x in range(boardWidth):
        for box_y in range(boardHeight):
            left, top = leftTopCoordsOfBox(box_x, box_y)

            # draw covered box
            if not revealed[box_x][box_y]:
                pygame.draw.rect(displaysurf, boxColor, (left, top, boxSize, boxSize))

            # draw revealed icon
            else:
                shape, color = getShapeAndColor(board, box_x, box_y)
                drawIcon(shape, color, box_x, box_y)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(boardWidth):
        revealedBoxes.append([val] * boardHeight)
    return revealedBoxes


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(boxSize, (-revealSpeed) - 1, -revealSpeed):
        drawBoxCovers(board, boxesToReveal,coverage)


# Draw boxes being covered/revealed
def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(displaysurf, bgColor, (left, top, boxSize, boxSize))

        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])

        # only draw cover if there exists a coverage
        if coverage > 0:
            pygame.draw.rect(displaysurf, boxColor, (left, top, coverage, boxSize))

    pygame.display.update()
    fpsClock.tick(FPS)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, boxSize + revealSpeed, revealSpeed):
        drawBoxCovers(board, boxesToCover, coverage)


#  Create a board of randomly placed icons
def getRandomizedBoard():
    # list of every possible shape in every possible color
    icons = []
    for color in allColors:
        for shape in allShapes:
            icons.append((shape, color))

    # randomize the order of the icons list
    random.shuffle(icons)
    numIconsUsed = int(boardWidth * boardHeight / 2) # calculate the number of icons needed
    icons = icons[:numIconsUsed]*2  # and make two of each
    random.shuffle(icons)

    # Create the board with randomly placed icons
    board = []
    for x in range(boardWidth):
        col = []
        for y in range(boardHeight):
            col.append(icons[0])
            del icons[0] # remove the icons as they are assigned
        board.append(col)
    return board


# Drawing icon
def drawIcon(shape, color, box_x, box_y):
    quarter = int(boxSize * 0.25)
    half = int(boxSize * 0.5)

    # get pixel coors from board coors
    left, top = leftTopCoordsOfBox(box_x, box_y)

    # drawing shapes
    if shape == donut:
        pygame.draw.circle(displaysurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(displaysurf, bgColor, (left + half, top + half), quarter - 5)

    elif shape == square:
        pygame.draw.rect(displaysurf, color, (left + quarter, top + quarter, boxSize - half, boxSize - half))

    elif shape == diamond:
        pygame.draw.polygon(displaysurf, color, ((left + half, top), (left + boxSize - 1, top + half), (left + half, top + boxSize - 1), (left, top + half)))

    elif shape == lines:
        for i in range(0, boxSize, 4):
            pygame.draw.line(displaysurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(displaysurf, color, (left + i, top + boxSize - 1), (left + boxSize - 1, top + i))

    elif shape == oval:
        pygame.draw.ellipse(displaysurf, color, (left, top + quarter, boxSize, half))


def drawHighlightBox(box_x, box_y):
    left, top = leftTopCoordsOfBox(box_x, box_y)
    pygame.draw.rect(displaysurf, highlightColor, (left - 5, top - 5, boxSize + 10, boxSize + 10), 4)


# Get shapes and color
def getShapeAndColor(board, box_x, box_y):
    #  shape value for x,y spot is stored in board[x][y][0]
    #  color value for x,y spot is stored in board[x][y][1]
    return board[box_x][box_y][0], board[box_x][box_y][1]


def getBoxAtPixel(x, y):
    for box_x in range(boardWidth):
        for box_y in range(boardHeight):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            boxRect = pygame.Rect(left, top, boxSize, boxSize)
            if boxRect.collidepoint(x, y):
                return box_x, box_y

    return None, None


# Convert board coor into pixel coor
def leftTopCoordsOfBox(box_x, box_y):
    left = box_x * (boxSize + gapSize) + x_margin
    top = box_y * (boxSize + gapSize) + y_margin
    return left, top


if __name__ == '__main__':
    main()

