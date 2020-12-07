import random
import numpy as np

class jogo:
    
    def __init__(self):

        self.lista_peça = [] #lista com a representação das peças no vetor de peças
        for i in range(0,7):
            for j in range(i, 7):
                self.lista_peça.append((i,j))
        """Função que inicializa o estado de forma aleatória"""

        feature_pecas = [0]*16 + [1]*6 + [2]*6
        self.mao_adversario = []
        self.mao_jogador = [] #mao jogador sempre inicia
        self.cemiterio = []
        self.esquerda = -1
        self.direita = -1
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


        self.estado = (
        tuple(self.mao_adversario),
        tuple(self.mao_jogador),
        tuple(self.cemiterio),
        self.esquerda,
        self.direita
        )

        return

    def get_agente(self):
        return Agente()

    def reset(self):
        """Função que reinicia os estados do jogo de forma aleatória para as próximas partidas"""

        feature_pecas = [0]*16 + [1]*6 + [2]*6
        self.mao_adversario = []
        self.mao_jogador = [] #mao jogador sempre inicia
        self.cemiterio = []
        self.esquerda = -1
        self.direita = -1
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


        self.estado = (
        tuple(self.mao_adversario),
        tuple(self.mao_jogador),
        tuple(self.cemiterio),
        self.esquerda,
        self.direita
        )

    def atualizar_estado(self,parametros):
        """Função que padroniza a atualização do estado para que sempre ocorra após a realização de uma jogada"""
        
        self.mao_adversario = parametros[0]
        self.mao_jogador = parametros[1]
        self.cemiterio = parametros[2]
        self.esquerda = parametros[3]
        self.direita = parametros[4]

        
        self.estado = (
        self.mao_adversario,
        self.mao_jogador,
        self.cemiterio,
        self.esquerda,
        self.direita
        )
        return

    def realizar_jogada(self, mao, jogador, posicao=None, lado=None): #posicao é a peça, e jogador indica se é o adversário ou o próprio jogador
        """Funão que realiza a jogada"""

        if (posicao,lado) in self.acao_possível(mao) and lado != None:
            nova_mao = list(mao)
            nova_mao[posicao] = 0



            if self.lista_peça[posicao][1] == lado:
                if lado == self.esquerda:
                    esquerda = self.lista_peça[posicao][0]
                    direita = self.direita
                elif lado == self.direita:
                    direita = self.lista_peça[posicao][0]
                    esquerda = self.esquerda
                
            elif self.lista_peça[posicao][0] == lado:
                if lado == self.esquerda:
                    esquerda = self.lista_peça[posicao][1]
                    direita = self.direita
                elif lado == self.direita:
                    direita = self.lista_peça[posicao][1]
                    esquerda = self.esquerda

            cemiterio = self.cemiterio

            if jogador==1:
                self.atualizar_estado([tuple(nova_mao),self.estado[1],tuple(cemiterio),esquerda,direita])
            elif jogador==2:
                self.atualizar_estado([self.estado[0],tuple(nova_mao),tuple(cemiterio),esquerda,direita])

        elif lado == None and posicao != None: #realiza a a primeira jogada do jogo

            nova_mao = list(mao)
            nova_mao[posicao] = 0
            esquerda = self.lista_peça[posicao][1]
            direita = self.lista_peça[posicao][0]
            cemiterio = list(self.cemiterio)
            cemiterio[posicao] = 1

            
            if jogador==1:
                self.atualizar_estado([tuple(nova_mao),self.estado[1],tuple(cemiterio),esquerda,direita])
            elif jogador==2:
                self.atualizar_estado([self.estado[0],tuple(nova_mao),tuple(cemiterio),esquerda,direita])

            return
        elif len(self.pecas_na_mao(self.cemiterio)) != 0: #faz o jogador comprar peças caso não consiga jogar
            lista = []
            contador = 0
            for peca in self.cemiterio:
                if peca == 1:
                    lista.append(contador)
                contador += 1
            lista = random.sample(lista, k=len(lista))


            nova_mao = list(mao)
            nova_mao[lista[0]] = 1
            esquerda = self.esquerda
            direita = self.direita
            cemiterio = list(self.cemiterio)
            cemiterio[lista[0]] = 0

            
            if jogador==1:
                self.atualizar_estado([tuple(nova_mao),self.estado[1],tuple(cemiterio),esquerda,direita])
            elif jogador==2:
                self.atualizar_estado([self.estado[0],tuple(nova_mao),tuple(cemiterio),esquerda,direita])


            #mao[lista[0]] = 1
            #self.cemiterio[lista[0]] = 0
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

    def fim_de_jogo(self):
        """retorna se a partida acabou ou não"""
        if 1 not in self.mao_adversario:
            adversario = 'venceu'
            return adversario
        elif 1 not in self.mao_jogador:
            jogador = 'venceu2'
            return jogador
        elif (len(self.acao_possível(self.mao_jogador)) == 0) and (len(self.acao_possível(self.mao_adversario)) == 0) and (len(self.pecas_na_mao(self.cemiterio)) == 0):
            #print(self.pecas_na_mao(self.cemiterio))
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
        """retorna um lista com as peças jogávreis e o respectivo lado da mesa"""
        if self.direita == -1 and self.esquerda == -1:
            lista = []
            for peca in self.pecas_na_mao(mao):
                lista.append((peca,None))
            return lista
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

