import random

class jogo:
    
    def __init__(self):

        print("as peças seguem essa ordem")
        self.lista_peça = [] #lista com a representação das peças no vetor de peças
        for i in range(0,7):
            for j in range(i, 7):
                #print((i,j),end="")
                self.lista_peça.append((i,j))


        feature_pecas = [0]*16 + [1]*6 + [2]*6
        self.mao_adversario = []
        self.mao_jogador = [] #mao jogador sempre inicia
        self.cemiterio = []
        self.esquerda = None
        self.direita = None
        pecas = random.sample(feature_pecas, k=len(feature_pecas))#retorna uma lista de peças em ordem aleatória

        for peca in pecas:
            if peca == 0:
                self.mao_adversario.append(0)
                self.mao_jogador.append(0)
                self.cemiterio.append(1)

            if peca == 1:
                self.mao_adversario.append(0)
                self.mao_jogador.append(1)
                self.cemiterio.append(0)
                    
            if peca == 2:
                self.mao_adversario.append(1)
                self.mao_jogador.append(0)
                self.cemiterio.append(0)


        self.estado = [
        self.mao_adversario,
        self.mao_jogador,
        self.cemiterio,
        self.esquerda,
        self.direita
        ]

        """
        Código para iniciar com uma carroça

        for peca in self.lista_carroca(): #range(28,-1,-1):
            if self.mao_jogador[peca] == 1:

                self.esquerda = self.lista_peça[peca][0]
                self.direita = self.lista_peça[peca][1]
                self.mao_jogador[peca] = 0

            if self.mao_adversario[peca] == 1:

                self.esquerda = self.lista_peça[peca][0]
                self.direita = self.lista_peça[peca][1]
                self.mao_adversario[peca] = 0

        """
        #print(self.estado)
        #self.realizar_jogada()
        return


    def realizar_jogada(self, jogador, posicao=None, lado=None): #posicao é a peça, e jogador indica se é o adversário ou o próprio jogador

        if (posicao,lado) in self.acao_possível(jogador):
            jogador[posicao] = 0
            #print(self.lista_peça[posicao])
            if self.lista_peça[posicao][1] == lado:
                if lado == self.esquerda:
                    self.esquerda = self.lista_peça[posicao][0]
                elif lado == self.direita:
                    self.direita = self.lista_peça[posicao][0]
                
            elif self.lista_peça[posicao][0] == lado:
                if lado == self.esquerda:
                    self.esquerda = self.lista_peça[posicao][1]
                elif lado == self.direita:
                    self.direita = self.lista_peça[posicao][1]
        elif lado == None and posicao != None:
            jogador[posicao] = 0
            self.esquerda = self.lista_peça[posicao][1]
            self.direita = self.lista_peça[posicao][0]
            return
        elif len(self.pecas_na_mao(self.cemiterio)) != 0:
            lista = []
            contador = 0
            for peca in self.cemiterio:
                if peca == 1:
                    lista.append(contador)
                contador += 1
            lista = random.sample(lista, k=len(lista))
            jogador[lista[0]] = 1
            self.cemiterio[lista[0]] = 0
        else:
            return 'passar vez'

    def pecas_na_mao(self,mao): # quantidade de peças
            lista = []
            contador = 0
            for peca in mao:
                if peca == 1:
                    lista.append(contador)
                contador += 1
            return lista

    def fim_de_joog(self):
        """retorna se a partida acabou ou não"""
        if 1 not in self.mao_jogador:
            jogador = 'venceu'
            return jogador
        elif 1 not in self.mao_adversario:
            adversario = 'venceu2'
            return adversario
        elif (len(self.acao_possível(self.mao_jogador)) == 0) and (len(self.acao_possível(self.mao_adversario)) == 0) and (len(self.pecas_na_mao(self.cemiterio)) == 0):
            print(self.pecas_na_mao(self.cemiterio))
            return 'empate'
        else:
            return 'não acabou'

    def lista_carroca(self):

        lista = []
        k = 0
        for i in range(0,28):
            k+=(i+1)
            if k < 29:
                lista.append((28-k))
        return str(lista)

    def acao_possível(self, mao):
        lista = []
        cont = 0
        for peca in mao:

            if (peca == 1) and ((self.lista_peça[cont][1] == self.esquerda)):
                lista.append((cont,self.esquerda))
            if (peca == 1) and ((self.lista_peça[cont][0] == self.esquerda)):
                lista.append((cont,self.esquerda))
            if (peca == 1) and ((self.lista_peça[cont][0] == self.direita)):
                lista.append((cont,self.direita))
            if (peca == 1) and ((self.lista_peça[cont][1] == self.direita)):
                lista.append((cont,self.direita))
            cont += 1
        return lista


a = jogo()

lst = a.pecas_na_mao(a.mao_jogador)
lst2 = a.pecas_na_mao(a.mao_adversario)
print(lst ,lst2)
print(str(a.acao_possível(a.mao_jogador)))
a.realizar_jogada( posicao=lst[0], jogador=a.mao_jogador, lado=None)
"""
print(a.esquerda,a.direita)
print(a.lista_carroca())
lst = a.pecas_na_mao(a.mao_jogador)
print(lst)
print(str(a.acao_possível(a.mao_jogador)))

try:
    peca, lado = a.acao_possível(a.mao_jogador)[0]
    if a.esquerda == lado:
        a.realizar_jogada( posicao=peca, jogador=a.mao_jogador, lado=a.esquerda)
    else:
        a.realizar_jogada( posicao=peca, jogador=a.mao_jogador, lado=a.direita)
except:
    a.realizar_jogada(jogador=a.mao_jogador)
print(a.esquerda,a.direita)
"""
while a.fim_de_joog() == "não acabou":
    print(a.acao_possível(a.mao_adversario))
    print(a.pecas_na_mao(a.mao_adversario))
    print(a.esquerda, a.direita)
    try:
        peca, lado = a.acao_possível(a.mao_adversario)[0]
        if a.esquerda == lado:
            a.realizar_jogada( posicao=peca, jogador=a.mao_adversario, lado=a.esquerda)
        else:
            a.realizar_jogada( posicao=peca, jogador=a.mao_adversario, lado=a.direita)
    except:
        a.realizar_jogada(jogador=a.mao_adversario)
    if a.fim_de_joog() != "não acabou":
        print("")
    else:
        print(a.acao_possível(a.mao_jogador))
        print(a.pecas_na_mao(a.mao_jogador))
        print(a.esquerda, a.direita)
        try:
            peca, lado = a.acao_possível(a.mao_jogador)[0]
            if a.esquerda == lado:
                a.realizar_jogada( posicao=peca, jogador=a.mao_jogador, lado=a.esquerda)
            else:
                a.realizar_jogada( posicao=peca, jogador=a.mao_jogador, lado=a.direita)
        except:
            a.realizar_jogada(jogador=a.mao_jogador)
print(str(a.fim_de_joog()))
"""
print(a.mao_jogador)
print(a.mao_adversario)
print(a.cemiterio)
"""