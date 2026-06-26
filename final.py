import pygame # importando a biblioteca que a gente vai usar pro jogo
import random # a gente precisa disso pra sortear onde as coisas vão cair

# iniciando o pygame pra tudo funcionar certinho
pygame.init()

# definindo o tamanho do nosso mapa (5x5 que o professor pediu)
TAMANHO = 5
# tamanho de cada quadradinho na tela (100 pixels)
BLOCO = 100
# calculando a largura e altura total da tela do jogo
LARGURA = TAMANHO * BLOCO
# a altura tem 90 pixels a mais pra caber a barrinha de texto embaixo (antes era 60 mas o game over tava cortando)
ALTURA = TAMANHO * BLOCO + 90

# criando a janela do jogo e dando um nome pra ela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cyber-Geraldo - Bug do Milênio")
# escolhendo a fonte pra escrever os textos depois
fonte = pygame.font.SysFont("arial", 20)

# isso aqui é pra controlar a velocidade do jogo (FPS)
clock = pygame.time.Clock()

# classe do nosso herói, a gente usou POO pra ficar mais organizado
class Geraldo:
    def __init__(self):
        # ele sempre começa lá em cima na esquerda
        self.lin = 0
        self.col = 0
        # as vidas dele
        self.energia = 3 
        # quantos componentes a gente já pegou
        self.coletados = 0
        
    # função pra movimentar o robozinho
    def mover(self, direcao):
        # se tentar ir pra cima e não tiver na borda, ele sobe
        if direcao == "cima" and self.lin > 0:
            self.lin -= 1
            return True
        # mesma coisa pra baixo
        elif direcao == "baixo" and self.lin < TAMANHO - 1:
            self.lin += 1
            return True
        # pra esquerda...
        elif direcao == "esquerda" and self.col > 0:
            self.col -= 1
            return True
        # pra direita...
        elif direcao == "direita" and self.col < TAMANHO - 1:
            self.col += 1
            return True
            
        # se bater na parede, retorna falso pro jogo avisar o jogador
        return False
        
    # reseta tudo pro inicio se o cara for jogar de novo
    def resetar(self):
        self.lin = 0
        self.col = 0
        self.energia = 3
        self.coletados = 0

# classe pra cuidar do mapa e esconder as coisas
class Mapa:
    def __init__(self):
        self.grade = [] # matriz do mapa
        self.visitados = [] # onde o Geraldo já pisou
        self.gerar() # cria o mapa na hora
        
    def gerar(self):
        # limpa tudo antes de criar
        self.grade = []
        self.visitados = []
        
        # cria a matriz 5x5 cheia de zero (vazio)
        for i in range(TAMANHO):
            linha = []
            for j in range(TAMANHO):
                linha.append(0) 
            self.grade.append(linha)
            
        # sorteando 3 componentes (tipo 2) e 3 bugs (tipo 1)
        self.sortear_itens(2, 3) 
        self.sortear_itens(1, 3) 
        
        # marca que o geraldo ja visitou o primeiro lugar senao fica escondido
        self.visitados.append([0, 0]) 
        
    # espalha os itens nos lugares vazios
    def sortear_itens(self, tipo, quantidade):
        colocados = 0
        # fica tentando ate colocar tudo
        while colocados < quantidade:
            lin = random.randint(0, TAMANHO - 1)
            col = random.randint(0, TAMANHO - 1)
            
            # so coloca se o lugar tiver vazio (0)
            if self.grade[lin][col] == 0:
                # nao pode colocar no inicio e nem onde fica o servidor
                if not (lin == 0 and col == 0) and not (lin == 4 and col == 4):
                    self.grade[lin][col] = tipo
                    colocados += 1
                    
    # olha se tem alguma coisa onde o geraldo pisou
    def checar(self, lin, col):
        valor = self.grade[lin][col]
        # se tiver um bug ou componente, a gente pega e apaga do mapa
        if valor != 0:
            self.grade[lin][col] = 0 
        
        # salva que o geraldo passou por aqui pra mostrar no mapa
        if [lin, col] not in self.visitados:
            self.visitados.append([lin, col])
            
        return valor # retorna o que ele achou pra gente tratar dps
        
    # funcao que diz se a gnt ja passou num quadrado ou nao
    def foi_visitada(self, lin, col):
        for pos in self.visitados:
            if pos[0] == lin and pos[1] == col:
                return True
        return False