class Agente(jogo):
    def __init__(self):
        super().__init__()

        self.alpha = 0.0001
        self.epsilon = 0.03
        self.w = np.zeros((98, 1))


        #inicializar Q()? como um array ou como dicionário
        #como motar o erro td

    #retorna a funçã de valor
    def transforma_feature(self,estado):

        lista = np.zeros((98, 1))
        cont = 0
        for feature in estado:
            try:
                for thing in feature:
                    lista[cont] = thing
                    cont += 1
            except:
                lista[cont] = feature
                cont += 1

        return lista.T  #lista das 98 features

    def valor_estado(self, estado):

        if self.fim_de_jogo() != "não acabou":
            return 0
        else:
            estado = estado
            X = self.transforma_feature(estado)
            #self.w = np.add(self.w, np.arange(0, 0.5, 1/195))
            V = np.sum(np.dot(X,self.w)) #somar as peças de maior valor do preoduto do peso pela característica, fazendo o algoritmo buscar peças com maiores pesos

            return V

    def escolher_acao(self, mao,jogador):

        estado = self.estado
        acoes = self.acao_possível(mao)
        
        if np.random.uniform(0, 1) < self.epsilon and len(acoes) > 1:
            acao = random.sample(acoes,len(acoes))[0]
        else:
            lista_de_valores = []
            estado = self.estado
            for acao in acoes:
                #print(acao)
                self.realizar_jogada(mao = mao,jogador=jogador, posicao=acao[0], lado=acao[1])
                a,b,c,d,e = self.estado
                lista_de_valores.append(self.valor_estado(self.estado))
                #print(a,b,d,e)
                self.atualizar_estado([estado[0],estado[1],estado[2],estado[3],estado[4]])
            if len(lista_de_valores) != 0:
                acao  = max(lista_de_valores)
                acao = acoes[lista_de_valores.index(acao)]
            else:
                acao = [None,None]
            #print(lista_de_valores)
        self.estado =estado
        return acao, acoes

    def atualizar_funcao_valor(self, estado,jogador):

        estimativa = self.valor_estado(estado)
        if jogador == 1:
            mao = estado[0]
        else:
            mao = estado[1]

        b = self.escolher_acao(mao= mao, jogador = jogador)
        estado = self.estado
        self.realizar_jogada(mao = mao,jogador=jogador, posicao=b[0][0], lado=b[0][1])

        if self.fim_de_jogo() != "não acabou":
            self.atualizar_estado([estado[0],estado[1],estado[2],estado[3],estado[4]])
            self.estado =estado

            alvo = self.recompensa(jogador)
            delta = (alvo - estimativa)
            self.w += self.alpha*delta*self.transforma_feature(estado).T

        else:

            valor = self.valor_estado(self.estado)
            self.atualizar_estado([estado[0],estado[1],estado[2],estado[3],estado[4]])
            self.estado =estado

            alvo = self.recompensa(jogador) + valor
            delta = (alvo - estimativa)
            self.w += self.alpha*delta*self.transforma_feature(estado).T

        return

    def recompensa(self,jogador):
        #print(self.estado)
        fim_de_jogo = self.fim_de_jogo()
        #print("!!!"+fim_de_jogo)
        if fim_de_jogo == "venceu2" and jogador == 2:
            recompensa = 1
        elif fim_de_jogo == "venceu2" and jogador == 1:
            recompensa = -1
        if fim_de_jogo == "venceu" and jogador == 1:
            recompensa = 1
        elif fim_de_jogo == "venceu" and jogador == 2:
            recompensa = -1
        if fim_de_jogo == "empate":
            recompensa = 0
        if fim_de_jogo == "não acabou":
            recompensa = 0

        return recompensa


