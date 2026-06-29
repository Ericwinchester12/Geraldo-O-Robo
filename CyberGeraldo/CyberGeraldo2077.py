import pygame
import random # a gente precisa disso pra sortear onde as coisas vão cair aleatoriamente no mapa

# --- INICIANDO AS PARADAS ---
# dando a partida no motor do pygame
pygame.init()

# definindo o tamanho do mapa (vai ser uma matriz 5x5)
TAMANHO = 5
# tamanho de cada quadradinho na tela (100x100 pixels)
BLOCO = 100
# calculando a largura total da tela (5 * 100 = 500 pixels)
LARGURA = TAMANHO * BLOCO
# a altura tem 90 pixels a mais pra caber os textos de vida e itens embaixo
ALTURA = TAMANHO * BLOCO + 90

# criando a janela do jogo de fato e dando um nome pra ela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CyberGeraldo2077")

# escolhendo a fonte e o tamanho pra escrever os textos depois na tela
fonte = pygame.font.SysFont("arial", 20)

# isso aqui é um relógio do pygame pra controlar a velocidade do jogo (os FPS)
clock = pygame.time.Clock()

# --- CARREGANDO AS IMAGENS ---
# nome dos arquivos das imagens que tao na mesma pasta do codigo
NOME_SPRITE_GERALDO = "sprite trabalho cybergeraldo.png"
NOME_SPRITE_SERVIDOR = "Servidor Arasaka.jpeg"

try:
    # tenta carregar a imagem do geraldo ja com o fundo transparente (png)
    sprite_geraldo_original = pygame.image.load(NOME_SPRITE_GERALDO).convert_alpha()
    # arranca o fundo branco da imagem
    sprite_geraldo_original.set_colorkey((255, 255, 255))
    # da um resize pra caber no nosso quadrado de 100x100 (deixei 80x80 pra ter uma bordinha)
    sprite_geraldo = pygame.transform.scale(sprite_geraldo_original, (80, 80))
except Exception as e:
    # se a imagem nao carregar ou der BO, a gente faz um quadrado ciano no lugar pra nao crashar o jogo
    print(f"Erro ao carregar o sprite do Geraldo: {e}")
    sprite_geraldo = pygame.Surface((80, 80))
    sprite_geraldo.fill((0, 255, 255))

try:
    # tenta carregar a imagem do servidor arasaka e ajusta pro tamanho 80x80 tbm
    sprite_servidor_original = pygame.image.load(NOME_SPRITE_SERVIDOR).convert_alpha()
    sprite_servidor = pygame.transform.scale(sprite_servidor_original, (80, 80))
except Exception as e:
    # se der BO, faz um quadrado amarelo
    print(f"Erro ao carregar o sprite do Servidor: {e}")
    sprite_servidor = pygame.Surface((80, 80))
    sprite_servidor.fill((255, 255, 0))


# --- CLASSES DO JOGO ---

# classe do geraldo (nosso personagem)
class Geraldo:
    # o def __init__ é onde o geraldo "nasce". aqui ficam os status iniciais dele
    def __init__(self):
        # ele sempre começa na linha 0, coluna 0 (lá em cima na esquerda)
        self.lin = 0
        self.col = 0
        # começa com 3 vidas (energia)
        self.energia = 3 
        # começa com 0 componentes na mochila
        self.coletados = 0
        
    # função pra movimentar o robozinho no mapa
    def mover(self, direcao):
        # a logica aqui é: se apertou pra cima, e ele nao tiver batendo no teto (lin > 0), ele sobe (-1 na linha)
        if direcao == "cima" and self.lin > 0:
            self.lin -= 1
            return True
        # se for pra baixo e nao bater no limite da tela (TAMANHO - 1), ele desce (+1 na linha)
        elif direcao == "baixo" and self.lin < TAMANHO - 1:
            self.lin += 1
            return True
        # mesma logica pra ir pra esquerda (-1 na coluna)
        elif direcao == "esquerda" and self.col > 0:
            self.col -= 1
            return True
        # mesma logica pra ir pra direita (+1 na coluna)
        elif direcao == "direita" and self.col < TAMANHO - 1:
            self.col += 1
            return True
            
        # se nenhuma dessas der certo, é pq ele bateu na parede. ai retorna falso.
        return False
        
    # volta os status do geraldo pro inicio quando a gente reinicia a fase
    def resetar(self):
        self.lin = 0
        self.col = 0
        self.energia = 3
        self.coletados = 0


