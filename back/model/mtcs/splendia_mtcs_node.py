from copy import copy, deepcopy
import numpy
import random
from model.mtcs.monte_carlo_tree_search import Node
from model.game_manager import GameManager
from model.token_array import TokenArray
from model.checker import Checker
from tqdm import tqdm
import multiprocessing as mp
import time
class SplendiaMtcsNode(GameManager, Node):
    """
    This class is a node for the tree of the Monte Carlo Tree Search algorithm / Alpha beta algorithm.
    It is a copy of the GameManager class, with some additional attributes and methods.

    Attributes:
        has_pass: True if the player has passed his turn, False otherwise
        depth: the depth of the node in the tree
        max_depth: the maximum depth of the tree
        finished: True if the game is finished, False otherwise
        _bankController: the bank controller of the game
        _patronController: the patron controller of the game
        _playerController: the player controller of the game
        _shopController: the shop controller of the game
        currentPlayer: the current player
        nbPlayer: the number of players
        userId: the id of the user
        firstPlayerId: the id of the first player
        scopePlayer: the id of the player for which the tree is built
        parent_action: the action that led to this node
        child: the childrens of this node

    """
    def __init__(self, other: GameManager, scopePlayer: int, depth: int, has_pass=False, max_depth: int = 30):
        self.has_pass = has_pass
        self.depth = depth
        self.max_depth = max_depth

        self.finished = False
        assert isinstance(other, GameManager)
        assert 0 <= scopePlayer < 4
        self._bankController = deepcopy(other._bankController)
        self._patronController = deepcopy(other._patronController)
        self._playerController = deepcopy(other._playerController)
        self._shopController = deepcopy(other._shopController)
        self.currentPlayer = (other.currentPlayer)
        self.nbPlayer = (other.nbPlayer)
        self.userId = (other.userId)
        self.firstPlayerId = (other.firstPlayerId)
        self.scopePlayer = scopePlayer
        self.parent_action = None
        self.child: list[SplendiaMtcsNode] = []
        # self.find_children()

    def find_children(self):  # -> list[SplendiaMtcsNode]
        """
        Find the children of the node, and add them to the child attribute.
        """
        if self.is_terminal():
            return

        action_possible = self.get_possible_actions()
        for action in action_possible:
            state_copy = SplendiaMtcsNode(self, self.scopePlayer, self.depth + 1, self.has_pass)
            state_copy.parent_action = action

            self.child.append(state_copy)

    def evaluate_children(self):
        """
        Evaluate the children of the node, and add them to the child attributes

        """
        if self.is_terminal():
            return
        for child in self.child:
            child.apply_action(child.parent_action)

    def find_random_child(self):

        if self.is_terminal():
            return None
        out = SplendiaMtcsNode(self)
        out.make_random_move()
        return out

    def is_terminal(self) -> bool:
        return (self.is_last_turn() and self.currentPlayer == self.firstPlayerId)

    def evaluate(self) -> float:
        if self.is_terminal():
            return self.reward()
        else:
            return self.get_current_player().victoryPoints.value

    def reward(self) -> int:
        assert self.is_terminal(), 'reward called on non terminal board'

        victoryPoints = [player.victoryPoints.value for player in self._playerController.players]
        ties = [1 if points == max(victoryPoints) else 0 for points in victoryPoints]
        if sum(ties) == 1:
            if self.scopePlayer == victoryPoints.index(max(victoryPoints)):
                return 1  # the scope player won, reward = 1
            else:
                return 0  # the scope player lose, reward = 0
        elif victoryPoints[self.scopePlayer] == max(victoryPoints):
            return 0.5  # the scope player is in a tie, reward = 0.5
        else:
            return 0  # the scope player lose, reward = 0

    def __key(self) -> tuple:
        out = []
        # shop information
        for i in range(3):
            for j in range(4):
                out.append(self._shopController.ranks[i].hand.cards[j].card_id)
        # players information
        for i in range(self.nbPlayer):
            # tokens
            for j in range(6):
                out.append(self._playerController.players[i].tokens.get_tokens()[j])
            # cards
            for j in range(len(self._playerController.players[i].hand.cards)):
                out.append(self._playerController.players[i].hand.cards[j].card_id)
            # reserved cards
            for j in range(len(self._playerController.players[i].reserved.cards)):
                out.append(self._playerController.players[i].reserved.cards[j].card_id)
            # patrons
            for j in range(len(self._playerController.players[i].patrons)):
                out.append(self._playerController.players[i].patrons[j].patron_id)
        # patron information
        for i in range(len(self._patronController.patrons)):
            out.append(self._patronController.patrons[i].patron_id)
        return tuple(out)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, SplendiaMtcsNode):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def possible_cards_to_buy(self) -> list[int]:
        out = []
        for rank in self._shopController.ranks:
            for card in rank.hand.cards:
                if self.get_current_player().can_pay_with_reduced_price(card.price):
                    out.append(card.card_id)

        for card in self.get_current_player().reserved.cards:
            if self.get_current_player().can_pay_with_reduced_price(card.price):
                out.append(card.card_id)
        return out

    def possible_cards_to_reserve(self) -> list[int]:
        out = []
        for rank in self._shopController.ranks:
            for card in rank.hand.cards:
                out.append(card.card_id)
        return out

    def possible_tokens_to_take(self) -> list[TokenArray]:
        out = []
        combinations = {
            TokenArray([1, 1, 1, 0, 0, 0]),
            TokenArray([1, 1, 0, 1, 0, 0]),
            TokenArray([1, 1, 0, 0, 1, 0]),
            TokenArray([1, 0, 1, 1, 0, 0]),
            TokenArray([1, 0, 1, 0, 1, 0]),
            TokenArray([1, 0, 0, 1, 1, 0]),
            TokenArray([0, 1, 1, 1, 0, 0]),
            TokenArray([0, 1, 1, 0, 1, 0]),
            TokenArray([0, 1, 0, 1, 1, 0]),
            TokenArray([0, 0, 1, 1, 1, 0]),
            TokenArray([2, 0, 0, 0, 0, 0]),
            TokenArray([0, 2, 0, 0, 0, 0]),
            TokenArray([0, 0, 2, 0, 0, 0]),
            TokenArray([0, 0, 0, 2, 0, 0]),
            TokenArray([0, 0, 0, 0, 2, 0]),
        }
        for comb in combinations:
            if self._bankController.can_withdraw((comb)):
                out.append(comb)
        return out

    def make_random_move(self) -> None:
        possible_actions = self.get_possible_actions()


        for action in possible_actions:
            # copy the state
            state_copy = SplendiaMtcsNode(self, 2, self.depth + 1, self.has_pass)
            # apply the action
            state_copy.apply_action(action)
            (state_copy).parent_action = action
            # put the state in the tree
            self.child.append(state_copy)
        for child in self.child:
            if child.finished == False and child.is_last_turn() == False:
                child.make_random_move()
        # select a random action from the possible actions
        # get the action from the random action

    def get_possible_actions(self):
        # get the attributes of the get_mask function
        state = self.gather_ia_board_state()
        player_str = 'player' + str(self.currentPlayer + 1)
        # read the pickle
        mask = numpy.zeros(88)
        shop_cards_rank1 = state['shop']['rank1_cards']
        shop_cards_rank2 = state['shop']['rank2_cards']
        shop_cards_rank3 = state['shop']['rank3_cards']
        # if the shop of rank 1 is empty, padd the shop with none
        if len(shop_cards_rank1) != 4:
            # padd with none shop_cards_rank1 until it has 4 cards
            for i in range(4 - len(state['shop']['rank1_cards'])):
                shop_cards_rank1.append(None)
        # if the shop of rank 2 is empty, padd the shop with none
        if len(shop_cards_rank2) != 4:
            for i in range(4 - len(state['shop']['rank2_cards'])):
                shop_cards_rank2.append(None)
        # if the shop of rank 3 is empty, padd the shop with none
        if len(shop_cards_rank3) != 4:
            for i in range(4 - len(state['shop']['rank3_cards'])):
                shop_cards_rank3.append(None)
        # remove the none from the reserved cards
        number_card_reserved = len(
            [x for x in state[player_str]['reserved'] if x is not None])
        shop_cards = [shop_cards_rank1, shop_cards_rank2, shop_cards_rank3]
        mask = Checker.get_mask(state[player_str]['cards'], shop_cards, state['shop']['rank1_size'],
                                state['shop']['rank2_size'], state['shop']['rank3_size'], number_card_reserved,
                                TokenArray(state[player_str]['tokens']), state['shop']['tokens'],
                                state[player_str]['reserved'],
                                state[player_str]['object'])
        # print(mask)
        # get the possible actions, i.e where the mask is 1
        possible_actions = numpy.where(mask == 1)[0]
        return possible_actions

    def simulate_monte_carlo(self, player_id):
        # while the game is not finished
        is_finish = False
        number_iteration = 0
        self.last_action_done = -1
        current_node = copy(self)
        while not is_finish:
            # choose a random action
            number_iteration += 1
            possible_actions = current_node.get_possible_actions()
            # check if possible_actions contains only 65




            # take a random action
            action = random.choice(possible_actions)
            if action == 65 and self.last_action_done == 65:
                return -1  ,number_iteration # if the last action was pass and the current action is pass, return -1
            self.last_action_done = action
            # apply the action
            current_node.apply_action(action)
            # check if the game is finished
            if current_node.currentPlayer == current_node.firstPlayerId and current_node.is_last_turn() == True:

                # return the winner
                if current_node._playerController.players[player_id].victoryPoints.value > current_node._playerController.players[(player_id + 1) % 2].victoryPoints.value:
                    return 1 , number_iteration
                elif current_node._playerController.players[player_id].victoryPoints.value == current_node._playerController.players[(player_id + 1) % 2].victoryPoints.value:
                    return 0 , number_iteration
                else:
                    return 0.5 , number_iteration

            #print('number iteration : ', number_iteration)

    def is_leaf(self):
        return len(self.get_possible_actions()) == 0

    def stop_game(self):
        self.finished = True

    def apply_action(self, action):
        # print the action done
        # print('action done : ', action)
        if action == 0:
            # take [1,1,1,0,0,0] tokens
            self.take_token(TokenArray([1, 1, 1, 0, 0, 0]))
        elif action == 1:
            # take [1,1,0,1,0,0] tokens
            self.take_token(TokenArray([1, 1, 0, 1, 0, 0]))
        elif action == 2:
            # take [1,1,0,0,1,0] tokens
            self.take_token(TokenArray([1, 1, 0, 0, 1, 0]))
        elif action == 3:
            # take [1,0,1,1,0,0] tokens
            self.take_token(TokenArray([1, 0, 1, 1, 0, 0]))
        elif action == 4:
            # take [1,0,1,0,1,0] tokens
            self.take_token(TokenArray([1, 0, 1, 0, 1, 0]))
        elif action == 5:
            # take [1,0,0,1,1,0] tokens
            self.take_token(TokenArray([1, 0, 0, 1, 1, 0]))
        elif action == 6:
            # take [0,1,1,1,0,0] tokens
            self.take_token(TokenArray([0, 1, 1, 1, 0, 0]))
        elif action == 7:
            # take [0,1,1,0,1,0] tokens
            self.take_token(TokenArray([0, 1, 1, 0, 1, 0]))
        elif action == 8:
            # take [0,1,0,1,1,0] tokens
            self.take_token(TokenArray([0, 1, 0, 1, 1, 0]))
        elif action == 9:
            # take [0,0,1,1,1,0] tokens
            self.take_token(TokenArray([0, 0, 1, 1, 1, 0]))
        elif action == 10:
            self.take_token(TokenArray([2, 0, 0, 0, 0, 0]))
        elif action == 11:
            self.take_token(TokenArray([0, 2, 0, 0, 0, 0]))
        elif action == 12:
            self.take_token(TokenArray([0, 0, 2, 0, 0, 0]))
        elif action == 13:
            self.take_token(TokenArray([0, 0, 0, 2, 0, 0]))
        elif action == 14:
            self.take_token(TokenArray([0, 0, 0, 0, 2, 0]))
        elif action == 15:
            self.buy_card(self._shopController.ranks[0].hand.cards[0].card_id)
        elif action == 16:
            self.buy_card(self._shopController.ranks[0].hand.cards[1].card_id)
        elif action == 17:
            self.buy_card(self._shopController.ranks[0].hand.cards[2].card_id)
        elif action == 18:
            self.buy_card(self._shopController.ranks[0].hand.cards[3].card_id)
        elif action == 19:
            self.buy_card(self._shopController.ranks[1].hand.cards[0].card_id)
        elif action == 20:
            self.buy_card(self._shopController.ranks[1].hand.cards[1].card_id)
        elif action == 21:
            self.buy_card(self._shopController.ranks[1].hand.cards[2].card_id)
        elif action == 22:
            self.buy_card(self._shopController.ranks[1].hand.cards[3].card_id)
        elif action == 23:
            self.buy_card(self._shopController.ranks[2].hand.cards[0].card_id)
        elif action == 24:
            self.buy_card(self._shopController.ranks[2].hand.cards[1].card_id)
        elif action == 25:
            self.buy_card(self._shopController.ranks[2].hand.cards[2].card_id)
        elif action == 26:
            self.buy_card(self._shopController.ranks[2].hand.cards[3].card_id)
        elif action == 27:
            self.buy_card(self.get_current_player().reserved.cards[0].card_id)
        elif action == 28:
            self.buy_card(self.get_current_player().reserved.cards[1].card_id)
        elif action == 29:
            self.buy_card(self.get_current_player().reserved.cards[2].card_id)
        elif action == 30:
            self.reserve_card(self._shopController.ranks[0].hand.cards[0].card_id)
        elif action == 31:
            self.reserve_card(self._shopController.ranks[0].hand.cards[1].card_id)
        elif action == 32:
            self.reserve_card(self._shopController.ranks[0].hand.cards[2].card_id)
        elif action == 33:
            self.reserve_card(self._shopController.ranks[0].hand.cards[3].card_id)
        elif action == 34:
            self.reserve_card(self._shopController.ranks[1].hand.cards[0].card_id)
        elif action == 35:
            self.reserve_card(self._shopController.ranks[1].hand.cards[1].card_id)
        elif action == 36:
            self.reserve_card(self._shopController.ranks[1].hand.cards[2].card_id)
        elif action == 37:
            self.reserve_card(self._shopController.ranks[1].hand.cards[3].card_id)
        elif action == 38:
            self.reserve_card(self._shopController.ranks[2].hand.cards[0].card_id)
        elif action == 39:
            self.reserve_card(self._shopController.ranks[2].hand.cards[1].card_id)
        elif action == 40:
            self.reserve_card(self._shopController.ranks[2].hand.cards[2].card_id)
        elif action == 41:
            self.reserve_card(self._shopController.ranks[2].hand.cards[3].card_id)
        elif action == 42:
            self.reserve_pile_card(0)
        elif action == 43:
            self.reserve_pile_card(1)
        elif action == 44:
            self.reserve_pile_card(2)
        elif action == 45:
            self.take_token(TokenArray([1, 0, 0, 0, 0, 0]))
        elif action == 46:
            self.take_token(TokenArray([0, 1, 0, 0, 0, 0]))
        elif action == 47:
            self.take_token(TokenArray([0, 0, 1, 0, 0, 0]))
        elif action == 48:
            self.take_token(TokenArray([0, 0, 0, 1, 0, 0]))
        elif action == 49:
            self.take_token(TokenArray([0, 0, 0, 0, 1, 0]))
        elif action == 50:
            self.take_token(TokenArray([1, 1, 0, 0, 0, 0]))
        elif action == 51:
            self.take_token(TokenArray([1, 0, 1, 0, 0, 0]))
        elif action == 52:
            self.take_token(TokenArray([1, 0, 0, 1, 0, 0]))
        elif action == 53:
            self.take_token(TokenArray([1, 0, 0, 0, 1, 0]))
        elif action == 54:
            self.take_token(TokenArray([0, 1, 1, 0, 0, 0]))
        elif action == 55:
            self.take_token(TokenArray([0, 1, 0, 1, 0, 0]))
        elif action == 56:
            self.take_token(TokenArray([0, 1, 0, 0, 1, 0]))
        elif action == 57:
            self.take_token(TokenArray([0, 0, 1, 1, 0, 0]))
        elif action == 58:
            self.take_token(TokenArray([0, 0, 1, 0, 1, 0]))
        elif action == 59:
            self.take_token(TokenArray([0, 0, 0, 1, 1, 0]))
        elif action == 60:
            self.take_token(TokenArray([2, 0, 0, 0, 0, 0]))
        elif action == 61:
            self.take_token(TokenArray([0, 2, 0, 0, 0, 0]))
        elif action == 62:
            self.take_token(TokenArray([0, 0, 2, 0, 0, 0]))
        elif action == 63:
            self.take_token(TokenArray([0, 0, 0, 2, 0, 0]))
        elif action == 64:
            self.take_token(TokenArray([0, 0, 0, 0, 2, 0]))
        elif action == 65:
            if self.has_pass:
                self.stop_game()
            else:
                self.has_pass = True
                self.pass_turn()


