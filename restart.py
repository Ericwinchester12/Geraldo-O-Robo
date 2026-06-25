import pygame
import random
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
   # reinicia os status do robo para começar outra partida
   def resetar(self):
       self.lin = 0
       self.col = 0
       self.energia = 3
       self.coletados = 0
class Mapa:
   def __init__(self):
       self.grade = []
       self.visitados = [] # salva as casas que ja foram descobertas
       self.gerar()
   def gerar(self):
       self.grade = []
       self.visitados = []
       for i in range(TAMANHO):
           linha = []
           for j in range(TAMANHO):
               linha.append(0)
           self.grade.append(linha)
       self.sortear_itens(2, 3)
       self.sortear_itens(1, 3)
       # marca a posicao inicial como ja visitada
       self.visitados.append([0, 0])
   def sortear_itens(self, tipo, quantidade):
       colocados = 0
       while colocados < quantidade:
           lin = random.randint(0, TAMANHO - 1)
           col = random.randint(0, TAMANHO - 1)
           if self.grade[lin][col] == 0:
               if not (lin == 0 and col == 0) and not (lin == 4 and col == 4):
                   self.grade[lin][col] = tipo
                   colocados += 1
   def checar(self, lin, col):
       valor = self.grade[lin][col]
       if valor != 0:
           self.grade[lin][col] = 0
      
       # se ainda nao passou por aqui, salva na lista de visitados
       if [lin, col] not in self.visitados:
           self.visitados.append([lin, col])
       return valor
   # confere se a casa ja esta na lista
   def foi_visitada(self, lin, col):
       for pos in self.visitados:
           if pos[0] == lin and pos[1] == col:
               return True
       return False
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
ativo = True
resultado = ""
try:
   rodando = True
   while rodando:
       clock.tick(30)
       for evento in pygame.event.get():
           if evento.type == pygame.QUIT:
               rodando = False
           if evento.type == pygame.KEYDOWN:
               # se o jogo acabou, permite reiniciar apertando R
               if not ativo and evento.key == pygame.K_r:
                   geraldo.resetar()
                   mapa.gerar()     
                   msg = ""
                   ativo = True
                   resultado = ""
               if ativo and evento.key in teclas:
                   direcao = teclas[evento.key]
                   moveu = geraldo.mover(direcao)
                   if not moveu:
                       msg = "Você bateu em uma parede"
                   else:
                       item = mapa.checar(geraldo.lin, geraldo.col)
                       msg = ""
                       if item == 2:
                           geraldo.coletados += 1
                           msg = "Componente coletado! (" + str(geraldo.coletados) + "/3)"
                       elif item == 1:
                           geraldo.energia -= 1
                           msg = "Bug Corruptor! Energia -1"
                       if geraldo.lin == 4 and geraldo.col == 4:
                           if geraldo.coletados >= 3:
                               ativo = False
                               resultado = "ganhou"
                               msg = "Missao completa! Sistema reiniciado!"
                           else:
                               msg = "Componentes insuficientes para o reparo!"
                       if geraldo.energia <= 0:
                           ativo = False
                           resultado = "perdeu"
                           msg = "Game Over! O Bug do Milênio corrompeu o Geraldo."
       tela.fill((0, 0, 0))
       for i in range(TAMANHO):
           for j in range(TAMANHO):
               x = j * BLOCO
               y = i * BLOCO
               # muda a cor do quadrado se o jogador ja tiver passado por ele
               if mapa.foi_visitada(i, j):
                   pygame.draw.rect(tela, (30, 50, 30), (x, y, BLOCO, BLOCO))
               else:
                   if (i + j) % 2 == 0:
                       pygame.draw.rect(tela, (35, 35, 50), (x, y, BLOCO, BLOCO))
                   else:
                       pygame.draw.rect(tela, (50, 50, 65), (x, y, BLOCO, BLOCO))
                  
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
           if resultado == "ganhou":
               cor = (0, 255, 0)
           elif resultado == "perdeu":
               cor = (255, 50, 50)
           else:
               cor = (255, 140, 0)
           texto_msg = fonte.render(msg, True, cor)
           tela.blit(texto_msg, (200, TAMANHO * BLOCO + 18))
       # mostra a opção de reiniciar
       if not ativo:
           texto_reinicio = fonte.render("Aperte R pra jogar de novo", True, (255, 255, 255))
           tela.blit(texto_reinicio, (130, 230))
       pygame.display.flip()
except Exception as erro:
   print("Ocorreu um erro na execução:", erro)
finally:
   pygame.quit()
