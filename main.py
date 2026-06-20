import pygame
import sys
import math

pygame.init()

SCREEN_W = 1100
SCREEN_H = 700

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("PUCPR Survivor")

clock = pygame.time.Clock()
FPS = 60

fonte = pygame.font.SysFont("Arial", 14, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 72, bold=True)
fonte_media = pygame.font.SysFont("Arial", 36, bold=True)

estado = "menu"

fases = [
    {"top": 200, "bottom": 500},
    {"top": 180, "bottom": 520},
    {"top": 160, "bottom": 540},
    {"top": 140, "bottom": 560},
    {"top": 120, "bottom": 580},
]

for f in fases:
    f["paredes"] = [
        pygame.Rect(0, 0, SCREEN_W, f["top"]),
        pygame.Rect(0, f["bottom"], SCREEN_W, SCREEN_H - f["bottom"]),
    ]
    f["meta"] = pygame.Rect(1060, f["top"], 10, f["bottom"] - f["top"])

fase_atual = 0

def mover_com_colisao(rect, dx, dy):
    paredes = fases[fase_atual]["paredes"]

    rect.x += int(dx)
    if rect.left < 0: rect.left = 0
    if rect.right > SCREEN_W: rect.right = SCREEN_W

    rect.y += int(dy)
    for parede in paredes:
        if rect.colliderect(parede):
            if dy > 0: rect.bottom = parede.top
            if dy < 0: rect.top    = parede.bottom

player_speed = 4.5
TAMANHO = 22

INIMIGOS_CONFIG = [
    {"nome": "Unicesumar",  "cor": (0, 80, 200),    "tipo": "perseguicao", "speed": 2.2, "fase_inicio": 0},
    {"nome": "Unibrasil",   "cor": (230, 190, 0),   "tipo": "perseguicao", "speed": 2.4, "fase_inicio": 1},
    {"nome": "Unicuritiba", "cor": (150, 50, 200),  "tipo": "perseguicao", "speed": 2.6, "fase_inicio": 2},
    {"nome": "Positivo",    "cor": (255, 120, 0),   "tipo": "perseguicao", "speed": 2.8, "fase_inicio": 3},
    {"nome": "UTFPR",       "cor": (120, 120, 120), "tipo": "patrulha",    "speed": 6.0, "fase_inicio": 4, "x_fixo": 780},
    {"nome": "UFPR",        "cor": (255, 255, 255), "tipo": "patrulha",    "speed": 6.0, "fase_inicio": 4, "x_fixo": 920},
]

def criar_inimigos():
    inimigos = []
    top = fases[fase_atual]["top"]
    bottom = fases[fase_atual]["bottom"]

    contador_perseguicao = 0
    for cfg in INIMIGOS_CONFIG:
        if cfg["fase_inicio"] > fase_atual:
            continue

        if cfg["tipo"] == "perseguicao":
            sx = 480.0 + contador_perseguicao * 130
            centro_y = (top + bottom) / 2
            offsets_y = [0, 80, -80, 40]
            sy = centro_y + offsets_y[contador_perseguicao % len(offsets_y)]
            x_ativacao = 60.0 + contador_perseguicao * 220
            contador_perseguicao += 1
            inimigos.append({
                "nome":       cfg["nome"],
                "cor":        cfg["cor"],
                "tipo":       "perseguicao",
                "speed":      cfg["speed"],
                "x":          sx,
                "y":          sy,
                "rect":       pygame.Rect(int(sx), int(sy), TAMANHO, TAMANHO),
                "ativo":      contador_perseguicao == 1,
                "x_ativacao": x_ativacao,
            })
        else:
            sx = float(cfg["x_fixo"])
            if cfg["nome"] == "UTFPR":
                sy = top + 10
                direcao = 1
            else:
                sy = bottom - TAMANHO - 10
                direcao = -1
            inimigos.append({
                "nome":    cfg["nome"],
                "cor":     cfg["cor"],
                "tipo":    "patrulha",
                "speed":   cfg["speed"],
                "x":       sx,
                "y":       sy,
                "rect":    pygame.Rect(int(sx), int(sy), TAMANHO, TAMANHO),
                "direcao": direcao,
            })
    return inimigos

def resetar_jogo():
    global player, inimigos
    top = fases[fase_atual]["top"]
    bottom = fases[fase_atual]["bottom"]
    centro_y = (top + bottom) / 2 - TAMANHO / 2
    player = pygame.Rect(60, int(centro_y), TAMANHO, TAMANHO)
    inimigos = criar_inimigos()

resetar_jogo()

