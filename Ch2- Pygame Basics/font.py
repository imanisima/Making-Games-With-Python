import pygame, sys
from pygame.locals import *

"""
Drawing text on a screen
"""

pygame.init()
displaysurf = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Drawing Text")

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

fontObj = pygame.font.Font("freesansbold.ttf", 32)
textSurf = fontObj.render("Hello world!", True, blue, green)
textRect = textSurf.get_rect()
textRect.center = (200, 150)

while True:
    displaysurf.fill(white)
    displaysurf.blit(textSurf, textRect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