def alpha_beta(node, depth, alpha, beta, maximizing_player=True):
    global pruned_branches  # for debugging
    if depth == 0 or node.is_terminal():
        #print(' evaluate : ', node.evaluate())
        return node.evaluate(), []
    node.find_children()
    iterator = 0
    for action in node.get_possible_actions():
        node.child[iterator].apply_action(action)
        node.child[iterator].parent_action = action

        iterator += 1
    if maximizing_player:
        best_value = float('-inf')
        best_path = []

        for child in node.child:

            child_value, child_path = alpha_beta(child, depth - 1, alpha, beta, False)
            if child_value > best_value:
                best_value = child_value
                best_path = [child.parent_action] + child_path
            alpha = max(alpha, best_value)
            if beta <= alpha:
                pruned_branches += 1
                break

        return best_value, best_path

    else:
        best_value = float('inf')
        best_path = []

        for child in node.child:
            child_value, child_path = alpha_beta(child, depth - 1, alpha, beta, True)
            if child_value < best_value:
                best_value = child_value
                best_path = [child.parent_action] + child_path
            beta = min(beta, best_value)
            if beta <= alpha:
                pruned_branches += 1
                break

        return best_value, best_path


def monte_carlo(node: SplendiaMtcsNode, nb_simulations, current_player):
    node.find_children()
    node_child = node.child
    manager = mp.Manager()
    results = manager.dict()
    procs = []


    for child in node_child:
        proc = mp.Process(target=compute_random_game_reward, args=(child, current_player, nb_simulations, results))
        procs.append(proc)
        proc.start()
        #compute_random_game_reward(child, current_player, nb_simulations, results)
        print(f"Simulating action {child.parent_action}")


    for proc in procs:
        proc.join()

    # get the best action
    best_reward = -float('inf')
    best_action = None
    for child in node_child:
        reward = results[child.parent_action]
        if reward > best_reward:
            best_reward = reward
            best_action = child.parent_action

    print(f"Best action: {best_action}")
    print(f"Best reward: {best_reward}")
    return best_action

