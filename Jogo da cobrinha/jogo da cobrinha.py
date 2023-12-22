import pygame
from pygame.locals import *
import random 


TAMANHO_JANELA = (600,600)
TAMANHO_PIXEL = 10


def colisao(pos1, pos2):
    return pos1 == pos2

def limite_parede(pos):
    if 0 <= pos[0] < TAMANHO_JANELA[0] and 0 <= pos[1] < TAMANHO_JANELA[1]:
        return False
    else:
        return True
    
def random_tela():
    x = random.randint(0, TAMANHO_JANELA[0])
    y = random.randint(0, TAMANHO_JANELA[1])
    return x // TAMANHO_PIXEL * TAMANHO_PIXEL, y // TAMANHO_PIXEL * TAMANHO_PIXEL

def reiniciar_jogo():
    global cobra_pos
    global maça_pos
    global cobra_direçao
    cobra_pos = [(250, 50), (260, 50), (270, 50)]
    cobra_direçao = K_LEFT 
    maça_pos = random_tela()

def desenhar_botao(texto, pos):
    fonte = pygame.font.Font(None,36)
    texto_render = fonte.render(texto, True, (255, 255, 255))
    retangulo = texto_render.get_rect(center = pos)
    return texto_render, retangulo
    
def botao_clicado(pos, button_rect):
    return button_rect.collidepoint(pos)


pygame.init()
janela = pygame.display.set_mode(TAMANHO_JANELA)
pygame.display.set_caption("A VIDA SNAKE")


cobra_pos = [(250, 50), (260, 50), (270, 50)]
cobra_superfice = pygame.Surface((TAMANHO_PIXEL, TAMANHO_PIXEL))
cobra_superfice.fill((255, 255, 255))
cobra_direçao = K_LEFT 

maça_superfice = pygame.Surface((TAMANHO_PIXEL, TAMANHO_PIXEL))
maça_superfice.fill((255, 0, 0))
maça_pos = random_tela()

botao_iniciar_texto, botao_iniciar_rect = desenhar_botao("Iniciar", (TAMANHO_JANELA[0] // 2, TAMANHO_JANELA[1] // 2))

iniciado = False
while True:
    pygame.time.Clock().tick(15)
    janela.fill((0,0,0))

    mouse_pos = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            quit()

        elif evento.type == MOUSEBUTTONDOWN and not iniciado:
            if botao_clicado(mouse_pos, botao_iniciar_rect):
                iniciado = True
            if not iniciado:
                janela.blit(botao_iniciar_texto, botao_iniciar_rect)

        elif evento.type == KEYDOWN:
            if evento.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                cobra_direçao = evento.key 

    janela.blit(maça_superfice, maça_pos)
    
    if colisao(maça_pos, cobra_pos[0]):
        cobra_pos.append((-10,-10))
        maça_pos = random_tela()


    for pos in cobra_pos:
        janela.blit(cobra_superfice, pos)


    for i in range(len(cobra_pos)-1,0,-1):
        if colisao(cobra_pos[0], cobra_pos[i]):
           reiniciar_jogo()
        cobra_pos[i] = cobra_pos[i-1]
      
    if limite_parede(cobra_pos[0]):
      reiniciar_jogo()

    if cobra_direçao == K_UP:
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] - TAMANHO_PIXEL)
    elif cobra_direçao == K_DOWN:
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] + TAMANHO_PIXEL)
    elif cobra_direçao == K_LEFT:
        cobra_pos[0] = (cobra_pos[0][0] -TAMANHO_PIXEL, cobra_pos[0][1])
    elif cobra_direçao == K_RIGHT:
        cobra_pos[0] = (cobra_pos[0][0] + TAMANHO_PIXEL, cobra_pos[0][1])

    pygame.display.update()