import pygame
import sys

pygame.init()

SCREEN_W = 900
SCREEN_H = 600

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PUCPR survivor")

clock = pygame.time.Clock()
FPS = 60

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((28,28,38))
    pygame.display.flip()