def compute_random_game_reward(child, current_player, nb_simulations, results):
    reward_list = []
    for i in range(nb_simulations):
        copy = deepcopy(child)
        reward, _ = copy.simulate_monte_carlo(current_player)
        reward_list.append(reward)

    avg_reward = sum(reward_list) / len(reward_list)
    results[child.parent_action] = avg_reward

    print(f"Average reward for action {child.parent_action}: {avg_reward}")


if __name__ == '__main__':
    pruned_branches = 0
    # get time
    start_time = time.time()
    first_state = GameManager(nbPlayer=2)
    node = SplendiaMtcsNode(first_state, 2, 0, False, 9)
    number_actions = 50
    for i in range(number_actions):

        possible_actions = node.get_possible_actions()
        # get a random action
        action = random.choice(possible_actions)
        node.apply_action(action)
    print()
    dummy = copy(node)
    print(monte_carlo(dummy, 100, 0))
    print("--- %s seconds ---" % (time.time() - start_time))
    # node.find_children()
    dummy = copy(node)
    #dummy.find_children()
    player = True if node.currentPlayer == 0 else False
    best_value, best_path = alpha_beta(dummy, 4, float('-inf'), float('inf'), player)
    print(f"Optimal path for 4 : {best_path}")
    dummy = SplendiaMtcsNode(node, 2, 0, False, 9)
    #dummy.find_children()
    best_value, best_path = alpha_beta(dummy, 7, float('-inf'), float('inf'), player)
    print(f"Optimal path for 6 : {best_path}")


    print(f"Optimal value: {best_value}")
    print("Actions to take:")
    for action in best_path:
        print(action)
    print(f"Number of pruned branches: {pruned_branches}")
