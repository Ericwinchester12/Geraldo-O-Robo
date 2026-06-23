
import pygame
pygame.init()
# configs da tela
TAMANHO = 5
BLOCO = 100
LARGURA = TAMANHO * BLOCO
ALTURA = TAMANHO * BLOCO + 60
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo - Bug do Milênio")
fonte = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()
# loop principal so pra testar a tela
rodando = True
while rodando:
    clock.tick(30)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    tela.fill((0, 0, 0))
    # desenha o tabuleiro 5x5
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            if (i + j) % 2 == 0:
                pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
            else:
                pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
            pygame.draw.rect(tela, (70, 70, 90), (x, y, BLOCO, BLOCO), 1)
    # linhas da grade
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (100, 100, 120), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (100, 100, 120), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
    # barra de info embaixo
    pygame.draw.rect(tela, (20, 20, 30), (0, TAMANHO * BLOCO, LARGURA, 60))
    pygame.display.flip()
pygame.quit()
