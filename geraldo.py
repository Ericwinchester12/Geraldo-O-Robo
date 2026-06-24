
import pygame # importa a lib do pygame
import random # pra gente sortear onde os itens vao cair dps
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
# criamos a classe pro robo pra usar orientacao a objetos q pediram
class Geraldo:
    # construtor da classe, seta como ele comeca
    def __init__(self):
        self.lin = 0 # comeca na linha 0 (cima)
        self.col = 0 # comeca na coluna 0 (esquerda)
        self.energia = 3 # energia inicial do robo
        self.coletados = 0 # quantos componentes pegou
