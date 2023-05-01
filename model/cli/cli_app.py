import unicurses as curses

from model.business_model.game_manager import GameManager
from model.cli.objects_win import PatronWin, CardWin, PlayerWin, InputWin


class CliApp():
    def __init__(self, nbPlayer: int) -> None:
        # color tests
        if (curses.has_colors() is False):
            print("Your terminal does not support color!")
        curses.start_color()
        curses.noecho()

        # game
        self.gm = GameManager(nbPlayer)
        self.gm.launch_game(nbPlayer)

        # constants
        self.ESCAPE = ['q']
        self.SCREEN_HEIGHT = 47
        self.MIN_SIZE = (23, 67)

        # colors
        curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.COMMANDS = {
            'take': self.take_tokens,
            'token': self.take_tokens,
            'white': self.take_tokens,
            'blue': self.take_tokens,
            'green': self.take_tokens,
            'red': self.take_tokens,
            'black': self.take_tokens,

            'reserve': self.reserve,
            'buy': self.buy,
            'h': self.help,
            'help': self.help,
        }

        # screen
        self.stdscr = curses.initscr()
        self.screenH, self.screenW = curses.getmaxyx(self.stdscr)
        if self.screenH < self.MIN_SIZE[0] or self.screenW < self.MIN_SIZE[1]:
            print('console too small' + str((self.screenH, self.screenW)))
            quit()
        self.inputWin = InputWin()

        # main loop
        self.main_loop()

        # exit
        curses.werase(self.stdscr)
        curses.refresh()

    def main_loop(self) -> None:
        while True:
            self.display()
            user_input = self.get_input()
            if user_input in self.ESCAPE:
                break
            elif user_input[0] in self.COMMANDS.keys():
                self.COMMANDS[user_input[0]](user_input[1:])
            else:
                pass

    def get_input(self, message="") -> list[str]:
        self.inputWin.display(message)

        out = ''
        newchar = curses.wgetch(self.inputWin.win)
        pos_cursor = 0
        while newchar != '\n':
            if type(newchar) == int:
                if newchar == 263:  # delete
                    if len(out) > 0 and pos_cursor > 0:
                        out = out[:pos_cursor - 1] + out[pos_cursor:]
                        pos_cursor -= 1
                elif newchar == curses.KEY_LEFT:  # left arrow
                    pos_cursor = pos_cursor - 1 if pos_cursor > 0 else 0
                elif newchar == curses.KEY_RIGHT:  # right arrow
                    pos_cursor = pos_cursor + 1 if pos_cursor < len(out) else pos_cursor
                elif newchar == curses.KEY_DOWN:  # down arrow
                    pos_cursor = len(out)
                elif newchar == curses.KEY_UP:  # up arrow
                    pos_cursor = 0
                else:
                    with open('log.txt', 'a') as file:
                        file.write(str(type(newchar)) + '     ' + str(newchar) + '\n')
            else:
                out = out[:pos_cursor] + newchar + out[pos_cursor:]
                pos_cursor += 1

            self.inputWin.display(out[:pos_cursor] + '_' + out[pos_cursor:])
            newchar = curses.wgetch(self.inputWin.win)

        self.inputWin.display('')
        return out

    def display(self) -> None:
        curses.werase(self.stdscr)

        # border
        right = 67
        bottom = 21
        curses.mvwhline(self.stdscr, 0, 0, curses.ACS_HLINE, right)
        curses.mvwhline(self.stdscr, bottom, 0, curses.ACS_HLINE, right)
        curses.mvwvline(self.stdscr, 0, 0, curses.ACS_VLINE, bottom)
        curses.mvwvline(self.stdscr, 0, right, curses.ACS_VLINE, bottom)
        curses.mvwaddch(self.stdscr, 0, 0, curses.ACS_ULCORNER)
        curses.mvwaddch(self.stdscr, 0, right, curses.ACS_URCORNER)
        curses.mvwaddch(self.stdscr, bottom, 0, curses.ACS_LLCORNER)
        curses.mvwaddch(self.stdscr, bottom, right, curses.ACS_LRCORNER)

        # patron windows
        self.patronWins = [PatronWin(patron, y, 0) for patron, y in zip(self.gm.get_patron_controller().patrons, (3, 8, 13, 18, 23))]
        for patronWin in self.patronWins:
            patronWin.display()

        # card windows
        self.cardWins = []
        for i, rank in enumerate(self.gm.get_shop_controller().ranks):
            for j, card in enumerate(rank.hand.cards):
                self.cardWins.append(CardWin(card, 16 - 6 * i, 12 + j * 8))
                self.cardWins[-1].display()

        for i, card in enumerate(self.gm.get_player_controller().players[self.gm.userId].reserved.cards):
            self.cardWins.append(CardWin(card, 10 + 6 * i, 47))
            self.cardWins[-1].display()

        # player windows
        self.playerWin = []
        for i, player in enumerate(self.gm.get_player_controller().players):
            if player.player_id == self.gm.userId:
                name = 'Player'
            else:
                name = f'CPU#{player.player_id}'
            self.playerWin.append(PlayerWin(player, name, i * 6, 45))
            self.playerWin[-1].display()

        # input window
        self.inputWin.display()

    def take_tokens(self) -> None:
        pass

    def reserve(self) -> None:
        pass

    def buy(self) -> None:
        pass

    def help(self) -> None:
        pass
