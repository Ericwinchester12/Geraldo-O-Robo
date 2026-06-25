import pygame # importa a lib do pygame
import random # pra sortear onde os itens vao cair dps
pygame.init()
# tamanho e resolucao da tela
TAMANHO = 5
BLOCO = 100
LARGURA = TAMANHO * BLOCO
ALTURA = TAMANHO * BLOCO + 60
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo - Bug do Milênio")
fonte = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()
# cria a classe pro robo pra usar orientacao a objetos
class Geraldo:
    # construtor da classe, seta como ele comeca
    def __init__(self):
        self.lin = 0 # comeca na linha 0 (cima)
        self.col = 0 # comeca na coluna 0 (esquerda)
        self.energia = 3 # energia inicial do robo
        self.coletados = 0 # quantos componentes pegou
    # funcao de andar, recebe pra onde vai
    # retorna True se andou, False se bateu em parede do mapa
    def mover(self, direcao):
        # tenta subir
        if direcao == "cima" and self.lin > 0:
            self.lin -= 1
            return True
        # tenta descer
        elif direcao == "baixo" and self.lin < TAMANHO - 1:
            self.lin += 1
            return True
        # tenta ir pra esquerda
        elif direcao == "esquerda" and self.col > 0:
            self.col -= 1
            return True
        # tenta ir pra direita
        elif direcao == "direita" and self.col < TAMANHO - 1:
            self.col += 1
            return True
        
        # se nao deu nenhum dos if ali de cima,é pq bateu em parede
        return False
# dicionario pra mapear as teclas de movimento
teclas = {
    pygame.K_w: "cima",
    pygame.K_UP: "cima",
    pygame.K_s: "baixo",
    pygame.K_DOWN: "baixo",
    pygame.K_a: "esquerda",
    pygame.K_LEFT: "esquerda",
    pygame.K_d: "direita",
    pygame.K_RIGHT: "direita"
}
# cria o objeto do robo
geraldo = Geraldo()
# mensagem que vai aparecer na barra inferior
msg = ""
rodando = True
# laco principal do jogo
while rodando:
    clock.tick(30) 
    # ler se o usuario fechou ou apertou tecla
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        # se apertou uma tecla que a gente mapeou
        if evento.type == pygame.KEYDOWN and evento.key in teclas:
            direcao = teclas[evento.key] 
            moveu = geraldo.mover(direcao) 
            # avisa se tentar sair do mapa
            if not moveu:
                msg = "Você bateu em uma parede"
            else:
                msg = "" 
    # limpa a tela pintando de preto
    tela.fill((0, 0, 0))
    # for pra desenhar o tabuleiro xadrez
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            if (i + j) % 2 == 0:
                pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
            else:
                pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
            # bordinha
            pygame.draw.rect(tela, (70, 70, 90), (x, y, BLOCO, BLOCO), 1)
    # desenha o robo geraldo (P) na tela
    gx = geraldo.col * BLOCO 
    gy = geraldo.lin * BLOCO 
    pygame.draw.rect(tela, (0, 130, 255), (gx + 10, gy + 10, 80, 80)) 
    texto_robo = fonte.render("P", True, (255, 255, 255))
    tela.blit(texto_robo, (gx + 40, gy + 37))
    # desenha o servidor (S) no canto direito inferior
    sx = 4 * BLOCO
    sy = 4 * BLOCO
    pygame.draw.rect(tela, (130, 0, 200), (sx + 10, sy + 10, 80, 80)) 
    texto_servidor = fonte.render("S", True, (255, 255, 255))
    tela.blit(texto_servidor, (sx + 42, sy + 37))
    # linhas da grade
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (100, 100, 120), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (100, 100, 120), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
    # barra de informações
    pygame.draw.rect(tela, (20, 20, 30), (0, TAMANHO * BLOCO, LARGURA, 60))
    # escreve a energia na barra
    texto_energia = fonte.render("Energia: " + str(geraldo.energia), True, (0, 200, 80))
    tela.blit(texto_energia, (10, TAMANHO * BLOCO + 5))
    # mostra a mensagem de parede se tiver
    if msg != "":
        texto_msg = fonte.render(msg, True, (255, 140, 0))
        tela.blit(texto_msg, (200, TAMANHO * BLOCO + 18))
    # atualiza a tela
    pygame.display.flip()
pygame.quit()
