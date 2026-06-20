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

fases = [
    {
        "paredes": [
            pygame.Rect(0, 0, 900, 150),
            pygame.Rect(0, 450, 900, 150),
        ],
        "meta": pygame.Rect(860, 150, 10, 300),
    },
    {
        "paredes": [
            pygame.Rect(0, 0, 900, 130),
            pygame.Rect(0, 470, 900, 130),
        ],
        "meta": pygame.Rect(860, 130, 10, 340),
    },
    {
        "paredes": [
            pygame.Rect(0, 0, 900, 120),
            pygame.Rect(0, 480, 900, 120),
        ],
        "meta": pygame.Rect(860, 120, 10, 360),
    },
    {
        "paredes": [
            pygame.Rect(0, 0, 900, 110),
            pygame.Rect(0, 490, 900, 110),
        ],
        "meta": pygame.Rect(860, 110, 10, 380),
    },
    {
        "paredes": [
            pygame.Rect(0, 0, 900, 100),
            pygame.Rect(0, 500, 900, 100),
        ],
        "meta": pygame.Rect(860, 100, 10, 400),
    },
]

fase_atual = 0

def mover_com_colisao(rect, dx, dy):
    paredes = fases[fase_atual]["paredes"]
    rect.x += int(dx)
    for parede in paredes:
        if rect.colliderect(parede):
            if dx > 0: rect.right  = parede.left
            if dx < 0: rect.left   = parede.right
    rect.y += int(dy)
    for parede in paredes:
        if rect.colliderect(parede):
            if dy > 0: rect.bottom = parede.top
            if dy < 0: rect.top    = parede.bottom

player_speed = 4.0

INIMIGOS_CONFIG = [
    {"nome": "Unicesumar",  "cor": (0, 80, 200),    "speed": 2.0, "fase_inicio": 0},
    {"nome": "Unibrasil",   "cor": (230, 190, 0),   "speed": 2.3, "fase_inicio": 1},
    {"nome": "Unicuritiba", "cor": (150, 50, 200),  "speed": 2.7, "fase_inicio": 2},
    {"nome": "Positivo",    "cor": (255, 120, 0),   "speed": 3.1, "fase_inicio": 3},
    {"nome": "UFPR",        "cor": (30, 30, 30),    "speed": 3.5, "fase_inicio": 4},
    {"nome": "UTFPR",       "cor": (120, 120, 120), "speed": 3.8, "fase_inicio": 4},
]

def criar_inimigos():
    inimigos = []
    spawns_x = [700, 650, 600, 550, 500, 450]
    spawns_y = [200, 350, 250, 320, 280, 230]
    for i, cfg in enumerate(INIMIGOS_CONFIG):
        if cfg["fase_inicio"] <= fase_atual:
            sx = float(spawns_x[i])
            sy = float(spawns_y[i])
            inimigos.append({
                "nome":  cfg["nome"],
                "cor":   cfg["cor"],
                "speed": cfg["speed"],
                "x":     sx,
                "y":     sy,
                "rect":  pygame.Rect(int(sx), int(sy), 36, 36),
            })
    return inimigos

def resetar_jogo():
    global player, inimigos
    player   = pygame.Rect(60, 282, 36, 36)
    inimigos = criar_inimigos()

resetar_jogo()

