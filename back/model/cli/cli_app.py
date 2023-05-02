import curses
import locale

from model.business_model.game_manager import GameManager
from model.cli.objects_win import PatronWin, CardWin, PlayerWin, InputWin


class CliApp():
    def __init__(self, nbPlayer: int, stdscr) -> None:
        # encoding
        # locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        # self.code = locale.getpreferredencoding()
        # curses.curs_set(0)

        # game
        self.gm = GameManager(nbPlayer)
        self.gm.launch_game(nbPlayer)

        # constants
        self.ESCAPE = ['q']
        self.SCREEN_HEIGHT = 47
        self.MIN_SIZE = (23, 67)

        # colors
        curses.init_pair(1, 232, 1)  # white
        curses.init_pair(2, 22, 1)  # blue
        curses.init_pair(3, 41, 1)  # green
        curses.init_pair(4, 197, 1)  # red
        curses.init_pair(5, 9, 1)  # black
        curses.init_pair(6, 221, 1)  # yellow

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
        self.screen = stdscr
        self.screenH, self.screenW = self.screen.getmaxyx()
        if self.screenH < self.MIN_SIZE[0] or self.screenW < self.MIN_SIZE[1]:
            print('console too small' + str((self.screenH, self.screenW)))
            quit()
        self.inputWin = InputWin()

        # main loop
        self.main_loop()

        # exit
        self.screen.erase()
        self.screen.refresh()

    def main_loop(self) -> None:
        while True:
            self.display()
            self.display()
            user_input = self.get_input('=>')
            if user_input in self.ESCAPE:
                break
            elif user_input[0] in self.COMMANDS.keys():
                self.COMMANDS[user_input[0]](user_input[1:])
            else:
                pass

    def get_input(self, message="") -> list[str]:
        self.inputWin.display(message)

        out = ''
        newchar = self.screen.get_wch()
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
            newchar = self.screen.get_wch()

        self.inputWin.display('')
        return out

    def display(self) -> None:
        self.screen.erase()
        self.screen.border()

        # # patron windows
        # self.patronWins = [PatronWin(patron, y, 0) for patron, y in zip(self.gm.get_patron_controller().patrons, (3, 8, 13, 18, 23))]
        # for patronWin in self.patronWins:
        #     patronWin.display()

        # # card windows
        # self.cardWins = []
        # for i, rank in enumerate(self.gm.get_shop_controller().ranks):
        #     for j, card in enumerate(rank.hand.cards):
        #         self.cardWins.append(CardWin(card, 16 - 6 * i, 12 + j * 8))
        #         self.cardWins[-1].display()

        # for i, card in enumerate(self.gm.get_player_controller().players[self.gm.userId].reserved.cards):
        #     self.cardWins.append(CardWin(card, 10 + 6 * i, 47))
        #     self.cardWins[-1].display()

        # # player windows
        # self.playerWin = []
        # for i, player in enumerate(self.gm.get_player_controller().players):
        #     if player.player_id == self.gm.userId:
        #         name = 'Player'
        #     else:
        #         name = f'CPU#{player.player_id}'
        #     self.playerWin.append(PlayerWin(player, name, i * 6, 45))
        #     self.playerWin[-1].display()

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
