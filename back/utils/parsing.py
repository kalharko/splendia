import pandas as pd

from model.token_array import TokenArray
from model.victory_point import VictoryPoint
from model.card import Card
from model.patron import Patron


def bonus_color_to_enum_array(bonus_color: str) -> TokenArray:
    """This function converts a bonus color to an enum array.

    Args:
        bonus_color (str): The bonus color.

    Returns:
        TokenArray: The enum array.

            """
    # switch on the bonus color

    if bonus_color == 'White':
        return TokenArray([1, 0, 0, 0, 0, 0])
    elif bonus_color == 'Blue':
        return TokenArray([0, 1, 0, 0, 0, 0])
    elif bonus_color == 'Green':
        return TokenArray([0, 0, 1, 0, 0, 0])
    elif bonus_color == 'Red':
        return TokenArray([0, 0, 0, 1, 0, 0])
    elif bonus_color == 'Black':
        return TokenArray([0, 0, 0, 0, 1, 0])
    else:
        return TokenArray([0, 0, 0, 0, 0, 0])


def retrieve_and_parse_cards() -> list[Card]:
    """This function retrieves and parses the cards from the csv file.

    Returns:
        list[Card]: The list of cards.
        """
    df = pd.read_csv(
        'data/card.csv')
    df.set_index('Id', inplace=True)

    card_list = df.apply(
        lambda card: Card(
            price=TokenArray([card['White'], card['Blue'],
                             card['Green'], card['Red'], card['Black'], 0]),
            bonus=bonus_color_to_enum_array(card['Color']),
            victoryPoint=VictoryPoint(card['PV']),
            cardId=card.name),
        axis=1)
    return card_list


def retrieve_and_parse_patrons() -> list[Patron]:
    """This function retrieves and parses the patrons from the csv file.

    Returns:
        list[Patron]: The list of patrons.
        """

    df = pd.read_csv(
        'data/patrons.csv')
    df.set_index('id', inplace=True)

    patron_list = df.apply(
        lambda patron: Patron(
            requirements=TokenArray(
                [int(patron['blanc']), int(patron['bleu']), int(patron['vert']), int(patron['rouge']), int(patron['noir']), 0]),
            victoryPoints=VictoryPoint(3),
            patron_id=patron.name),
        axis=1)

    return patron_list.to_list()