# classe que cuida de criar a matriz e esconder as paradas nela
class Mapa:
    def __init__(self):
        self.grade = [] # matriz principal do mapa (as linhas e colunas)
        self.visitados = [] # lista pra gravar onde o Geraldo já pisou
        self.gerar() # chama a função de gerar o mapa na mesma hora
        
    def gerar(self):
        # zera a matriz e os lugares visitados (bom pra quando der restart no jogo)
        self.grade = []
        self.visitados = []
        
        # cria a matriz 5x5 cheia de zero (0 = quadrado vazio)
        for i in range(TAMANHO):
            linha = []
            for j in range(TAMANHO):
                linha.append(0) 
            self.grade.append(linha)
            
        # sorteia 3 componentes (representados pelo numero 2) e 3 bugs (representados pelo numero 1)
        self.sortear_itens(2, 3) 
        self.sortear_itens(1, 3) 
        
        # ja marca que o geraldo visitou o [0, 0] senao o chao de inicio fica escuro
        self.visitados.append([0, 0]) 
        
    # pega os itens e joga em lugares aleatorios da matriz
    def sortear_itens(self, tipo, quantidade):
        colocados = 0
        # fica num loop infinito ate conseguir plantar todos os itens
        while colocados < quantidade:
            lin = random.randint(0, TAMANHO - 1) # sorteia uma linha
            col = random.randint(0, TAMANHO - 1) # sorteia uma coluna
            
            # so deixa colocar o item la se o espaço for 0 (vazio)
            if self.grade[lin][col] == 0:
                # bloqueia pra nao nascer item em cima de onde a gnt começa (0,0) nem onde ta o servidor (4,4)
                if not (lin == 0 and col == 0) and not (lin == 4 and col == 4):
                    self.grade[lin][col] = tipo
                    colocados += 1 # marca que plantou um item
                    
    # olha o que tem no chao toda vez que o geraldo pisa num quadrado novo
    def checar(self, lin, col):
        valor = self.grade[lin][col]
        # se não for 0 (vazio), quer dizer que achou um item/bug. ai a gente pega e troca pra 0 pra ele sumir do mapa.
        if valor != 0:
            self.grade[lin][col] = 0 
        
        # guarda nas coordenadas que a gnt ja passou por ali pra desenhar o chao roxo dps
        if [lin, col] not in self.visitados:
            self.visitados.append([lin, col])
            
        return valor # joga o que ele achou (0, 1 ou 2) la pro loop principal resolver
        
    # so ve se a coordenada atual ta na nossa lista de lugares que a gente ja passou
    def foi_visitada(self, lin, col):
        for pos in self.visitados:
            if pos[0] == lin and pos[1] == col:
                return True
        return False


# --- DESENHO DA TELA ---
# separei os desenhos pra ca senao o loop principal lá embaixo ia ficar muito poluido
def desenhar_tela(geraldo, mapa, msg, ativo, resultado):
    # pinta a tela inteira de preto pra limpar o quadro anterior
    tela.fill((0, 0, 0)) 
    
    # desenhando o chao
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            x = j * BLOCO
            y = i * BLOCO
            
            # se for uma area que a gnt ja pisou, pinta o fundo de roxo neon
            if mapa.foi_visitada(i, j):
                pygame.draw.rect(tela, (45, 10, 55), (x, y, BLOCO, BLOCO))
            else:
                # se nao pisou ainda, faz um xadrez de cinza escuro usando matematica basica de par/impar
                if (i + j) % 2 == 0:
                    pygame.draw.rect(tela, (15, 15, 20), (x, y, BLOCO, BLOCO))
                else:
                    pygame.draw.rect(tela, (25, 30, 40), (x, y, BLOCO, BLOCO))
                
                # desenha a interrogacao de lugar desconhecido (rosa neon)
                texto = fonte.render("?", True, (255, 0, 255))
                tela.blit(texto, (x + 43, y + 37))
                
            # desenha a bordinha de cada quadrado (ciano neon)
            pygame.draw.rect(tela, (0, 255, 255), (x, y, BLOCO, BLOCO), 1)
            
    # desenha o servidor arasaka la na saida do mapa (linha 4, coluna 4)
    sx = 4 * BLOCO
    sy = 4 * BLOCO
    tela.blit(sprite_servidor, (sx + 10, sy + 10))
    
    # desenha o sprite do Geraldo em cima de onde ele ta na matriz
    gx = geraldo.col * BLOCO
    gy = geraldo.lin * BLOCO
    tela.blit(sprite_geraldo, (gx + 10, gy + 10))
    
    # faz as linhas da grade virarem roxo neon pra dar o estilo cyberpunk
    for i in range(TAMANHO + 1):
        pygame.draw.line(tela, (148, 0, 211), (0, i * BLOCO), (LARGURA, i * BLOCO))
        pygame.draw.line(tela, (148, 0, 211), (i * BLOCO, 0), (i * BLOCO, TAMANHO * BLOCO))
        
    # pinta a area de baixo (onde fica os textos) com um fundo bem escuro
    pygame.draw.rect(tela, (5, 5, 15), (0, TAMANHO * BLOCO, LARGURA, 90))
    
    # cria os textos de vida e peças do inventario
    texto_energia = fonte.render("Energia: " + str(geraldo.energia), True, (0, 255, 255))
    texto_comp = fonte.render("Componentes: " + str(geraldo.coletados) + "/3", True, (255, 255, 0))
    # e bota eles na tela (o .blit cola a imagem na tela)
    tela.blit(texto_energia, (10, TAMANHO * BLOCO + 5))
    tela.blit(texto_comp, (10, TAMANHO * BLOCO + 30))
    
    # logica pra mostrar os avisos (bateu na parede, achou item, etc)
    if msg != "":
        # muda a cor da letra dependendo de como a gente ta no jogo
        if resultado == "ganhou":
            cor = (57, 255, 20) # verde pro vitoria
        elif resultado == "perdeu":
            cor = (255, 0, 128) # rosa pro game over
        else:
            cor = (0, 255, 255) # ciano pras msgs normais
            
        texto_msg = fonte.render(msg, True, cor)
        tela.blit(texto_msg, (10, TAMANHO * BLOCO + 60))
        
    # se alguem ganhou ou morreu (ativo == False), mostra o aviso pra reiniciar
    if not ativo:
        texto_reinicio = fonte.render("Aperte R pra jogar de novo", True, (255, 255, 0))
        tela.blit(texto_reinicio, (130, 230))
        
    # isso aqui diz pro pygame atualizar a tela de fato com todos esses desenhos que a gnt programou
    pygame.display.flip()