# separei os desenhos pra ca senao o laço principal ia ficar mt feio
def desenhar_tela(geraldo, mapa, msg, ativo, resultado):
    # pinta a tela de preto pra limpar
    tela.fill((0, 0, 0)) 
    
    # desenhando o chao
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            
            # se ele ja passou, mostra um chao verde
            if mapa.foi_visitada(i, j):
                pygame.draw.rect(tela, (30, 50, 30), (x, y, BLOCO, BLOCO))
            else:
                # se nao, faz um xadrez cinza e bota uma interrogacao pros itens escondidos
                if (i + j) % 2 == 0:
                    pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
                else:
                    pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
                
                texto = fonte.render("?", True, (80, 80, 100))
                tela.blit(texto, (x + 43, y + 37))
                
            # desenha a bordinha de cada quadrado
            pygame.draw.rect(tela, (70, 70, 90), (x, y, BLOCO, BLOCO), 1)
            
    # desenha o servidor (S) roxo ali no final (4,4)
    sx = 4 * BLOCO
    sy = 4 * BLOCO
    pygame.draw.rect(tela, (130, 0, 200), (sx + 10, sy + 10, 80, 80))
    texto_servidor = fonte.render("S", True, (255, 255, 255))
    tela.blit(texto_servidor, (sx + 42, sy + 37))
    
    # desenha o nosso robo Geraldo (P) azulzinho
    gx = geraldo.col * BLOCO
    gy = geraldo.lin * BLOCO
    pygame.draw.rect(tela, (0, 130, 255), (gx + 10, gy + 10, 80, 80))
    texto_robo = fonte.render("P", True, (255, 255, 255))
    tela.blit(texto_robo, (gx + 40, gy + 37))
    
    # fazendo as linhas brancas do tabuleiro pra ficar mais visivel
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (100, 100, 120), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (100, 100, 120), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
        
    # fundo escuro pra nossa barra de avisos
    pygame.draw.rect(tela, (20, 20, 30), (0, TAMANHO * BLOCO, LARGURA, 90))
    
    # escreve a vida e as pecas dele
    texto_energia = fonte.render("Energia: " + str(geraldo.energia), True, (0, 200, 80))
    texto_comp = fonte.render("Componentes: " + str(geraldo.coletados) + "/3", True, (255, 220, 0))
    tela.blit(texto_energia, (10, TAMANHO * BLOCO + 5))
    tela.blit(texto_comp, (10, TAMANHO * BLOCO + 30))
    
    # ve se tem alguma mensagem pra mostrar
    if msg != "":
        # muda a cor da mensagem dependendo do que for
        if resultado == "ganhou":
            cor = (0, 255, 0) # verde
        elif resultado == "perdeu":
            cor = (255, 50, 50) # vermelho
        else:
            cor = (255, 140, 0) # laranjinha pros avisos normais
            
        texto_msg = fonte.render(msg, True, cor)
        # desci a mensagem pra terceira linha pra ela poder ocupar a tela toda
        tela.blit(texto_msg, (10, TAMANHO * BLOCO + 60))
        
    # se o jogo acabou, avisa que da pra dar restart
    if not ativo:
        texto_reinicio = fonte.render("Aperte R pra jogar de novo", True, (255, 255, 255))
        tela.blit(texto_reinicio, (130, 230))
        
    # isso aqui manda o pygame mostrar tudo na tela msm
    pygame.display.flip()

# criando o robo e o cenario
geraldo = Geraldo()
mapa = Mapa()
msg = ""
ativo = True
resultado = ""

# configurando as teclas. coloquei as setinhas e tbm W A S D
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

# coloquei esse try pra se der BO o codigo nao crashar feiao
try:
    rodando = True
    # loop principal que o professor pediu (while)
    while rodando:
        clock.tick(30) # pra nao ficar mega rapido rodando a 1000 fps
        
        # lendo os botões que o cara apertou
        for evento in pygame.event.get():
            # se apertou o X da janela a gnt quita do jogo
            if evento.type == pygame.QUIT:
                rodando = False
                
            # checando botoes do teclado
            if evento.type == pygame.KEYDOWN:
                # apertar R se quiser tentar dnv quando morre ou ganha
                if not ativo and evento.key == pygame.K_r:
                    geraldo.resetar()
                    mapa.gerar()
                    msg = ""
                    ativo = True
                    resultado = ""
                    
                # se ta jogando e apertou algum botao de andar
                if ativo and evento.key in teclas:
                    direcao = teclas[evento.key]
                    moveu = geraldo.mover(direcao)
                    
                    # se bater na parede, mostra esse aviso
                    if not moveu:
                        msg = "Você bateu em uma parede"
                    else:
                        # ve o que tem na casa q a gnt pisou
                        item = mapa.checar(geraldo.lin, geraldo.col)
                        msg = ""
                        
                        # se pegou o componente
                        if item == 2:
                            geraldo.coletados += 1
                            msg = "Componente coletado! (" + str(geraldo.coletados) + "/3)"
                        # se tomou dano pro bug
                        elif item == 1:
                            geraldo.energia -= 1
                            msg = "Bug Corruptor! Energia -1"
                            
                        # checando se tamo no servidor principal
                        if geraldo.lin == 4 and geraldo.col == 4:
                            # so ganha se tiver as 3 peças
                            if geraldo.coletados >= 3:
                                ativo = False
                                resultado = "ganhou"
                                msg = "Missao completa! Sistema reiniciado!"
                            else:
                                # senao o cara q continue procurando (ele nao perde aqui)
                                msg = "Você não possui componentes suficientes para realizar o reparo"
                                
                        # se acabarem as vidas
                        if geraldo.energia <= 0:
                            ativo = False
                            resultado = "perdeu"
                            msg = "Game over! O Bug do MiIênio corrompeu o Geraldo"
                            
        # desenha tudo dps que fizer a logica
        desenhar_tela(geraldo, mapa, msg, ativo, resultado)
        
except Exception as erro:
    # se o jogo der ruim mostra onde foi o erro no terminal pra gnt consertar
    print("Ocorreu um erro na execução do jogo:", erro)
finally:
    # fecha o pygame suave
    pygame.quit()