btn_jogar   = pygame.Rect(SCREEN_W // 2 - 100, 320, 200, 55)
btn_sair    = pygame.Rect(SCREEN_W // 2 - 100, 400, 200, 55)
btn_retry   = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)
btn_proxima = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)
btn_vitoria_menu = pygame.Rect(SCREEN_W // 2 - 150, 340, 300, 55)

while True:
    clock.tick(FPS)
    if estado == "jogando":
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

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
                if btn_retry.collidepoint(mouse):
                    resetar_jogo()
                    estado = "jogando"

            if estado == "fase_completa":
                if btn_proxima.collidepoint(mouse):
                    fase_atual += 1
                    resetar_jogo()
                    estado = "jogando"

            if estado == "vitoria":
                if btn_vitoria_menu.collidepoint(mouse):
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
            if ini["tipo"] == "perseguicao" and not ini["ativo"]:
                if player.x > ini["x_ativacao"]:
                    ini["ativo"] = True

        top = fases[fase_atual]["top"]
        bottom = fases[fase_atual]["bottom"]

        for ini in inimigos:
            if ini["tipo"] == "perseguicao" and ini["ativo"]:
                dx_i = player.x - ini["x"]
                dy_i = player.y - ini["y"]
                distancia = math.hypot(dx_i, dy_i)

                if distancia > 0:
                    move_x = (dx_i / distancia) * ini["speed"]
                    move_y = (dy_i / distancia) * ini["speed"]
                    ini["x"] += move_x
                    ini["y"] += move_y
                    ini["rect"].x = int(ini["x"])
                    ini["rect"].y = int(ini["y"])
                    if ini["rect"].top < top: ini["rect"].top = top
                    if ini["rect"].bottom > bottom: ini["rect"].bottom = bottom
                    ini["y"] = float(ini["rect"].y)

            elif ini["tipo"] == "patrulha":
                ini["y"] += ini["direcao"] * ini["speed"]
                ini["rect"].y = int(ini["y"])
                if ini["rect"].top <= top:
                    ini["rect"].top = top
                    ini["direcao"] = 1
                if ini["rect"].bottom >= bottom:
                    ini["rect"].bottom = bottom
                    ini["direcao"] = -1
                ini["y"] = float(ini["rect"].y)

            if player.colliderect(ini["rect"]):
                estado = "game_over"

        perseguidores = [i for i in inimigos if i["tipo"] == "perseguicao" and i["ativo"]]
        for i in range(len(perseguidores)):
            for j in range(i + 1, len(perseguidores)):
                a = perseguidores[i]
                b = perseguidores[j]
                if a["rect"].colliderect(b["rect"]):
                    dx_ab = a["x"] - b["x"]
                    dy_ab = a["y"] - b["y"]
                    dist_ab = math.hypot(dx_ab, dy_ab)
                    if dist_ab == 0:
                        dist_ab = 1
                    empurrao = 0.6
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

    if estado == "jogando" or estado == "game_over":
        for parede in fases[fase_atual]["paredes"]:
            pygame.draw.rect(screen, (100, 100, 120), parede)

        pygame.draw.rect(screen, (0, 255, 0), fases[fase_atual]["meta"])

        pygame.draw.rect(screen, (200, 20, 20), player)
        texto_puc = fonte.render("PUCPR", True, (255, 255, 255))
        puc_x = player.x + (TAMANHO - texto_puc.get_width()) // 2
        screen.blit(texto_puc, (puc_x, player.y + TAMANHO + 4))

        for ini in inimigos:
            pygame.draw.rect(screen, ini["cor"], ini["rect"])
            pygame.draw.rect(screen, (255, 255, 255), ini["rect"], 2)
            texto_ini = fonte.render(ini["nome"], True, (255, 255, 255))
            tx = ini["rect"].x + (TAMANHO - texto_ini.get_width()) // 2
            screen.blit(texto_ini, (tx, ini["rect"].y + TAMANHO + 4))

        hud = fonte_media.render(f"Fase {fase_atual + 1}", True, (255, 255, 255))
        screen.blit(hud, (10, 10))

    if estado == "game_over":
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_go = fonte_grande.render("GAME OVER", True, (220, 30, 30))
        screen.blit(txt_go, (SCREEN_W // 2 - txt_go.get_width() // 2, 180))

        pygame.draw.rect(screen, (50, 50, 150), btn_retry, border_radius=8)
        txt_retry = fonte_media.render("Tentar Novamente", True, (255, 255, 255))
        screen.blit(txt_retry, (btn_retry.x + (300 - txt_retry.get_width()) // 2, btn_retry.y + 10))

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

        pygame.draw.rect(screen, (50, 50, 150), btn_vitoria_menu, border_radius=8)
        txt_menu = fonte_media.render("Voltar ao Menu", True, (255, 255, 255))
        screen.blit(txt_menu, (btn_vitoria_menu.x + (300 - txt_menu.get_width()) // 2, btn_vitoria_menu.y + 10))

    pygame.display.flip()