# --- START DO JOGO ---
# aqui a gente cria (instancia) tudo pra valer
geraldo = Geraldo()
mapa = Mapa()
msg = ""
ativo = True # variavel que diz se a gnt ta jogando ou se ja deu game over/vitoria
resultado = ""

# montei um dicionario conectando as teclas de movimento nas direcoes pra nao precisar fazer mil IFs
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

# coloquei esse try grandão pra se rolar algum crash, ele fechar direito e mostrar o erro
try:
    rodando = True
    # LOOP PRINCIPAL: fica repetindo isso aqui enquanto o jogo ta aberto
    while rodando:
        clock.tick(30) # trava o jogo a 30 fps pro boneco nao voar pelo mapa parecendo o flash
        
        # captura todos os botões que o cara apertar no teclado
        for evento in pygame.event.get():
            # se apertou no X de fechar a aba
            if evento.type == pygame.QUIT:
                rodando = False
                
            # se ele apertar (descer) alguma tecla
            if evento.type == pygame.KEYDOWN:
                # se o jogo acabou e ele apertar R, reinicia tudo do zero
                if not ativo and evento.key == pygame.K_r:
                    geraldo.resetar()
                    mapa.gerar()
                    msg = ""
                    ativo = True
                    resultado = ""
                    
                # se ta jogando e apertou um dos botoes de andar (que tao la no dicionario)
                if ativo and evento.key in teclas:
                    direcao = teclas[evento.key]
                    moveu = geraldo.mover(direcao) # manda o geraldo andar
                    
                    # se bater na borda da tela (o mover retornou falso)
                    if not moveu:
                        msg = "Você bateu em uma parede"
                    else:
                        # ve o que tem na casa q a gnt pisou usando aquela def do mapa
                        item = mapa.checar(geraldo.lin, geraldo.col)
                        msg = ""
                        
                        # se o retorno foi 2 (componente)
                        if item == 2:
                            geraldo.coletados += 1
                            msg = "Componente coletado! (" + str(geraldo.coletados) + "/3)"
                        # se o retorno foi 1 (bug)
                        elif item == 1:
                            geraldo.energia -= 1
                            msg = "Bug Corruptor! Energia -1"
                            
                        # logica final: checa se chegamis no Servidor (linha 4, coluna 4)
                        if geraldo.lin == 4 and geraldo.col == 4:
                            # so ganha se ja pegou as 3 peças
                            if geraldo.coletados >= 3:
                                ativo = False # trava o jogo
                                resultado = "ganhou"
                                msg = "Missao completa! Sistema reiniciado!"
                            else:
                                # se nao, manda aviso mas deixa ele continuar jogando
                                msg = "Você não possui componentes suficientes para realizar o reparo"
                                
                        # se a vida bater zero ou menos, morre
                        if geraldo.energia <= 0:
                            ativo = False # trava o jogo
                            resultado = "perdeu"
                            msg = "Game over! O Bug do MiIênio corrompeu o Geraldo"
                            
        # depois de ver toda a logica, os botoes, a vida... a gente manda desenhar a tela
        desenhar_tela(geraldo, mapa, msg, ativo, resultado)
        
except Exception as erro:
    # se o loop der pau, a gnt printa no terminal pra investigar o erro (ajuda muito a achar o erro rapido)
    print("Ocorreu um erro na execução do jogo:", erro)
finally:
    # dps que fecha a janela (sai do while), quita do pygame pra fechar o processo limpo
    pygame.quit()
