import pandas as pd
import rank
from token_array import TokenArray
from victory_point import VictoryPoint


def bonus_color_to_enum_array(bonus_color: str) -> TokenArray:
    # switch on the bonus color

    if bonus_color == 'White':
        return TokenArray([1, 0, 0, 0, 0])
    elif bonus_color == 'Blue':
        return TokenArray([0, 1, 0, 0, 0])
    elif bonus_color == 'Green':
        return TokenArray([0, 0, 1, 0, 0])
    elif bonus_color == 'Red':
        return TokenArray([0, 0, 0, 1, 0])
    elif bonus_color == 'Black':
        return TokenArray([0, 0, 0, 0, 1])
    else:
        return TokenArray([0, 0, 0, 0, 0])


def retrieve_and_parse_cards() -> list[Cards.Card]:
    df = pd.read_csv('data/card.csv')
    df['id'] = range(1, len(df) + 1)
    df.set_index('id', inplace=True)

    card_list = df.apply(
        lambda card: Cards.Card(TokenArray([card['White'], card['Blue'], card['Green'], card['Red'], card['Black']]),
                          bonus_color_to_enum_array(card['Color']), VictoryPoint(card['PV']), card_id=card.name),
        axis=1)
    return card_list
