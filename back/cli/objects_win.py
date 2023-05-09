import curses

from model.patron import Patron
from model.card import Card
from model.player import Player


class MyWin():
    colors = (1, 2, 3, 4, 5, 6)


class PatronWin(MyWin):
    def __init__(self, patron: Patron, y, x) -> None:
        self.patron = patron
        self.win = curses.newwin(4, 11, y, x)
        self.win.refresh()

    def display(self) -> None:
        self.win.erase()
        # self.draw_border()
        self.win.border()

        self.win.addstr(1, 1, ' - 3PV - ')

        requirements = self.patron.requirements.get_tokens()
        if sum(requirements) == 8:
            x = 2
            for i in range(6):
                if requirements[i] == 4:
                    self.win.addstr(
                        2, x, '[4]', curses.color_pair(self.colors[i]))
                    x += 4
        else:
            x = 1
            for i in range(6):
                if requirements[i] == 3:
                    self.win.addstr(
                        2, x, '[3]', curses.color_pair(self.colors[i]))
                    x += 3
        self.win.refresh()


class CardWin(MyWin):
    def __init__(self, card: Card, y, x) -> None:
        self.card = card
        self.win = curses.newwin(6, 8, y, x)
        self.win.refresh()

    def display(self) -> None:
        self.win.erase()
        self.win.border()

        self.win.addstr(1, 1, str(self.card.victoryPoint.value))
        self.win.addstr(1, 4, '[]', curses.color_pair(
            self.colors[self.card.bonus.get_tokens().index(1)]))

        if len(str(self.card.card_id)) == 1:
            self.win.addstr(2, 1, f'__{self.card.card_id}___')
        else:
            self.win.addstr(2, 1, f'__{self.card.card_id}__')

        x = 1
        y = 3
        for i in range(6):
            if self.card.price.get_tokens()[i] != 0:
                self.win.addstr(
                    y, x, f'({self.card.price.get_tokens()[i]})', curses.color_pair(self.colors[i]))
                x += 3
                if x > 4:
                    x = 1
                    y += 1
        self.win.refresh()


class PlayerWin(MyWin):
    def __init__(self, player: Player, name: str, y, x) -> None:
        self.player = player
        self.name = name
        self.currentPlayer = False
        self.win = curses.newwin(5, 22, y, x)
        self.win.refresh()

    def display(self) -> None:
        self.win.erase()
        self.win.border()

        if self.currentPlayer:
            self.win.addstr(1, 1, '>')
        self.win.addstr(1, 2, self.name)
        self.win.addstr(1, 15, f'VP:{self.player.victoryPoints.value}')

        for i, v in enumerate(self.player.tokens.get_tokens()):
            self.win.addstr(
                2, 2 + i * 3, f'({v})', curses.color_pair(self.colors[i]))

        for i, v in enumerate(self.player.hand.compute_hand_bonuses().get_tokens()[:-1]):
            self.win.addstr(
                3, 2 + i * 3, f'[{v}]', curses.color_pair(self.colors[i]))
        self.win.refresh()


class InputWin(MyWin):
    def __init__(self) -> None:
        self.win = curses.newwin(3, 67, 22, 0)
        self.win.refresh()

    def display(self, message='') -> None:
        self.win.erase()
        self.win.clear()
        self.win.border()
        self.win.addstr(1, 2, message)
        self.win.refresh()


class HistWin(MyWin):
    def __init__(self, y: int, x: int, h: int) -> None:
        self.nbLines = h - 2
        self.win = curses.newwin(h, 67, y, x)
        self.win.refresh()

    def display(self, message: list[str]) -> None:
        self.win.erase()
        self.win.clear()
        self.win.border()

        if len(message) > self.nbLines:
            toDisplay = message[len(message) - self.nbLines::-1]
        else:
            toDisplay = message[::-1]

        for i, line in enumerate(toDisplay):
            if i == 0:
                self.win.addstr(i + 1, 2, line)
            else:
                self.win.addstr(i + 1, 2, line, curses.color_pair(5))
        self.win.refresh()
