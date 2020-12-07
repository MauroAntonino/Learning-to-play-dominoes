import random
import numpy as np
from game import Game

class Agent(Game):
    def __init__(self):
        super().__init__()
        self.alpha = 0.0001
        self.epsilon = 0.03
        self.w = np.zeros((98, 1))

        #inicializar Q()? como um array ou como dicionário
        #como motar o erro td

    #retorna a função de valor
    def transforma_feature(self, state):
        lista = np.zeros((98, 1))
        count = 0

        for feature in state:
            if type(feature) == tuple:
                for tile in self.domino_set:
                    if tile in feature:
                        lista[count] = 1
                    else:
                        lista[count] = 0
            else:
                lista[count] = feature
            count+=1
        return lista.T  #lista das 98 features

    def valor_estado(self, state):
        if self.game_status() != "It is not over":
            return 0
        else:
            state = state
            X = self.transforma_feature(state)
            #self.w = np.add(self.w, np.arange(0, 0.5, 1/195))
            V = np.sum(np.dot(X, self.w)) #somar as peças de maior valor do preoduto do peso pela característica, fazendo o algoritmo buscar peças com maiores pesos
            return V

    def choose_action(self, hand, isPlayer):
        state = self.state
        actions = self.possible_actions(hand)
        
        if np.random.uniform(0, 1) < self.epsilon and len(actions) > 1:
            action = random.sample(actions, len(actions))[0]
        else:
            value_list = []
            state = self.state
            for action in actions:
                self.play(hand, isPlayer, action[0], action[1])
                value_list.append(self.valor_estado(self.state))
                self.update_state(state[0], state[1], state[2], state[3], state[4])
            if len(value_list) != 0:
                action = actions[value_list.index(max(value_list))]
            else:
                action = [None, None]
        self.state = state
        return action, actions

    def atualizar_funcao_valor(self, estado, isPlayer):
        estimativa = self.valor_estado(estado)
        if isPlayer:
            hand = estado[0]
        else:
           hand = estado[1]

        b = self.choose_action(hand, isPlayer)
        estado = self.state
        self.play(hand, isPlayer, b[0][0], b[0][1])

        if self.game_status() != "It is not over":
            self.update_state(estado[0], estado[1], estado[2], estado[3], estado[4])
            self.state = estado

            alvo = self.reward(isPlayer)
            delta = (alvo - estimativa)
            self.w += self.alpha * delta * self.transforma_feature(estado).T
        else:
            valor = self.valor_estado(self.state)
            self.update_state(estado[0], estado[1], estado[2], estado[3], estado[4])
            self.state = estado

            alvo = self.reward(isPlayer) + valor
            delta = (alvo - estimativa)
            self.w += self.alpha * delta * self.transforma_feature(estado).T
        return

    def reward(self, isPlayer):
        game_status = self.game_status()
        if (game_status == "Won" and isPlayer) or (game_status == 'Lost' and not isPlayer):
            reward = 1
        elif (game_status == 'Won' and not isPlayer) or (game_status == 'Lost' and isPlayer):
            reward = -1
        else:
            reward = 0
        return reward