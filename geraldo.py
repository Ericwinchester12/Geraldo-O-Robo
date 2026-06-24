
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
