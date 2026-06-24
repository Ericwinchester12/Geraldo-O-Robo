import pygame # importa a lib de jogos
# tem que dar init antes de tudo
pygame.init()
# tamanho da matriz
TAMANHO = 5
# cada quadrado tem 100px
BLOCO = 100
# 5 * 100 = 500px de largura
LARGURA = TAMANHO * BLOCO
# 500px + 60px pro menu escuro embaixo
ALTURA = TAMANHO * BLOCO + 60
# cria a janela com o calculo de cima
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo")
# fonte que vamos usar dps pros textos
fonte = pygame.font.SysFont("arial", 20)
# relogio pra travar o FPS senao o jogo crasha
clock = pygame.time.Clock()
rodando = True
# while q dxa o jogo aberto
while rodando:
    clock.tick(30) # trava em 30 fps
    # ler se o usuario apertou alguma coisa
    for evento in pygame.event.get():
        # clicou no X
        if evento.type == pygame.QUIT:
            rodando = False
    # pinta a tela de preto pra apagar o frame velho
    tela.fill((0, 0, 0))
    # desenha o chao do galpao
    # for das linhas
    for i in range(TAMANHO):
        # for das colunas
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            # matematica de modulo pra fazer xadrez claro/escuro
            if (i + j) % 2 == 0:
                pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
            else:
                pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
            # bordinha em volta da casa
            pygame.draw.rect(tela, (70, 70, 90), (x, y, BLOCO, BLOCO), 1)
    # desenha a gradezinha certa
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (100, 100, 120), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (100, 100, 120), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
    # menu preto debaixo q vai ficar a vida e as coisas dps
    pygame.draw.rect(tela, (20, 20, 30), (0, TAMANHO * BLOCO, LARGURA, 60))
    # atualiza a tela
    pygame.display.flip()
pygame.quit()
