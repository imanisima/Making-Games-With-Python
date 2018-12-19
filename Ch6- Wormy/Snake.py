import random, pygame, sys
from pygame.locals import *

FPS = 15
windowWidth = 700
windowHeight = 580
cellsize = 20
assert windowWidth % cellsize == 0, "Window width must be a MULTIPLE of cell size."
assert windowHeight % cellsize == 0, "Window height must be a MULTIPLE of cell size"
cellWidth = int(windowWidth/cellsize)
cellHeight = int(windowHeight/cellsize)

# COLORS
white     = (255, 255, 255)
black     = (0, 0, 0)
red       = (153, 0, 0)
purple    = (153, 0, 76)
green     = (0, 204, 0)
darkGreen = (76, 153, 0)
gray      = (32, 32, 32)
yellow    = (255, 255, 0)

bgColor = black

# DIRECTIONS
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0  # Snake head


def main():
    global fpsClock, displaysurf, basicFont

    pygame.init()
    fpsClock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowWidth, windowHeight))
    basicFont = pygame.font.Font("freesansbold.ttf", 16)
    pygame.display.set_caption("Snake")

    showStartScreen()
    while True:
        startGame()
        displaysurf.fill(bgColor)
        showGameOverScreen()


def startGame():
    # Set a random start point
    start_x = random.randint(5, cellWidth - 6)
    start_y = random.randint(5, cellHeight - 6)
    snakeCoors = [{"x": start_x, "y": start_y},
                  {"x": start_x - 1, "y": start_y},
                  {"x": start_x - 2, "y": start_y}]
    direction = RIGHT

    # Place the apple in a random place
    apple = getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # Check if the snake has reached the edge -> game over
        if snakeCoors[HEAD]["x"] == -1 or snakeCoors[HEAD]["x"] == cellWidth or snakeCoors[HEAD]["y"] == -1 or snakeCoors[HEAD]["y"] == cellHeight:
            return

        # Check if the snake has consumed itself -> gameway
        for snakeBody in snakeCoors[1:]:
            if snakeBody["x"] == snakeCoors[HEAD]["x"] and snakeBody["y"] == snakeCoors[HEAD]["y"]:
                return

        # Check if snake has eaten an apple
        if snakeCoors[HEAD]["x"] == apple["x"] and snakeCoors[HEAD]["y"] == apple["y"]:
            # Don't remove snake's tail segment & set a new apple somewhere
            apple = getRandomLocation()
        else:
            # otherwise, remove a tail segment
            del snakeCoors[-1]

        # Move the snake by adding a segment in the direction it is going
        if direction == UP:
            newHead = {"x": snakeCoors[HEAD]["x"], "y": snakeCoors[HEAD]["y"] - 1}
        elif direction == DOWN:
            newHead = {"x": snakeCoors[HEAD]["x"], "y": snakeCoors[HEAD]["y"] + 1}
        elif direction  == LEFT:
            newHead = {"x": snakeCoors[HEAD]["x"] - 1, "y": snakeCoors[HEAD]["y"]}
        elif direction == RIGHT:
            newHead = {"x": snakeCoors[HEAD]["x"] + 1, "y": snakeCoors[HEAD]["y"]}

        snakeCoors.insert(0, newHead)
        displaysurf.fill(bgColor)
        drawGrid()
        drawSnake(snakeCoors)
        drawApple(apple)
        drawScore(len(snakeCoors) - 3)
        pygame.display.update()
        fpsClock.tick(FPS)


def drawPressKeyMsg(message):
    pressKeySurf = basicFont.render(message, True, white)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (windowWidth - 350, windowHeight - 50)
    displaysurf.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None

    if keyUpEvents[0].key == K_ESCAPE:
        terminate()

    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font("freesansbold.ttf", 90)
    titleSurf1 = titleFont.render("WORMY", True, white, darkGreen)
    titleSurf2 = titleFont.render("WORMY", True, green)

    degrees1 = 0
    degrees2 = 0

    while True:
        displaysurf.fill(bgColor)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (windowWidth /2, windowHeight / 2)
        displaysurf.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (windowWidth / 2, windowHeight / 2)
        displaysurf.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg("Press Any Key To Start...")

        if checkForKeyPress():
            pygame.event.get()
            return

        pygame.display.update()
        fpsClock.tick(FPS)
        degrees1 += 3
        degrees2 += 7


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {"x": random.randint(0, cellWidth - 1), "y": random.randint(0, cellHeight - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 100)
    gameSurf = gameOverFont.render("GAME", True, green)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (windowWidth / 2, 100)

    gameSurf2 = gameOverFont.render("GAME", True, white)
    gameRect2 = gameSurf2.get_rect()
    gameRect2.midtop = (windowWidth / 2, 110)

    overSurf = gameOverFont.render("OVER", True, green)
    overRect = overSurf.get_rect()
    overRect.midtop = (windowWidth / 2, gameRect.height + 80 + 25)

    overSurf2 = gameOverFont.render("OVER", True, white)
    overRect2 = overSurf2.get_rect()
    overRect2.midtop = (windowWidth / 2, gameRect.height + 90 + 25)

    displaysurf.blit(gameSurf, gameRect)
    displaysurf.blit(gameSurf2, gameRect2)
    displaysurf.blit(overSurf, overRect)
    displaysurf.blit(overSurf2, overRect2)

    drawPressKeyMsg("Press Any Key To Start Again Or ESC To Quit...")
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return


def drawScore(score):
    scoreSurf = basicFont.render("Score: %s" % score, True, white)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windowWidth - 80, 5)
    displaysurf.blit(scoreSurf, scoreRect)


def drawSnake(snakeCoor):
    for coordinate in snakeCoor:
        x = coordinate["x"] * cellsize
        y = coordinate["y"] * cellsize
        snakeSegmentRect = pygame.Rect(x, y, cellsize, cellsize)
        pygame.draw.rect(displaysurf, red, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, cellsize - 8, cellsize - 8)
        pygame.draw.rect(displaysurf, green, snakeInnerSegmentRect)


def drawApple(coordinate):
    x = coordinate["x"] * cellsize
    y = coordinate["y"] * cellsize
    appleRect = pygame.Rect(x + 4, y + 5, cellsize/2, cellsize/2)
    pygame.draw.rect(displaysurf, yellow, appleRect)


def drawGrid():
    for x in range(0, windowWidth, cellsize):  # veritcal lines
        pygame.draw.line(displaysurf, gray, (x, 0), (x, windowHeight))
        for y in range(0, windowHeight, cellsize):  # horizontal
            pygame.draw.line(displaysurf, gray, (0, y), (windowWidth, y))


if __name__ == '__main__':
    main()