btn_jogar   = pygame.Rect(SCREEN_W // 2 - 100, 320, 200, 55)
btn_sair    = pygame.Rect(SCREEN_W // 2 - 100, 400, 200, 55)
btn_menu    = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)
btn_proxima = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)

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
                    fase_atual = 0
                    resetar_jogo()
                    estado = "jogando"
                if btn_sair.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

            if estado == "game_over":
                if btn_menu.collidepoint(mouse):
                    estado = "menu"

            if estado == "fase_completa":
                if btn_proxima.collidepoint(mouse):
                    fase_atual += 1
                    resetar_jogo()
                    estado = "jogando"

            if estado == "vitoria":
                if btn_menu.collidepoint(mouse):
                    fase_atual = 0
                    estado = "menu"

    if estado == "jogando":
        keys = pygame.key.get_pressed()

        dx, dy = 0.0, 0.0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += player_speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= player_speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += player_speed

        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        mover_com_colisao(player, dx, dy)

        for ini in inimigos:
            dx_i = player.x - ini["x"]
            dy_i = player.y - ini["y"]
            distancia = math.hypot(dx_i, dy_i)

            if distancia > 0:
                move_x = (dx_i / distancia) * ini["speed"]
                move_y = (dy_i / distancia) * ini["speed"]

                ini["x"] += move_x
                ini["rect"].x = int(ini["x"])
                for parede in fases[fase_atual]["paredes"]:
                    if ini["rect"].colliderect(parede):
                        if move_x > 0: ini["rect"].right = parede.left
                        if move_x < 0: ini["rect"].left  = parede.right
                        ini["x"] = float(ini["rect"].x)

                ini["y"] += move_y
                ini["rect"].y = int(ini["y"])
                for parede in fases[fase_atual]["paredes"]:
                    if ini["rect"].colliderect(parede):
                        if move_y > 0: ini["rect"].bottom = parede.top
                        if move_y < 0: ini["rect"].top    = parede.bottom
                        ini["y"] = float(ini["rect"].y)

            if player.colliderect(ini["rect"]):
                estado = "game_over"

        for i in range(len(inimigos)):
            for j in range(i + 1, len(inimigos)):
                a = inimigos[i]
                b = inimigos[j]
                if a["rect"].colliderect(b["rect"]):
                    dx_ab = a["x"] - b["x"]
                    dy_ab = a["y"] - b["y"]
                    dist_ab = math.hypot(dx_ab, dy_ab)
                    if dist_ab == 0:
                        dist_ab = 1
                    empurrao = 1.5
                    a["x"] += (dx_ab / dist_ab) * empurrao
                    a["y"] += (dy_ab / dist_ab) * empurrao
                    b["x"] -= (dx_ab / dist_ab) * empurrao
                    b["y"] -= (dy_ab / dist_ab) * empurrao
                    a["rect"].x = int(a["x"])
                    a["rect"].y = int(a["y"])
                    b["rect"].x = int(b["x"])
                    b["rect"].y = int(b["y"])

        if player.colliderect(fases[fase_atual]["meta"]):
            if fase_atual == 4:
                estado = "vitoria"
            else:
                estado = "fase_completa"

    # desenho
    screen.fill((28, 28, 38))

    if estado == "menu":
        titulo = fonte_grande.render("PUCPR Survivor", True, (200, 20, 20))
        screen.blit(titulo, (SCREEN_W // 2 - titulo.get_width() // 2, 150))

        pygame.draw.rect(screen, (50, 150, 50), btn_jogar, border_radius=8)
        pygame.draw.rect(screen, (150, 30, 30), btn_sair,  border_radius=8)

        txt_jogar = fonte_media.render("Jogar", True, (255, 255, 255))
        txt_sair  = fonte_media.render("Sair",  True, (255, 255, 255))

        screen.blit(txt_jogar, (btn_jogar.x + (200 - txt_jogar.get_width()) // 2, btn_jogar.y + 10))
        screen.blit(txt_sair,  (btn_sair.x  + (200 - txt_sair.get_width())  // 2, btn_sair.y  + 10))

    if estado == "jogando":
        for parede in fases[fase_atual]["paredes"]:
            pygame.draw.rect(screen, (100, 100, 120), parede)

        pygame.draw.rect(screen, (0, 255, 0), fases[fase_atual]["meta"])

        pygame.draw.rect(screen, (200, 20, 20), player)
        texto_puc = fonte.render("PUCPR", True, (255, 255, 255))
        puc_x = player.x + (36 - texto_puc.get_width()) // 2
        screen.blit(texto_puc, (puc_x, player.y + 40))

        for ini in inimigos:
            pygame.draw.rect(screen, ini["cor"], ini["rect"])
            texto_ini = fonte.render(ini["nome"], True, (255, 255, 255))
            tx = ini["rect"].x + (36 - texto_ini.get_width()) // 2
            screen.blit(texto_ini, (tx, ini["rect"].y + 40))

        # HUD - numero da fase
        hud = fonte_media.render(f"Fase {fase_atual + 1}", True, (255, 255, 255))
        screen.blit(hud, (10, 10))

    if estado == "game_over":
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_go = fonte_grande.render("GAME OVER", True, (220, 30, 30))
        screen.blit(txt_go, (SCREEN_W // 2 - txt_go.get_width() // 2, 180))

        pygame.draw.rect(screen, (50, 50, 150), btn_menu, border_radius=8)
        txt_menu = fonte_media.render("Voltar ao Menu", True, (255, 255, 255))
        screen.blit(txt_menu, (btn_menu.x + (300 - txt_menu.get_width()) // 2, btn_menu.y + 10))

    if estado == "fase_completa":
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_fc = fonte_grande.render(f"FASE {fase_atual + 1} COMPLETA!", True, (50, 200, 80))
        screen.blit(txt_fc, (SCREEN_W // 2 - txt_fc.get_width() // 2, 180))

        pygame.draw.rect(screen, (50, 150, 50), btn_proxima, border_radius=8)
        txt_prox = fonte_media.render("Proxima Fase", True, (255, 255, 255))
        screen.blit(txt_prox, (btn_proxima.x + (300 - txt_prox.get_width()) // 2, btn_proxima.y + 10))

    if estado == "vitoria":
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_v = fonte_grande.render("VOCE VENCEU!", True, (255, 215, 0))
        screen.blit(txt_v, (SCREEN_W // 2 - txt_v.get_width() // 2, 160))

        txt_sub = fonte_media.render("A PUCPR sobreviveu!", True, (255, 255, 255))
        screen.blit(txt_sub, (SCREEN_W // 2 - txt_sub.get_width() // 2, 270))

        pygame.draw.rect(screen, (50, 50, 150), btn_menu, border_radius=8)
        txt_menu = fonte_media.render("Voltar ao Menu", True, (255, 255, 255))
        screen.blit(txt_menu, (btn_menu.x + (300 - txt_menu.get_width()) // 2, btn_menu.y + 10))

    pygame.display.flip()