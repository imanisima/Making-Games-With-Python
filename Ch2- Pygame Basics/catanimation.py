import pygame, sys
from pygame.locals import *

"""
Example program demonstrating a cat animation
"""

pygame.init()

# ensure game runs in specific FPS
FPS = 30
fpsClock = pygame.time.Clock()

# Window set-up
displaysurf = pygame.display.set_mode((400, 360), 0, 32)
pygame.display.set_caption("Animation")

# Color & Sprites (images)
white = (255, 255, 255)
cat_image = pygame.image.load("cat.png")
cat_image2 = pygame.image.load("cat.png")
cat_x = 10
cat_y = 10
direction = "right"

# game loop
while True:
    displaysurf.fill(white)

    sound = pygame.mixer.Sound("beep1.ogg")
    sound.play()

    if direction == "right":
        cat_x += 5
        if cat_x == 280:
            direction = "down"
    elif direction == "down":
        cat_y += 5
        if cat_y == 220:
            direction = "left"
    elif direction == "left":
        cat_x -= 5
        if cat_x == 10:
            direction = "up"
    elif direction == "up":
        cat_y -= 5
        if cat_y == 10:
            direction = "right"

    # copy image's surface object onto the displace surface object
    displaysurf.blit(cat_image, (cat_x, cat_y))
    displaysurf.blit(cat_image2, (cat_y, cat_x))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS) # ensure game runs at the same speed no matter how fast the computer
