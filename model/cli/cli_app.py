from termcolor import colored as c

from model.game_manager import GameManager
from model.token_array import TokenArray


class CliApp():
    def __init__(self, nbPlayer: int) -> None:
        # game
        self.gm = GameManager(nbPlayer)

        # constants
        self.ESCAPE = ['q']

        # screen
        self.width = 80
        self.height = 24

    def main_loop(self) -> None:
        # TODO: while loop
        boardState = self.gm.gather_cli_board_state()
        self.display(boardState)

    def display(self, boardState) -> None:
        bs = boardState
        print("+---------+----------------------------------+--------------------+")

        print("| PATRONS |              BANK                | CPU#1        VP:", end='')
        print(str(bs['cpu1-vp']) + (3 - len(str(bs['cpu1-vp']))) * ' ' + '|')

        print("|         |  white blue  green  red  black   | " + self.str_token_array(bs['cpu1-tokens']) + " |")

        print(f"|[- 3PV -]|   ({bs['bank'][0]})   ({bs['bank'][1]})   ({bs['bank'][2]})   ({bs['bank'][3]})   ({bs['bank'][4]})    |", end="")
        print(" " + self.str_bonus_array(bs['cpu1-bonus']) + f" [{bs['cpu1-nbReserved']}]|")

        print(f"|{self.str_patron_price(bs['patrons'][0])}|                                  +--------------------+")

        print("|         |              SHOP                | CPU#1        VP:", end='')
        print(str(bs['cpu2-vp']) + (3 - len(str(bs['cpu2-vp']))) * ' ' + '|')

        print("|[- 3PV -]|   ", end="")
        print(f"{bs['shop00-pv']}  {self.str_card_bonus(bs['shop00-bonus'])}   ", end="")
        print(f"{bs['shop10-pv']}  {self.str_card_bonus(bs['shop10-bonus'])}   ", end="")
        print(f"{bs['shop20-pv']}  {self.str_card_bonus(bs['shop20-bonus'])}   ", end="")
        print(f"{bs['shop30-pv']}  {self.str_card_bonus(bs['shop30-bonus'])}  ", end="")
        print(f"| {self.str_token_array(bs['cpu2-tokens'])} |")

        print(f"|{self.str_patron_price(bs['patrons'][1])}|  ", end="")
        print(f"{self.str_first_card_price(bs['shop00-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop10-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop20-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop30-price'])}  ", end="")
        print(f"| {self.str_bonus_array(bs['cpu2-bonus'])} [{bs['cpu2-nbReserved']}]|")

        print("|         |  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop00-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop10-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop20-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop30-price'])}  ", end="")
        print("+--------------------+")

        print("|[- 3PV -]|                                  | CPU#1        VP:", end='')
        print(str(bs['cpu3-vp']) + (3 - len(str(bs['cpu3-vp']))) * ' ' + '|')

        print(f"|{self.str_patron_price(bs['patrons'][2])}|   ", end="")
        print(f"{bs['shop01-pv']}  {self.str_card_bonus(bs['shop01-bonus'])}   ", end="")
        print(f"{bs['shop11-pv']}  {self.str_card_bonus(bs['shop11-bonus'])}   ", end="")
        print(f"{bs['shop21-pv']}  {self.str_card_bonus(bs['shop21-bonus'])}   ", end="")
        print(f"{bs['shop31-pv']}  {self.str_card_bonus(bs['shop31-bonus'])}  ", end="")
        print(f"| {self.str_token_array(bs['cpu3-tokens'])} |")

        print("|         |  ", end="")
        print(f"{self.str_first_card_price(bs['shop01-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop11-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop21-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop31-price'])}  ", end="")
        print(f"| {self.str_bonus_array(bs['cpu3-bonus'])} [{bs['cpu3-nbReserved']}]|")

        print("|[- 3PV -]|  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop01-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop11-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop21-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop31-price'])}  ", end="")
        print("+--------------------+")

        print(f"|{self.str_patron_price(bs['patrons'][3])}|                                  |                    |")

        print("|         |   ", end="")
        print(f"{bs['shop02-pv']}  {self.str_card_bonus(bs['shop02-bonus'])}   ", end="")
        print(f"{bs['shop12-pv']}  {self.str_card_bonus(bs['shop12-bonus'])}   ", end="")
        print(f"{bs['shop22-pv']}  {self.str_card_bonus(bs['shop22-bonus'])}   ", end="")
        print(f"{bs['shop32-pv']}  {self.str_card_bonus(bs['shop32-bonus'])}  ", end="")
        print("| PLAYER       VP:", end='')
        print(str(bs['player-vp']) + (3 - len(str(bs['player-vp']))) * ' ' + '|')

        print("|[- 3PV -]|  ", end="")
        print(f"{self.str_first_card_price(bs['shop02-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop12-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop22-price'])}  ", end="")
        print(f"{self.str_first_card_price(bs['shop32-price'])}  ", end="")
        print(f"| {self.str_token_array(bs['player-tokens'])} |")

        print(f"|{self.str_patron_price(bs['patrons'][4])}|  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop02-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop12-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop22-price'])}  ", end="")
        print(f"{self.str_scnd_card_price(bs['shop32-price'])}  ", end="")
        print(f"| {self.str_bonus_array(bs['player-bonus'])} [{bs['player-nbReserved']}]|")

        print("|         |                                  |                    |")
        print("+---------+----------------------------------+--------------------+")

    def str_token_array(self, ta: TokenArray) -> str:
        out = ""
        out += c(f'({ta.tokens[0]})', 'white')
        out += c(f'({ta.tokens[1]})', 'blue')
        out += c(f'({ta.tokens[2]})', 'green')
        out += c(f'({ta.tokens[3]})', 'red')
        out += c(f'({ta.tokens[4]})', 'light_grey')
        out += c(f'({ta.tokens[5]})', 'yellow')
        return out

    def str_bonus_array(self, ta: TokenArray) -> str:
        out = ""
        out += c(f'[{ta.tokens[0]}]', 'white')
        out += c(f'[{ta.tokens[1]}]', 'blue')
        out += c(f'[{ta.tokens[2]}]', 'green')
        out += c(f'[{ta.tokens[3]}]', 'red')
        out += c(f'[{ta.tokens[4]}]', 'light_grey')
        return out

    def str_patron_price(self, ta: TokenArray) -> str:
        out = ""
        count = 0
        for i, color in enumerate(['white', 'blue', 'green', 'red', 'light_grey']):
            if ta.tokens[i] != 0:
                count += 1
                out += c(f'[{ta.tokens[i]}]', color)
        out += (9 - 3 * count) * " "
        return out

    def str_first_card_price(self, ta: TokenArray) -> str:
        out = ""
        count = 0
        for i, color in enumerate(['white', 'blue', 'green', 'red', 'light_grey']):
            if ta.tokens[i] != 0:
                out += c(f'({ta.tokens[i]})', color)
                count += 1
            if count >= 2:
                break
        out += (6 - 3 * count) * " "
        return out

    def str_scnd_card_price(self, ta: TokenArray) -> str:
        out = ""
        count = 0
        for i, color in enumerate(['white', 'blue', 'green', 'red', 'light_grey']):
            if ta.tokens[i] != 0:
                count += 1
                if count > 2:
                    out += c(f'({ta.tokens[i]})', color)
        if count == 1:
            out += 6 * " "
        else:
            out += (6 - 3 * (count - 2)) * " "
        return out

    def str_card_bonus(self, ta: TokenArray) -> str:
        for i, color in enumerate(['white', 'blue', 'green', 'red', 'light_grey']):
            if ta.tokens[i] != 0:
                return c('[]', color)
        return 'er'
