# Fala pessoal da #404, beleza? Estamos nos anos 2000 e preciso de um apoio. O temido
‘Bug do Milênio’ corrompeu os sistemas da nossa grande oficina mecânica. O nosso robô
assistente, o Cyber-Geraldo, precisa navegar pelos setores de um galpão abandonado
para coletar componentes eletrônicos espalhados e levá-los até o Servidor Principal para
reiniciar o sistema. Se ele falhar, a oficina para e todos os dados de manutenção serão
apagados. Preciso que vocês projetem e programem o simulador dessa missão.

Eu estava refletindo sobre esse jogo e tem algumas coisas que não podem ficar de fora
de forma alguma. Tipo, se o usuário tentar passar do limite do mapa, ele tem de
permanecer no mesmo lugar e receber um aviso de alerta, algo tipo “Você bateu em uma
parede”. Outra coisa que pensei é que como temos vários componentes eletrônicos para
serem coletados, o jogador só será vencedor caso chegue ao local do servidor com pelo
menos 3 componentes coletados. Caso ele não atenda isso, ele deverá ser informado que
não possui componentes suficientes para realizar o reparo.

Além disso, temos de fazer um sistema similar ao de vidas, no caso serão pontos de
energia. O jogador irá iniciar com 3. Para cada vez que pisar em um Bug Corruptor (B),
ele irá perder 1 ponto de energia e aquele bug deve desaparecer da posição em que
estava. Falando em vidas, temos de falar de como irá funcionar o Game Over.
Basicamente, se os pontos de energia esgotarem, deverá ser informado a seguinte
mensagem: “Game Over! O Bug do Milênio corrompeu o Geraldo.”


Especificações Técnicas do Sistema
1. O Mapa do Galpão
 O ambiente do jogo deve ser representado por uma matriz de tamanho 5 x 5.
 O robô Cyber-Geraldo (P) sempre inicia sua jornada no canto superior
esquerdo.
 O Servidor Principal (S) está localizado na coordenada fixa [4][4] (Canto inferior
direito).
 Espalhados pelo mapa, devem existir obrigatoriamente 3 Componentes
Eletrônicos (C) e 3 Bugs Corruptores (B) em posições sorteadas pelo algoritmo.
Esses itens devem permanecer ocultos na tela, a ideia é que lembre um caça
ao tesouro misturado com campo minado.
 O jogo deverá funcionar em tempo real, ou seja, ao apertar uma tecla de
movimento a ação irá acontecer na tela.
2. Movimentação e Game Loop
O jogo deve rodar dentro de um laço contínuo (while) que só encerra em caso de
Vitória ou Game Over.
O sistema deve estar atento as entrada de teclado para mover o robô:
w ou UP (Seta pra cima) -&gt; Move para Cima
s ou DOWN (Seta para baixo) -&gt; Move para Baixo
a ou LEFT (Seta para esquerda) -&gt; Move para a Esquerda
d ou RIGHT (Seta para direita) -&gt; Move para a Direita

Instruções de Entrega
Para que a entrega seja validada e aceita pelo cliente, a equipe deve consolidar 3
arquivos distintos:

FASE 1: Documentação de Engenharia (Arquivo de Texto ou PDF)
Com base no briefing acima, listem formalmente:
 Requisitos Funcionais (RF): Todas as ações que o usuário ou o sistema devem
fazer (Dica: usem verbos no início, ex: RF01 – Permitir mover o personagem, RF02
– Atualizar o mapa na tela).
 Requisitos Não-Funcionais (RNF): As restrições e o ambiente de funcionamento do
sistema (ex: linguagem utilizada, tipo de interface).
 Regras de Negócio (RN): As travas de segurança e lógica do jogo extraídas do
texto.
FASE 2: Diagramas UML do Jogo
Utilizando a sintaxe padrão de formas geométricas:
 Desenhem o Diagrama de Atividades;
 Desenhem o Diagrama Comportamental;
 Desenhem o Diagrama Estruturado.
FASE 3: O Software Executável (Arquivo .py)
 O código deverá ser feito em Python, com uso da biblioteca Pygame. O uso de
funções, tratativa de erros e a realização de comentários é essencial. Vocês podem
desenvolver o jogo utilizando o POO (Programação Orientada a Objetos).


Instruções Extras:
Vocês atuarão como uma Software House autônoma durante esta semana. Eu estarei
simulando um cliente que viajou e aguarda a entrega do MVP (Produto Mínimo Viável)
funcional ao final do prazo. Vocês deverão criar um novo espaço de trabalho no JIRA e
um novo repositório no GitHub. Dessa forma vocês conseguirão se organizar e versionar
o código corretamente. Segue abaixo sugestão para separar as demandas:

 Dia 1: Leitura do escopo, extração de Requisitos, Regras de Negócio e desenho
dos diagramas.
 Dias 2 a 4: Desenvolvimento da estrutura lógica e do mapa do jogo em Python.
 Dia 5: Testes de mesa, tratamento de erros de digitação do usuário e envio do
projeto.

Formato: Mesmas equipes montadas anteriormente
Ambiente de Desenvolvimento: VS Code
Entrega: Arquivos de Documentação (PDF/Imagens) + Código-Fonte (.py)
Não aceitarei códigos de IA. Boa sorte!
