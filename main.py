import pygame
import sys
import math

pygame.init()

SCREEN_W = 900
SCREEN_H = 600

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PUCPR survivor")

clock = pygame.time.Clock()
FPS = 60

fonte = pygame.font.SysFont("Arial", 14, bold=True)

player = pygame.Rect(60, 282, 36, 36)
player_speed = 4.0

inimigo_x = 50.0
inimigo_y = 50.0
inimigo = pygame.Rect(50, 50, 36, 36)
inimigo_speed = 2.0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]: player.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]: player.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: player.y += player_speed

    dx = player.x - inimigo_x
    dy = player.y - inimigo_y
    distancia = math.hypot(dx, dy)
    
    if distancia > 0:
        
        inimigo_x += (dx / distancia) * inimigo_speed
        inimigo_y += (dy / distancia) * inimigo_speed
        
        inimigo.x = int(inimigo_x)
        inimigo.y = int(inimigo_y)
    
    screen.fill((28,28,38))

    pygame.draw.rect(screen, (200, 20, 20), player)
    texto_puc = fonte.render("PUCPR", True, (255, 255, 255))
    puc_x = player.x + (36 - texto_puc.get_width()) // 2
    screen.blit(texto_puc, (puc_x, player.y + 40))

    pygame.draw.rect(screen, (0, 80, 200), inimigo)
    texto_uni = fonte.render("UniCesumar", True, (255, 255, 255))
    uni_x = inimigo.x + (36 - texto_uni.get_width()) // 2
    screen.blit(texto_uni, (uni_x, inimigo.y + 40))

    pygame.display.flip()