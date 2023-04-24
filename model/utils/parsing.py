import pandas as pd

from model.token_array import TokenArray
from model.victory_point import VictoryPoint
from model.card import Card
from model.patron import Patron


def bonus_color_to_enum_array(bonus_color: str) -> TokenArray:
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
    df = pd.read_csv('model/data/card.csv')
    df.set_index('Id', inplace=True)

    card_list = df.apply(
        lambda card: Card(
            price=TokenArray([card['White'], card['Blue'], card['Green'], card['Red'], card['Black'], 0]),
            bonus=bonus_color_to_enum_array(card['Color']),
            victoryPoint=VictoryPoint(card['PV']),
            card_id=card.name),
        axis=1)
    return card_list

def retrieve_and_parse_patrons() -> list[Patron]:
    df = pd.read_csv('model/data/card.csv')
    #df.set_index('Id', inplace=True)

    patron_list = df.apply(
        lambda patron: Patron(
            requirements=TokenArray([patron['White'], patron['Blue'], patron['Green'], patron['Red'], patron['Black'], 0]),
            victoryPoints=VictoryPoint(0),
            patron_id=patron.name),
        axis=1)
    return patron_list
