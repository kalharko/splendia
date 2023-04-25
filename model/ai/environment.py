import gymnasium as gym
from model.game_manager import GameManager
import numpy as numpy
from model.checker import Checker
from model.token_array import TokenArray


class SplendorEnv(gym.Env):
    def __init__(self,nb_player=2):
        self.action_space = gym.spaces.Discrete(45)
        """
        Player 1 state:
        5 tokens: 0-4
        1 gold token: 5
        20 player cards: 6-25
        5 noble cards: 26-30
        3 reserved cards: 31-33
        
        Player 2 state:
        5 tokens: 34-38
        1 gold token: 39
        20 player cards: 40-59
        5 noble cards: 60-64
        3 reserved cards: 65-67
        
        Shop state:
        12 cards: 68-79
        5 noble cards: 80-84
        1 tier 1 number of cards: 85
        1 tier 2 number of cards: 86
        1 tier 3 number of cards: 87
    
        """
        self.observation_space = gym.spaces.MultiDiscrete(
            [8, 8, 8, 8, 8, 6, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91,
             91, 91, 91, 91, 91, 11, 11, 11, 11, 11, 91, 91, 91, 8, 8, 8, 8, 8, 6, 91, 91, 91, 91, 91, 91, 91, 91, 91,
             91, 91, 91, 91, 91, 91,
             91, 91, 91, 91, 91, 11, 11, 11, 11, 11, 92, 92, 92, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 11, 11,
             11, 11, 11, 40, 30, 20])

        self.game = GameManager(nbPlayer=nb_player)
        self.game.launch_game(nbPlayer=2)

        self.from_board_states_to_obs()
        pass

    def from_board_states_to_obs(self):
        state = self.game.gather_ia_board_state()
        obs = numpy.zeros(88)
        obs[0:6] = state['player1']['tokens']
        # if the length of the list smaller than 20, we padd with 90
        list_of_cards = [card.card_id for card in state['player1']['cards']]
        if len(list_of_cards) < 20:
            for i in range(20-len(list_of_cards)):
                list_of_cards.append(90)

        obs[6:26] = list_of_cards
        # same for nobles, if the length of the list smaller than 5, we padd with 10
        list_of_nobles = [patron.patron_id for patron in state['player1']['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5-len(list_of_nobles)):
                list_of_nobles.append(10)


        obs[26:31] = list_of_nobles

        self.reserved_cards = [card.card_id for card in state['player1']['reserved']]
        # same for reserved cards, if the length of the list smaller than 3, we padd with 90
        list_of_reserved = [card.card_id for card in state['player1']['reserved']]
        if len(list_of_reserved) < 3:
            for i in range(3-len(list_of_reserved)):
                list_of_reserved.append(90)
        obs[31:34] =  list_of_reserved

        obs[34:40] = state['player2']['tokens']
        # same for player 2
        list_of_cards = [card.card_id for card in state['player2']['cards']]
        if len(list_of_cards) < 20:
            for i in range(20 - len(list_of_cards)):
                list_of_cards.append(90)

        obs[40:60] = list_of_cards
        list_of_nobles = [patron.patron_id for patron in state['player2']['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5 - len(list_of_nobles)):
                list_of_nobles.append(10)
        obs[60:65] = list_of_nobles
        list_of_reserved = [card.card_id for card in state['player2']['reserved']]
        if len(list_of_reserved) < 3:
            for i in range(3 - len(list_of_reserved)):
                list_of_reserved.append(90)

        obs[65:68] = list_of_reserved

        # same for shop
        self.shop1_cards = state['shop']['rank1_cards']
        list_of_cards_rank1 = [card.card_id for card in state['shop']['rank1_cards']]

        if len(list_of_cards_rank1) < 4:
            for i in range(4 - len(list_of_cards_rank1)):
                list_of_cards_rank1.append(90)
        obs[68:72] = list_of_cards_rank1

        self.shop2_cards = state['shop']['rank2_cards']
        list_of_cards_rank2 = [card.card_id for card in state['shop']['rank2_cards']]
        if len(list_of_cards_rank2) < 4:
            for i in range(4 - len(list_of_cards_rank2)):
                list_of_cards_rank2.append(90)
        obs[72:76] = list_of_cards_rank2

        self.shop3_cards = state['shop']['rank3_cards']
        list_of_cards_rank3 = [card.card_id for card in state['shop']['rank3_cards']]
        if len(list_of_cards_rank3) < 4:
            for i in range(4 - len(list_of_cards_rank3)):
                list_of_cards_rank3.append(90)
        obs[76:80] = list_of_cards_rank3

        list_of_nobles = [patron.patron_id for patron in state['shop']['nobles']]
        if len(list_of_nobles) < 5:
            for i in range(5 - len(list_of_nobles)):
                list_of_nobles.append(10)
        obs[80:85] = list_of_nobles

        obs[85] = state['shop']['rank1_size']
        obs[86] = state['shop']['rank2_size']
        obs[87] = state['shop']['rank3_size']

        self.obs = obs
        self.get_mask()
    def get_mask(self):
        state = self.game.gather_ia_board_state()
        mask = numpy.zeros(88)
        shop_cards = state['shop']['rank1_cards'] + state['shop']['rank2_cards'] + state['shop']['rank3_cards']
        mask = Checker.get_mask(state['player1']['cards'],shop_cards,state['shop']['rank1_size'],state['shop']['rank2_size'],state['shop']['rank3_size'],len(state['player1']['reserved']),TokenArray(state['player1']['tokens']),state['shop']['tokens'])
        print(mask)


    def reset(self):
        self.game.launch_game(2)
        self.from_board_states_to_obs()
        pass

    def step(self, action):
        if action == 0:
            # take [1,1,1,0,0,0] tokens
            self.game.take_token(TokenArray([1,1,1,0,0,0]))
        elif action ==1:
            # take [1,1,0,1,0,0] tokens
            self.game.take_token(TokenArray([1,1,0,1,0,0]))
        elif action ==2:
            # take [1,1,0,0,1,0] tokens
            self.game.take_token(TokenArray([1,1,0,0,1,0]))
        elif action ==3:
            # take [1,0,1,1,0,0] tokens
            self.game.take_token(TokenArray([1,0,1,1,0,0]))
        elif action ==4:
            # take [1,0,1,0,1,0] tokens
            self.game.take_token(TokenArray([1,0,1,0,1,0]))
        elif action ==5:
            # take [1,0,0,1,1,0] tokens
            self.game.take_token(TokenArray([1,0,0,1,1,0]))
        elif action ==6:
            # take [0,1,1,1,0,0] tokens
            self.game.take_token(TokenArray([0,1,1,1,0,0]))
        elif action ==7:
            # take [0,1,1,0,1,0] tokens
            self.game.take_token(TokenArray([0,1,1,0,1,0]))
        elif action ==8:
            # take [0,1,0,1,1,0] tokens
            self.game.take_token(TokenArray([0,1,0,1,1,0]))
        elif action ==9:
            # take [0,0,1,1,1,0] tokens
            self.game.take_token(TokenArray([0,0,1,1,1,0]))
        elif action ==10:
            self.game.take_token(TokenArray([2,0,0,0,0,0]))
        elif action ==11:
            self.game.take_token(TokenArray([0,2,0,0,0,0]))
        elif action ==12:
            self.game.take_token(TokenArray([0,0,2,0,0,0]))
        elif action ==13:
            self.game.take_token(TokenArray([0,0,0,2,0,0]))
        elif action ==14:
            self.game.take_token(TokenArray([0,0,0,0,2,0]))
        elif action ==15:
            self.game.buy_card(self.shop1_cards[0].card_id)
        elif action ==16:
            self.game.buy_card(self.shop1_cards[1].card_id)
        elif action ==17:
            self.game.buy_card(self.shop1_cards[2].card_id)
        elif action ==18:
            self.game.buy_card(self.shop1_cards[3].card_id)
        elif action ==19:
            self.game.buy_card(self.shop2_cards[0].card_id)
        elif action ==20:
            self.game.buy_card(self.shop2_cards[1].card_id)
        elif action ==21:
            self.game.buy_card(self.shop2_cards[2].card_id)
        elif action ==22:
            self.game.buy_card(self.shop2_cards[3].card_id)
        elif action ==23:
            self.game.buy_card(self.shop3_cards[0].card_id)
        elif action ==24:
            self.game.buy_card(self.shop3_cards[1].card_id)
        elif action ==25:
            self.game.buy_card(self.shop3_cards[2].card_id)
        elif action ==26:
            self.game.buy_card(self.shop3_cards[3].card_id)
        elif action ==27:
            self.game.buy_card(self.reserved_cards[0].card_id)
        elif action ==28:
            self.game.buy_card(self.reserved_cards[1].card_id)
        elif action ==29:
            self.game.buy_card(self.reserved_cards[2].card_id)
        elif action ==30:
            self.game.reserve_card(self.shop1_cards[0].card_id)
        elif action ==31:
            self.game.reserve_card(self.shop1_cards[1].card_id)
        elif action ==32:
            self.game.reserve_card(self.shop1_cards[2].card_id)
        elif action ==33:
            self.game.reserve_card(self.shop1_cards[3].card_id)
        elif action ==34:
            self.game.reserve_card(self.shop2_cards[0].card_id)
        elif action ==35:
            self.game.reserve_card(self.shop2_cards[1].card_id)
        elif action ==36:
            self.game.reserve_card(self.shop2_cards[2].card_id)
        elif action ==37:
            self.game.reserve_card(self.shop2_cards[3].card_id)
        elif action ==38:
            self.game.reserve_card(self.shop3_cards[0].card_id)
        elif action ==39:
            self.game.reserve_card(self.shop3_cards[1].card_id)
        elif action ==40:
            self.game.reserve_card(self.shop3_cards[2].card_id)
        elif action ==41:
            self.game.reserve_card(self.shop3_cards[3].card_id)
        elif action ==42:
            self.game.reserve_pile_card(0)
        elif action ==43:
            self.game.reserve_pile_card(1)
        elif action ==44:
            self.game.reserve_pile_card(2)

        obs = self.from_board_states_to_obs()
        reward = self.game.playerController.players[0].victoryPoints
        done = False
        info = {}
        return obs, reward, done, info
    def render(self):
        # prin
        pass

    def close(self):
        pass