def jogada(jogador,agente):
    if jogador == 2:
        agente.epsilon = 1
        b = agente.escolher_acao(mao=a.estado[1],jogador=jogador)
        agente.epsilon = 0.03
        while b[0] == [None,None] and len(agente.pecas_na_mao(agente.cemiterio)) != 0:
            agente.realizar_jogada(mao=a.estado[1],posicao=b[0][0],lado=b[0][1],jogador=jogador)
            b = agente.escolher_acao(mao=a.estado[1],jogador=jogador)
        agente.realizar_jogada(mao=a.estado[1],posicao=b[0][0],lado=b[0][1],jogador=jogador)
        #agente.atualizar_funcao_valor(estado=a.estado,jogador = jogador)
    
    if jogador == 1:
        #agente.epsilon = 1
        c = agente.escolher_acao(mao=a.estado[0],jogador=jogador)
        #agente.episilon = 0.03
        while c[0] == [None,None] and len(agente.pecas_na_mao(agente.cemiterio)) != 0:
            agente.realizar_jogada(mao=a.estado[0],posicao=c[0][0],lado=c[0][1],jogador=jogador)
            c = agente.escolher_acao(mao=a.estado[0],jogador=jogador)
        #print(a.acao_possível(a.estado[0]),a.estado[0],a.estado[3],a.estado[4])
        agente.realizar_jogada(mao=a.estado[0],posicao=c[0][0],lado=c[0][1],jogador=jogador)
        agente.atualizar_funcao_valor(estado=a.estado,jogador = jogador)
    return



a = Agente()
cont = 0
vitorias_jogador_1 = 0
vitorias_jogador_2 = 0
jogos_por_cem = [0,0,0]
while cont < 500000:
    while a.fim_de_jogo() == "não acabou":
        #jogada(2,a)
        #a.atualizar_funcao_valor()
        jogada(1,a)
        jogada(2,a)
    #print(a.w)
    if "venceu" == a.fim_de_jogo():
        vitorias_jogador_1 +=1
        jogos_por_cem[0] += 1

    if "venceu2" == a.fim_de_jogo():
        vitorias_jogador_2 +=1
        jogos_por_cem[1] += 1
    #if "venceu2" == a.fim_de_jogo() or "venceu" == a.fim_de_jogo():
        #print(a.fim_de_jogo(),vitorias_jogador_1, vitorias_jogador_2)
    a.reset()
    cont += 1
    jogos_por_cem[2] += 1
    if cont%5000 == 0:
        print(vitorias_jogador_1/cont, vitorias_jogador_2/cont)
    if cont%5000 == 0:
        print(jogos_por_cem[0]/jogos_por_cem[2], jogos_por_cem[1]/jogos_por_cem[2],"%")
        jogos_por_cem = [0,0,0]

"""
agente líder com aprendizagem 0.54686-- agente secundário sem aprendizagem 0.343 -- 100.000 episódios 0.56401 0.334588
                                                                                                        0.58 0.336 %
"""