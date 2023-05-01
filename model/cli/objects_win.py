import unicurses as curses
from model.business_model.patron import Patron
from model.business_model.card import Card
from model.business_model.player import Player


class MyWin():
    colors = (curses.COLOR_WHITE, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    def draw_border(self):
        bottom, right = curses.getmaxyx(self.win)
        curses.mvwhline(self.win, 0, 0, curses.ACS_HLINE, right)
        curses.mvwhline(self.win, bottom, 0, curses.ACS_HLINE, right)
        curses.mvwvline(self.win, 0, 0, curses.ACS_VLINE, bottom)
        curses.mvwvline(self.win, 0, right, curses.ACS_VLINE, bottom)
        curses.mvwaddch(self.win, 0, 0, curses.ACS_ULCORNER)
        curses.mvwaddch(self.win, 0, right, curses.ACS_URCORNER)
        curses.mvwaddch(self.win, bottom, 0, curses.ACS_LLCORNER)
        curses.mvwaddch(self.win, 0, right, curses.ACS_LRCORNER)


class PatronWin(MyWin):
    def __init__(self, patron: Patron, y, x) -> None:
        self.patron = patron
        self.win = curses.newwin(nlines=4, ncols=11, begin_y=y, begin_x=x)

    def display(self) -> None:
        curses.werase(self.win)
        self.draw_border()

        curses.mvwaddstr(self.win, 1, 1, ' - 3PV - ')

        requirements = self.patron.requirements.get_tokens()
        if sum(requirements) == 2:
            x = 2
            for i in range(6):
                if requirements[i] == 4:
                    curses.mvwaddstr(self.win, 1, x, '[4]', self.colors[i])
                    x += 6
        else:
            x = 1
            for i in range(6):
                if requirements[i] == 3:
                    curses.mvwaddstr(self.win, 1, x, '[3]', self.colors[i])
                    x += 3
        curses.wrefresh(self.win)


class CardWin(MyWin):
    def __init__(self, card: Card, y, x) -> None:
        self.card = card
        self.win = curses.newwin(nlines=7, ncols=7, begin_y=y, begin_x=x)

    def display(self) -> None:
        curses.werase(self.win)
        self.draw_border()

        curses.mvwaddstr(self.win, 1, 1, str(self.card.victoryPoint.value))
        curses.mvwaddstr(self.win, 1, 4, '[]', self.colors[self.card.bonus.get_tokens().index(1)])

        if len(str(self.card.card_id)) == 1:
            curses.mvwaddstr(self.win, 2, 1, f'__{self.card.card_id}__')
        else:
            curses.mvwaddstr(self.win, 2, 1, f'_{self.card.card_id}__')

        x = 1
        y = 3
        for i in range(6):
            if self.card.price.get_tokens()[i] != 0:
                curses.mvwaddstr(self.win, y, x, f'({self.card.price.get_tokens()[i]})', self.colors[i])
                x += 3
                if x > 4:
                    x = 1
                    y += 1
        curses.wrefresh(self.win)


class PlayerWin(MyWin):
    def __init__(self, player: Player, name: str, y, x) -> None:
        self.player = player
        self.name = name
        self.win = curses.newwin(nlines=5, ncols=22, begin_y=y, begin_x=x)

    def display(self):
        curses.werase(self.win)
        self.draw_border()

        curses.mvwaddstr(self.win, 1, 2, self.name)
        curses.mvwaddstr(self.win, 1, 15, f'VP:{self.player.victoryPoints.value}')

        for i, v in enumerate(self.player.tokens.get_tokens()):
            curses.mvwaddstr(self.win, 2, 2 + i, f'({v})', self.colors[i])

        for i, v in enumerate(self.player.hand.compute_hand_bonuses().get_tokens()):
            curses.mvwaddstr(self.win, 3, 2 + i, f'[{v}]', self.colors[i])
        curses.wrefresh(self.win)


class InputWin(MyWin):
    def __init__(self) -> None:
        self.win = curses.newwin(3, 67, 20, 0)

    def display(self, message=''):
        curses.werase(self.win)
        self.draw_border()
        curses.mvwaddstr(self.win, 1, 2, message)
        curses.wrefresh(self.win)
