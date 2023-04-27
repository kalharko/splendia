# checker class
from model.token_array import TokenArray
import numpy
from model.card import Card


class Checker:

    @staticmethod
    def possible_token_to_take_2(player_token: TokenArray, bank_token: TokenArray):
        token_list = [0, 0, 0, 0, 0]
        higher_than_8 = []
        iterator = 0
        number_of_token = 0
        if (numpy.array(player_token.get_tokens()).sum()) > 8:
            return [0, 0, 0, 0, 0]

        for token in bank_token.get_tokens():
            if iterator >= 5:
                break
            if token >= 4:
                token_list[iterator] = 1
            else:
                token_list[iterator] = 0
            iterator += 1

        return token_list

    @staticmethod
    def possible_token_to_take_3(player_token: TokenArray, bank_token: TokenArray):
        """ combinations :
        1,2,3 -> [1,1,1,0,0,0]
        1,2,4 -> [1,1,0,1,0,0]
        1,2,5 -> [1,1,0,0,1,0]
        1,3,4 -> [1,0,1,1,0,0]
        1,3,5 -> [1,0,1,0,1,0]
        1,4,5 -> [1,0,0,1,1,0]
        2,3,4 -> [0,1,1,1,0,0]
        2,3,5 -> [0,1,1,0,1,0]
        2,4,5 -> [0,1,0,1,1,0]
        3,4,5 -> [0,0,1,1,1,0]
        """
        if (numpy.array(player_token.get_tokens()).sum()) > 7:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        combination_dict = {
            1: numpy.array([1, 1, 1, 0, 0, 0]),
            2: numpy.array([1, 1, 0, 1, 0, 0]),
            3: numpy.array([1, 1, 0, 0, 1, 0]),
            4: numpy.array([1, 0, 1, 1, 0, 0]),
            5: numpy.array([1, 0, 1, 0, 1, 0]),
            6: numpy.array([1, 0, 0, 1, 1, 0]),
            7: numpy.array([0, 1, 1, 1, 0, 0]),
            8: numpy.array([0, 1, 1, 0, 1, 0]),
            9: numpy.array([0, 1, 0, 1, 1, 0]),
            10: numpy.array([0, 0, 1, 1, 1, 0])
        }
        mask_list = []
        bank_token = numpy.array(bank_token.get_tokens())
        bank_token[-1] = 1

        # iterate over combination_dict
        for key, value in combination_dict.items():
            if numpy.all(bank_token >= value):
                mask_list.append(1)
            else:
                mask_list.append(0)
        return mask_list

    @staticmethod
    def possible_card_to_buy(player_token: TokenArray, shop_cards: list[Card], player_hand: list[Card], player):
        mask = []
        count_not_none = [card for card in player_hand if card is not None]
        if len(count_not_none) == 20:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for rank_cards in shop_cards:
            for card in rank_cards:
                if card is None:
                    mask.append(0)
                else:
                    boolean , _ = player.can_pay_with_reduced_price(card.price)
                    if boolean:
                        mask.append(1)
                    else:
                        mask.append(0)
        if len(mask) < 12:
            for i in range(12 - len(mask)):
                mask.append(0)
        return mask

    @staticmethod
    def possible_card_to_buy_in_reserve(player_token: TokenArray, reserved_cards: list[Card], player_hand: list[Card],player):

        mask = []
        count_not_none = [card for card in player_hand if card is not None]
        if len(count_not_none) == 20:

            return [0, 0, 0]

        for card in reserved_cards:
            if card is None:
                mask.append(0)
            else:
                boolean , _ = player.can_pay_with_reduced_price(card.price)
                if boolean:
                    mask.append(1)
                else:
                    mask.append(0)
        return mask

    @staticmethod
    def possible_card_to_reserve_in_shop(player_reserved_cards: int, shop_cards: list[Card]):
        mask = []
        if player_reserved_cards == 3:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for rank_cards in shop_cards:

            for card in rank_cards:
                if card is None:
                    mask.append(0)
                else:
                    mask.append(1)
        if len(mask) < 12:
            for i in range(12 - len(mask)):
                mask.append(0)
        return mask

    @staticmethod
    def possible_card_to_reserve_top_deck(player_reserved_number: int, tier1: int, tier2: int, tier3: int):
        mask = []

        if (player_reserved_number) == 3:
            return [0, 0, 0]

        if tier1 == 0:
            mask.append(0)
        else:
            mask.append(1)
        if tier2 == 0:
            mask.append(0)
        else:
            mask.append(1)
        if tier3 == 0:
            mask.append(0)
        else:
            mask.append(1)

        return mask

    @staticmethod
    def get_mask(player_hand: list[Card], shop_cards: list[Card], tier1: int, tier2: int, tier3: int,
                 player_reserved_number: int, player_token: TokenArray, bank_token: TokenArray,
                 player_reserved_cards: list[Card], player):
        """
        the mask :
        10 bites for 10 possible combination of 3 tokens to take
        5 bites for 5 possible combination of 2 tokens to take
        12 bites for 12 possible combination of one card to buy in the shop
        3 bites for 3 possible combination of one card  to but in the reserve
        12 bites to reserve in the shop
        3 bites to reserve card at the top of the deck
        """
        # count none values of player_reserved cards

        mask = numpy.zeros(46)
        mask[0:10] = Checker.possible_token_to_take_3(player_token, bank_token)
        mask[10:15] = Checker.possible_token_to_take_2(player_token, bank_token)
        mask[15:27] = Checker.possible_card_to_buy(player_token, shop_cards, player_hand, player)
        mask[27:30] = Checker.possible_card_to_buy_in_reserve(player_token, player_reserved_cards, player_hand,player)
        mask[30:42] = Checker.possible_card_to_reserve_in_shop(player_reserved_number, shop_cards)
        mask[42:45] = Checker.possible_card_to_reserve_top_deck(player_reserved_number, tier1, tier2, tier3)
        #
        # check if mask is full of 0
        if numpy.all(mask == 0):
            mask[-1] = 1
        return mask
