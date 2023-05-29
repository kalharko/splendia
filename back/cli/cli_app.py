import curses
import locale

from model.game_manager import GameManager
from model.token_array import TokenArray
from cli.objects_win import PatronWin, CardWin, PlayerWin, InputWin, HistWin
from utils.logger import Logger


class CliApp():
    def __init__(self, nbPlayer: int, stdscr) -> None:
        # encoding
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        curses.curs_set(0)
        if not curses.has_colors():
            exit('Your terminal does not support curses colors')

        # game
        self.gm = GameManager(nbPlayer)
        self.gm.launch_game(nbPlayer)

        # constants
        self.ESCAPE = ['q']
        self.SCREEN_HEIGHT = 47
        self.MIN_SIZE = (23, 67)

        # colors
        curses.init_pair(1, curses.COLOR_WHITE, 0)  # white
        curses.init_pair(2, curses.COLOR_BLUE, 0)  # blue
        curses.init_pair(3, curses.COLOR_GREEN, 0)  # green
        curses.init_pair(4, curses.COLOR_RED, 0)  # red
        curses.init_pair(5, 8, 0)  # black
        curses.init_pair(6, curses.COLOR_YELLOW, 0)  # yellow

        self.COMMANDS = {
            'white': self.take_tokens,
            'blue': self.take_tokens,
            'green': self.take_tokens,
            'red': self.take_tokens,
            'black': self.take_tokens,

            'reserve': self.reserve,
            'reserve_pile': self.reserve_pile,
            'buy': self.buy,
            'h': self.help,
            'help': self.help,
            'restart': self.restart
        }

        # screen
        self.screen = stdscr
        self.screenH, self.screenW = self.screen.getmaxyx()
        if self.screenH < self.MIN_SIZE[0] or self.screenW < self.MIN_SIZE[1]:
            print('console too small' + str((self.screenH, self.screenW)))
            quit()
        self.inputWin = InputWin()
        self.histWin = HistWin(25, 0, self.screenH - 25)
        self.history = ['Game Start']

        # main loop
        self.main_loop()

        # exit
        self.screen.erase()
        self.screen.refresh()

    def main_loop(self) -> None:
        while True:
            self.display()

            # cpu action
            if self.gm.currentPlayer != self.gm.userId:
                self.gm.cpu_turn()
                self.history.append(self.gm.logs[-1])
                self.display()
                continue

            # player action
            user_input = self.get_input('')
            if user_input[0] in self.ESCAPE:
                break
            elif user_input[0] in self.COMMANDS.keys():
                err = self.COMMANDS[user_input[0]](user_input)
                log = 'Player ('
                for w in user_input:
                    log += w + ' '
                log = log[:-1] + ')'

                if err is not None:
                    Logger().log(2, err, 'cli main loop, err returned by GM')
                    log += ' => ' + str(type(err)).split(" '")[1].rstrip("'>").split('.')[-1]
                self.history.append(log)
            else:
                Logger().log(2, self, str(user_input))

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
                    pos_cursor = pos_cursor + \
                        1 if pos_cursor < len(out) else pos_cursor
                elif newchar == curses.KEY_DOWN:  # down arrow
                    pos_cursor = len(out)
                elif newchar == curses.KEY_UP:  # up arrow
                    pos_cursor = 0
                else:
                    Logger().log(2, self.screen.get_wch, str(newchar))
            elif newchar == '\x08':
                if len(out) > 0 and pos_cursor > 0:
                    out = out[:pos_cursor - 1] + out[pos_cursor:]
                    pos_cursor -= 1
            else:
                out = out[:pos_cursor] + newchar + out[pos_cursor:]
                pos_cursor += 1

            self.inputWin.display(out[:pos_cursor] + '_' + out[pos_cursor:])
            newchar = self.screen.get_wch()

        self.inputWin.display('')
        return out.split(' ')

    def display(self) -> None:
        self.screen.erase()
        self.screen.border()
        self.screen.refresh()

        # bank
        tokens = self.gm.get_bank_controller().bank.get_tokens()
        self.screen.addstr(1, 14, 'white blue green red black gold')
        for i in range(6):
            self.screen.addstr(
                2, 15 + i * 5, f'({tokens[i]})', curses.color_pair(i + 1))

        # shop
        yCoords = (17, 11, 5)
        for i in range(3):
            deckSize = str(self.gm.get_shop_controller().ranks[i].deck.get_size())
            self.screen.addstr(yCoords[i], 14 - len(deckSize), deckSize)

        # patron windows
        self.patronWins = [PatronWin(patron, y, 0) for patron, y in zip(
            self.gm.get_patron_controller().patrons, (3, 8, 13, 18, 23))]
        for patronWin in self.patronWins:
            patronWin.display()

        # cpus windows
        self.playerWin = []
        y = 0
        for player in self.gm.get_player_controller().players:
            if player.playerId == self.gm.userId:
                humanPlayer = player
                continue
            name = f'CPU#{player.playerId}'
            self.playerWin.append(PlayerWin(player, name, y * 6 + 1, 47))
            y += 1
            if self.gm.currentPlayer == player.playerId:
                self.playerWin[-1].currentPlayer = True
            self.playerWin[-1].display()

        # player window
        self.playerWin.append(PlayerWin(humanPlayer, 'Player', y * 5 + 1, 47))
        if self.gm.currentPlayer == humanPlayer.playerId:
            self.playerWin[-1].currentPlayer = True
        self.playerWin[-1].display()

        # card windows
        # shop
        self.cardWins = []
        for i, rank in enumerate(self.gm.get_shop_controller().ranks):
            for j, card in enumerate(rank.hand.cards):
                self.cardWins.append(CardWin(card, 16 - 6 * i, 14 + j * 8))
                self.cardWins[-1].display()

        # reserved cards
        positions = ((10, 49), (10, 58), (16, 53))
        for i, card in enumerate(humanPlayer.reserved.cards):
            self.cardWins.append(CardWin(card, positions[i][0], positions[i][1]))
            self.cardWins[-1].display()

        # input window
        self.inputWin.display()

        # history window
        self.histWin.display(self.history)

    def take_tokens(self, user_input: list[str]) -> None:
        """Parse and call game manager take token action.
        Args:
            player_token (list[str]): args given by the user
        Returns:
            None: None or error code from the game manager
            """
        colors = ('white', 'blue', 'green', 'red', 'black')
        if [x in colors for x in user_input] != [True for x in user_input]:
            return
        tokens = [0, 0, 0, 0, 0, 0]
        if len(user_input) == 3:
            for c in user_input:
                tokens[colors.index(c)] = 1
        elif len(user_input) == 1:
            tokens[colors.index(user_input[0])] = 2

        return self.gm.take_token(TokenArray(tokens))

    def reserve(self, user_input: list[str]) -> None:
        """Parse and call game manager reserve action.
        Args:
            player_token (list[str]): args given by the user
        Returns:
            None: None or error code from the game manager
            """
        if len(user_input) != 2:
            return
        if not user_input[1].isdigit():
            return
        cardId = int(user_input[1])

        return self.gm.reserve_card(cardId)

    def reserve_pile(self, user_input: list[str]) -> None:
        """Parse and call game manager reserve pile action.
        Args:
            player_token (list[str]): args given by the user
        Returns:
            None: None or error code from the game manager
            """
        if len(user_input) != 2:
            return
        if not user_input[1].isdigit():
            return

        pile_level = int(user_input[1])
        if pile_level not in (1, 2, 3):
            return

        return self.gm.reserve_pile_card(pile_level - 1)

    def buy(self, user_input: list[str]) -> None:
        """Parse and call game manager buy action.
        Args:
            player_token (list[str]): args given by the user
        Returns:
            None: None or error code from the game manager
            """
        if len(user_input) != 2:
            return
        if not user_input[1].isdigit():
            return
        cardId = int(user_input[1])

        return self.gm.buy_card(cardId)

    def help(self, user_input: list[str]) -> None:
        self.histWin.display([
            'Controls :',
            'color1 color2 color3 => take 3 different colored tokens',
            'color1               => take 2 tokens of the same color',
            'buy cardId           => buy card with id cardId',
            'reserve cardId       => reserve card with id cardId',
            'press any key to quit the help display'
        ][::-1])
        self.screen.getch()

    def restart(self, user_input: list[str]) -> None:
        self.gm = GameManager(self.gm.nbPlayer)
