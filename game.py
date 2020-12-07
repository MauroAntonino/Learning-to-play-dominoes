import random
import numpy as np

class Game:
    def __init__(self):
        self.domino_set = [] #lista com a representação das peças no vetor de peças
        for i in range(0, 7):
            for j in range(i, 7):
                self.domino_set.append((i, j))

        """Inicializa o estado de forma aleatória"""
        self.player_hand = tuple(random.sample(self.domino_set, k=6))
        self.opponent_hand = tuple(random.sample([x for x in self.domino_set if x not in self.player_hand], k=6))
        self.boneyard = tuple([x for x in self.domino_set if x not in self.player_hand and x not in self.opponent_hand])
        self.current_number_left = -1
        self.current_number_right = -1

        self.state = (
            self.player_hand,
            self.opponent_hand,
            self.boneyard,
            self.current_number_left,
            self.current_number_right
        )

    def reset(self):
        """Função que reinicia os estados do jogo de forma aleatória para as próximas partidas"""
        
        self.player_hand = tuple(random.sample(self.domino_set, k=6))
        self.opponent_hand = tuple(random.sample([x for x in self.domino_set if x not in self.player_hand], k=6))
        self.boneyard = tuple([x for x in self.domino_set if x not in self.player_hand and x not in self.opponent_hand])
        self.current_number_left = -1
        self.current_number_right = -1

        self.state = (
            self.player_hand,
            self.opponent_hand,
            self.boneyard,
            self.current_number_left,
            self.current_number_right
        )

    def update_state(self, player_hand, opponent_hand, boneyard, current_number_left, current_number_right):
        """Função que padroniza a atualização do estado para que sempre ocorra após a realização de uma jogada"""
        
        self.player_hand = tuple(player_hand)
        self.opponent_hand = tuple(opponent_hand)
        self.boneyard = tuple(boneyard)
        self.current_number_left = current_number_left
        self.current_number_right = current_number_right

        self.state = (
            self.player_hand,
            self.opponent_hand,
            self.boneyard,
            self.current_number_left,
            self.current_number_right
        )
        return

    def play(self, hand, isPlayer, tile=None, number=None):
        #posicao é a peça, e jogador indica se é o adversário ou o próprio jogador
        """Funão que realiza a jogada"""

        if (tile, number) in self.possible_actions(hand) and number != None:
            new_hand = list(hand)
            new_hand.remove(tile)

            if number == self.current_number_left:
                current_number_right = self.current_number_right
                if tile[1] == number:
                    current_number_left = tile[0]
                else:
                    current_number_left = tile[1]
            else:
                current_number_left = self.current_number_left
                if tile[0] == number:
                    current_number_right = tile[1]
                else:
                   current_number_right = tile[0]
            if isPlayer:
                self.update_state(new_hand, self.state[1], self.boneyard, current_number_left, current_number_right)
            else:
                self.update_state(self.state[0], new_hand, self.boneyard, current_number_left, current_number_right)

        elif number == None and tile != None: #realiza a primeira jogada do jogo
            new_hand = list(hand)
            new_hand.remove(tile)
            current_number_left = tile[1]
            current_number_right = tile[0]

            if isPlayer:
                self.update_state(new_hand, self.state[1], self.boneyard, current_number_left, current_number_right)
            else:
                self.update_state(self.state[0], new_hand, self.boneyard, current_number_left, current_number_right)

            return
        elif len(self.boneyard) != 0: #faz o jogador comprar peças caso não consiga jogar
            new_tile = random.choice(self.boneyard)
            new_hand = list(hand)
            new_boneyard = list(self.boneyard)
            new_hand.append(new_tile)
            new_boneyard.remove(new_tile)
            
            if isPlayer:
                self.update_state(new_hand, self.state[1], new_boneyard, self.current_number_left, self.current_number_right)
            else:
                self.update_state(self.state[0], new_hand, new_boneyard, self.current_number_left, self.current_number_right)
        else:
            return 'passar vez'

    def game_status(self):
        """retorna se a partida acabou ou não"""
        if len(self.player_hand) == 0:
            return 'Won'
        elif len(self.opponent_hand) == 0:
            return 'Lost'
        elif (len(self.possible_actions(self.opponent_hand)) == 0) and (len(self.possible_actions(self.player_hand)) == 0) and (len(self.boneyard) == 0):
            #print(self.pecas_na_mao(self.boneyard))
            return 'Tie'
        else:
            return 'It is not over'

    def possible_actions(self, hand):
        """retorna um lista com as peças jogáveis e o respectivo lado da mesa"""
        #[(2,3),3]
        if self.current_number_right == -1 and self.current_number_left == -1:
            return [(x,None) for x in hand]
        possible_tiles = []
        for tile in hand:
            if self.current_number_left in tile:
                possible_tiles.append((tile, self.current_number_left))
            if self.current_number_right in tile:
                possible_tiles.append((tile, self.current_number_right))
        return possible_tiles