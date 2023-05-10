# checker class
from model.token_array import TokenArray
import numpy
from model.card import Card
from typing import List
from model.player import Player


class Checker:
    """This class is used to check if a player can take a card or a token."""

    @staticmethod
    def possible_token_to_take_2(player_token: TokenArray, bank_token: TokenArray) -> List[int]:
        """This method returns a list of 5 elements, each element is 1 if the player can take the token of the same index, 0 otherwise.
        The player can take a token if the bank has at least 4 tokens of that type and the player has less than 8 tokens.
        The list is ordered as the token array, so the first element is the number of white tokens, the second the number of blue tokens and so on.
        Args:
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
        Returns:
            List[int]: The list of the tokens that the player can take.
            """
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)

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
    def possible_token_to_take_3(player_token: TokenArray, bank_token: TokenArray) -> List[int]:
        """This method returns a list of 10 elements, each element is 1 if the player can take the token of the same index, 0 otherwise.
        Args:
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
        Returns:
            List[int]: The list of the tokens that the player can take.
            """
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
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)

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
    def possible_card_to_buy(shop_cards: list[Card], player_hand: list[Card], player: Player) -> List[int]:
        """This method returns a list of 12 elements, each element is 1 if the player can buy the card of the same index, 0 otherwise.
        Args:
            shop_cards (list[Card]): The cards in the shop.
            player_hand (list[Card]): The cards in the player hand.
            player (Player): The player.
        Returns:
            List[int]: The list of the cards that the player can buy.
            """
        assert isinstance(shop_cards, list)
        assert isinstance(player_hand, list)
        assert isinstance(player, Player)

        mask = []
        count_not_none = [card for card in player_hand if card is not None]
        if len(count_not_none) == 20:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for rank_cards in shop_cards:
            for card in rank_cards:
                if card is None:
                    mask.append(0)
                else:
                    boolean, _ = player.can_pay_with_reduced_price(card.price)
                    if boolean:
                        mask.append(1)
                    else:
                        mask.append(0)
        if len(mask) < 12:
            for i in range(12 - len(mask)):
                mask.append(0)
        return mask

    @staticmethod
    def possible_card_to_buy_in_reserve(reserved_cards: list[Card], player_hand: list[Card], player: Player) -> List[int]:
        """This method returns a list of 3 elements, each element is 1 if the player can buy the card of the same index, 0 otherwise.

        Args:
            reserved_cards (list[Card]): The cards in the reserve.
            player_hand (list[Card]): The cards in the player hand.
            player (Player): The player.
        Returns:
            List[int]: The list of the cards that the player can buy.
            """
        assert isinstance(reserved_cards, list)
        assert isinstance(player_hand, list)
        assert isinstance(player, Player)

        mask = []
        count_not_none = [card for card in player_hand if card is not None]
        if len(count_not_none) == 20:

            return [0, 0, 0]

        for card in reserved_cards:
            if card is None:
                mask.append(0)
            else:
                boolean, _ = player.can_pay_with_reduced_price(card.price)
                if boolean:
                    mask.append(1)
                else:
                    mask.append(0)
        return mask

    @staticmethod
    def possible_card_to_reserve_in_shop(player_reserved_cards: int, shop_cards: list[Card]) -> List[int]:
        """This method returns a list of 12 elements, each element is 1 if the player can reserve the card of the same index, 0 otherwise.

        Args:
            player_reserved_cards (int): The number of cards reserved by the player.
            shop_cards (list[Card]): The cards in the shop.
        Returns:
            List[int]: The list of the cards that the player can reserve.
            """
        assert isinstance(player_reserved_cards, int)
        assert isinstance(shop_cards, list)

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
    def possible_card_to_reserve_top_deck(player_reserved_number: int, tier1: int, tier2: int, tier3: int) -> List[int]:
        """This method returns a list of 3 elements, each element is 1 if the player can reserve the card of the same index, 0 otherwise.

        Args:
            player_reserved_number (int): The number of cards reserved by the player.
            tier1 (int): The number of tier 1 cards.
            tier2 (int): The number of tier 2 cards.
            tier3 (int): The number of tier 3 cards.
        Returns:
            List[int]: The list of the cards that the player can reserve.
            """
        assert isinstance(player_reserved_number, int)
        assert isinstance(tier1, int)
        assert isinstance(tier2, int)
        assert isinstance(tier3, int)

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
                 player_reserved_cards: list[Card], player: Player) -> numpy.ndarray:
        """This method returns a mask of 66 elements, each element is 1 if the player can do the action of the same index, 0 otherwise.

        Args:
            player_hand (list[Card]): The cards in the player hand.
            shop_cards (list[Card]): The cards in the shop.
            tier1 (int): The number of tier 1 cards.
            tier2 (int): The number of tier 2 cards.
            tier3 (int): The number of tier 3 cards.
            player_reserved_number (int): The number of cards reserved by the player.
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
            player_reserved_cards (list[Card]): The cards in the reserve.
            player (Player): The player.
        Returns:
            numpy.ndarray: The mask.
        """
        """
        the mask :
        10 bites for 10 possible combination of 3 tokens to take
        5 bites for 5 possible combination of 2 tokens to take
        12 bites for 12 possible combination of one card to buy in the shop
        3 bites for 3 possible combination of one card  to but in the reserve
        12 bites to reserve in the shop
        3 bites to reserve card at the top of the deck
        """
        assert isinstance(player_hand, list)
        assert isinstance(shop_cards, list)
        assert isinstance(tier1, int)
        assert isinstance(tier2, int)
        assert isinstance(tier3, int)
        assert isinstance(player_reserved_number, int)
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)
        assert isinstance(player_reserved_cards, list)
        assert isinstance(player, Player)

        # count none values of player_reserved cards

        mask = numpy.zeros(66)
        mask[0:10] = Checker.possible_token_to_take_3(player_token, bank_token)
        mask[10:15] = Checker.possible_token_to_take_2(
            player_token, bank_token)
        mask[15:27] = Checker.possible_card_to_buy(
            shop_cards, player_hand, player)
        mask[27:30] = Checker.possible_card_to_buy_in_reserve(
            player_reserved_cards, player_hand, player)
        mask[30:42] = Checker.possible_card_to_reserve_in_shop(
            player_reserved_number, shop_cards)
        mask[42:45] = Checker.possible_card_to_reserve_top_deck(
            player_reserved_number, tier1, tier2, tier3)
        mask[45:50] = Checker.possible_token_to_take_1_and_reject(
            player_token, bank_token)
        mask[50:60] = Checker.possible_token_to_take_2_different_and_reject(
            player_token, bank_token)
        mask[60:65] = Checker.possible_token_to_take_2_same_and_reject(
            player_token, bank_token)

        # check if mask is full of 0
        if numpy.all(mask == 0):

            mask[-1] = 1
        # print(mask)
        return mask

    @staticmethod
    def possible_token_to_take_1_and_reject(player_token: TokenArray, bank_token: TokenArray) -> numpy.ndarray:
        """This method returns a list of 5 elements, each element is 1 if the player can take the token of the same index, 0 otherwise.

        Args:
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
        Returns:
            numpy.ndarray: The list of the tokens that the player can take.
        """
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)

        # check if there is at least three colors none empty in the bank that are not gold
        non_empty_pile = 0
        for color in range(5):
            if bank_token.get_tokens()[color] > 0:
                non_empty_pile += 1
        if non_empty_pile < 3 or player_token.nb_of_tokens() != 9:
            return numpy.zeros(5)
        mask = numpy.zeros(5)
        for color in range(5):
            if bank_token.get_tokens()[color] > 0:
                mask[color] = 1

        return mask

    @staticmethod
    def possible_token_to_take_2_different_and_reject(player_token: TokenArray, bank_token: TokenArray) -> numpy.ndarray:
        """This method returns a list of 10 elements, each element is 1 if the player can take the tokens of the same index, 0 otherwise.

        Args:
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
        Returns:
            numpy.ndarray: The list of the tokens that the player can take.
        """
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)

        # check if there is at least three colors none empty in the bank that are not gold
        non_empty_pile = 0
        for color in range(5):
            if bank_token.get_tokens()[color] > 0:
                non_empty_pile += 1
        if non_empty_pile < 3 or player_token.nb_of_tokens() != 8:
            return numpy.zeros(10)
        mask = numpy.zeros(10)
        """ possible combinations :
        1,2 -> [1,1,0,0,0,0,0,0,0,0]
        1,3 -> [1,0,1,0,0,0,0,0,0,0]
        1,4 -> [1,0,0,1,0,0,0,0,0,0]
        1,5 -> [1,0,0,0,1,0,0,0,0,0]
        2,3 -> [0,1,1,0,0,0,0,0,0,0]
        2,4 -> [0,1,0,1,0,0,0,0,0,0]
        2,5 -> [0,1,0,0,1,0,0,0,0,0]
        3,4 -> [0,0,1,1,0,0,0,0,0,0]
        3,5 -> [0,0,1,0,1,0,0,0,0,0]
        4,5 -> [0,0,0,1,1,0,0,0,0,0]
        """

        combination_dict = {
            1: numpy.array([1, 1, 0, 0, 0, 0]),
            2: numpy.array([1, 0, 1, 0, 0, 0]),
            3: numpy.array([1, 0, 0, 1, 0, 0]),
            4:  numpy.array([1, 0, 0, 0, 1, 0]),
            5:  numpy.array([0, 1, 1, 0, 0, 0]),
            6:  numpy.array([0, 1, 0, 1, 0, 0]),
            7:  numpy.array([0, 1, 0, 0, 1, 0]),
            8:  numpy.array([0, 0, 1, 1, 0, 0]),
            9:  numpy.array([0, 0, 1, 0, 1, 0]),
            10:  numpy.array([0, 0, 0, 1, 1, 0])
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
    def possible_token_to_take_2_same_and_reject(player_token: TokenArray, bank_token: TokenArray) -> numpy.ndarray:
        """This method returns a list of 5 elements, each element is 1 if the player can take the tokens of the same index, 0 otherwise.

        Args:
            player_token (TokenArray): The tokens of the player.
            bank_token (TokenArray): The tokens of the bank.
        Returns:
            numpy.ndarray: The list of the tokens that the player can take.
            """
        assert isinstance(player_token, TokenArray)
        assert isinstance(bank_token, TokenArray)

        # check if there is at least three colors none empty in the bank that are not gold
        non_empty_pile = 0
        for color in range(5):
            if bank_token.get_tokens()[color] > 0:
                non_empty_pile += 1
        if non_empty_pile < 3 or player_token.nb_of_tokens() != 8:
            return numpy.zeros(5)
        mask = Checker.possible_token_to_take_2(player_token, bank_token)
        # convert the mask to a np array
        mask = numpy.array(mask)

        return mask
