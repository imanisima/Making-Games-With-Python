import pygame, sys
from pygame.locals import *

"""
Use different drawing functions to create surface objects or shapes
"""

pygame.init()
displaysurf = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Drawing")

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
maroon = (128, 0, 0)
silver = (192, 192, 192)

# Draw
displaysurf.fill(white)
pygame.draw.polygon(displaysurf, silver, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(displaysurf, green, (60, 60), (120, 60), 4)
pygame.draw.line(displaysurf, green, (120, 60), (60, 120))
pygame.draw.line(displaysurf, green, (60, 120), (120, 120), 4)
pygame.draw.circle(displaysurf, maroon, (300, 50), 20, 0)
pygame.draw.ellipse(displaysurf, blue, (300, 250, 40, 80), 1)
pygame.draw.rect(displaysurf, red, (200, 150, 100, 50))

pixObj = pygame.PixelArray(displaysurf)
pixObj[480][380] = black
pixObj[492][382] = black
pixObj[484][384] = black
pixObj[486][386] = black
pixObj[488][388] = black
del pixObj

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
