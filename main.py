import pygame
import sys
import math

pygame.init()

SCREEN_W = 900
SCREEN_H = 600

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PUCPR Survivor")

clock = pygame.time.Clock()
FPS = 60

fonte = pygame.font.SysFont("Arial", 14, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 72, bold=True)
fonte_media = pygame.font.SysFont("Arial", 36, bold=True)

estado = "menu"

def resetar_jogo():
    global player, inimigo_x, inimigo_y, inimigo
    player    = pygame.Rect(60, 282, 36, 36)
    inimigo_x = 50.0
    inimigo_y = 50.0
    inimigo   = pygame.Rect(50, 50, 36, 36)

resetar_jogo()

player_speed  = 4.0
inimigo_speed = 2.0

# botoes das telas
btn_jogar = pygame.Rect(SCREEN_W // 2 - 100, 320, 200, 55)
btn_sair  = pygame.Rect(SCREEN_W // 2 - 100, 400, 200, 55)
btn_menu  = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if estado == "menu":
                if btn_jogar.collidepoint(mouse):
                    resetar_jogo()
                    estado = "jogando"
                if btn_sair.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

            if estado == "game_over":
                if btn_menu.collidepoint(mouse):
                    estado = "menu"

    # logica do jogo
    if estado == "jogando":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.x += player_speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: player.y -= player_speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player.y += player_speed

        dx = player.x - inimigo_x
        dy = player.y - inimigo_y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            inimigo_x += (dx / distancia) * inimigo_speed
            inimigo_y += (dy / distancia) * inimigo_speed
            inimigo.x = int(inimigo_x)
            inimigo.y = int(inimigo_y)

        if player.colliderect(inimigo):
            estado = "game_over"

    screen.fill((28, 28, 38))

    # tela de menu
    if estado == "menu":
        titulo = fonte_grande.render("PUCPR Survivor", True, (200, 20, 20))
        screen.blit(titulo, (SCREEN_W // 2 - titulo.get_width() // 2, 150))

        pygame.draw.rect(screen, (50, 150, 50), btn_jogar, border_radius=8)
        pygame.draw.rect(screen, (150, 30, 30), btn_sair,  border_radius=8)

        txt_jogar = fonte_media.render("Jogar", True, (255, 255, 255))
        txt_sair  = fonte_media.render("Sair",  True, (255, 255, 255))

        screen.blit(txt_jogar, (btn_jogar.x + (200 - txt_jogar.get_width()) // 2, btn_jogar.y + 10))
        screen.blit(txt_sair,  (btn_sair.x  + (200 - txt_sair.get_width())  // 2, btn_sair.y  + 10))

    # tela de jogo
    if estado == "jogando":
        pygame.draw.rect(screen, (200, 20, 20), player)
        texto_puc = fonte.render("PUCPR", True, (255, 255, 255))
        puc_x = player.x + (36 - texto_puc.get_width()) // 2
        screen.blit(texto_puc, (puc_x, player.y + 40))

        pygame.draw.rect(screen, (0, 80, 200), inimigo)
        texto_uni = fonte.render("Unicesumar", True, (255, 255, 255))
        uni_x = inimigo.x + (36 - texto_uni.get_width()) // 2
        screen.blit(texto_uni, (uni_x, inimigo.y + 40))

    # tela de game over
    if estado == "game_over":
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_go = fonte_grande.render("GAME OVER", True, (220, 30, 30))
        screen.blit(txt_go, (SCREEN_W // 2 - txt_go.get_width() // 2, 180))

        pygame.draw.rect(screen, (50, 50, 150), btn_menu, border_radius=8)
        txt_menu = fonte_media.render("Voltar ao Menu", True, (255, 255, 255))
        screen.blit(txt_menu, (btn_menu.x + (300 - txt_menu.get_width()) // 2, btn_menu.y + 10))

    pygame.display.flip()