import pygame 
import random # importar random para sortear os componentes
pygame.init()
TAMANHO = 5
BLOCO = 100
LARGURA = TAMANHO * BLOCO
ALTURA = TAMANHO * BLOCO + 60
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo - Bug do Milênio")
fonte = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()
class Geraldo:
    def __init__(self):
        self.lin = 0
        self.col = 0
        self.energia = 3
        self.coletados = 0
    def mover(self, direcao):
        if direcao == "cima" and self.lin > 0:
            self.lin -= 1
            return True
        elif direcao == "baixo" and self.lin < TAMANHO - 1:
            self.lin += 1
            return True
        elif direcao == "esquerda" and self.col > 0:
            self.col -= 1
            return True
        elif direcao == "direita" and self.col < TAMANHO - 1:
            self.col += 1
            return True
        return False
# classe que gerencia a matriz do jogo e os itens ocultos
class Mapa:
    def __init__(self):
        self.grade = [] 
        self.gerar() 
    # cria a matriz 5x5 e preenche tudo com zero
    def gerar(self):
        self.grade = []
        for i in range(TAMANHO):
            linha = []
            for j in range(TAMANHO):
                linha.append(0) 
            self.grade.append(linha)
        # 2 é o código pro componente, 1 é o código pro bug
        self.sortear_itens(2, 3) 
        self.sortear_itens(1, 3) 
    # função para espalhar itens aleatoriamente na matriz
    def sortear_itens(self, tipo, quantidade):
        colocados = 0
        while colocados < quantidade:
            lin = random.randint(0, TAMANHO - 1)
            col = random.randint(0, TAMANHO - 1)
            # verifica se a casa está vazia
            if self.grade[lin][col] == 0:
                # proibe colocar o item em cima do robo (0,0) ou do servidor (4,4)
                if not (lin == 0 and col == 0) and not (lin == 4 and col == 4):
                    self.grade[lin][col] = tipo
                    colocados += 1
    # retorna o valor da casa onde o robo pisou
    def checar(self, lin, col):
        valor = self.grade[lin][col]
        # se pegou um item, zera a casa pra nao pegar de novo
        if valor != 0:
            self.grade[lin][col] = 0
        return valor
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
geraldo = Geraldo()
mapa = Mapa()
msg = ""
rodando = True
while rodando:
    clock.tick(30) 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key in teclas:
            direcao = teclas[evento.key]
            moveu = geraldo.mover(direcao)
            if not moveu:
                msg = "Você bateu em uma parede"
            else:
                # ve qual item tem no mapa na posicao nova
                item = mapa.checar(geraldo.lin, geraldo.col)
                msg = ""
                # encontrou um componente
                if item == 2:
                    geraldo.coletados += 1
                    msg = "Componente coletado! (" + str(geraldo.coletados) + "/3)"
                # encontrou o bug corruptor
                elif item == 1:
                    geraldo.energia -= 1
                    msg = "Bug Corruptor! Energia -1"
    tela.fill((0, 0, 0))
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            if (i + j) % 2 == 0:
                pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
            else:
                pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
            # desenha um '?' nas casas para representar o campo minado
            texto = fonte.render("?", True, (80, 80, 100))
            tela.blit(texto, (x + 43, y + 37))
            pygame.draw.rect(tela, (70, 70, 90), (x, y, BLOCO, BLOCO), 1)
    sx = 4 * BLOCO
    sy = 4 * BLOCO
    pygame.draw.rect(tela, (130, 0, 200), (sx + 10, sy + 10, 80, 80))
    texto_servidor = fonte.render("S", True, (255, 255, 255))
    tela.blit(texto_servidor, (sx + 42, sy + 37))
    gx = geraldo.col * BLOCO
    gy = geraldo.lin * BLOCO
    pygame.draw.rect(tela, (0, 130, 255), (gx + 10, gy + 10, 80, 80))
    texto_robo = fonte.render("P", True, (255, 255, 255))
    tela.blit(texto_robo, (gx + 40, gy + 37))
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (100, 100, 120), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (100, 100, 120), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
    pygame.draw.rect(tela, (20, 20, 30), (0, TAMANHO * BLOCO, LARGURA, 60))
    texto_energia = fonte.render("Energia: " + str(geraldo.energia), True, (0, 200, 80))
    texto_comp = fonte.render("Componentes: " + str(geraldo.coletados) + "/3", True, (255, 220, 0))
    tela.blit(texto_energia, (10, TAMANHO * BLOCO + 5))
    tela.blit(texto_comp, (10, TAMANHO * BLOCO + 30))
    if msg != "":
        texto_msg = fonte.render(msg, True, (255, 140, 0))
        tela.blit(texto_msg, (200, TAMANHO * BLOCO + 18))
    pygame.display.flip()
pygame.quit()