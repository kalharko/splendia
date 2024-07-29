from ai.environment import SplendorEnv
from model.game_manager import GameManager
from ai.model_ppo import PPO
import torch
from model.checker import Checker
import numpy as np
import copy
from model.token_array import TokenArray
from collections import defaultdict

class TreeNode:
    def __init__(self, game_manager, action, is_player_turn, prob=0, card_id= None):
        self.game_manager = game_manager
        self.action = action
        self.card_id = card_id
        self.is_player_turn = is_player_turn
        self.children = []
        self.ppo_value = None
        self.prob = prob
        
        
    

class ExplainByCriticTree:
    def __init__(self, game_manager : GameManager):
        self.root = None
        champion_path = "Champion/champion_0.pth"

        state_dim = 88
        action_dim = 66
        has_continuous_action_space = False

        lr_actor = 0.0002
        lr_critic = 0.001
        gamma = 0.99
        K_epochs = 80
        eps_clip = 0.2
        playerId = 1
        action_std_init = 0.6

        self.ppo_critic = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip,
                              has_continuous_action_space, action_std_init, playerId)

        self.ppo_critic.load(champion_path)
        

    def build_tree(self, game_manager, depth, max_depth, is_player_turn, parent_prob=1, parent_node=None):
        if parent_node is None:
            node = TreeNode(game_manager, None, is_player_turn, prob=parent_prob)
        else:
            node = parent_node

        if depth == max_depth:
            return node

        # print('=====================')
        action_logprobs_np = self.evaluate_board_state(node)

        for action_index, prob in enumerate(action_logprobs_np):
            if prob != 0:  # Check if the action is viable
                next_game_manager = copy.deepcopy(game_manager)
                next_game_manager = self.play_move(next_game_manager, action_index, 0 if is_player_turn else 1)
                
                card_id = None
                if action_index >= 15 or action_index <= 29:
                    card_id = self.get_card_id(game_manager, action_index)
        
                child_node = TreeNode(next_game_manager, action_index, not is_player_turn, card_id=card_id)
                
                child_node.ppo_value = prob
                node.children.append(child_node)

        if depth < max_depth:
            if depth % 2 == 1:
                child_prob = parent_prob / len(node.children) if node.children else 0
                for child in node.children:
                    child.prob = child_prob
                    self.build_tree(child.game_manager, depth + 1, max_depth, not is_player_turn, child_prob, child)
            else:
                best_child_node = self.get_highest_value_child(node)
                for child in node.children:
                    child.prob = parent_prob if child is best_child_node else 0
                if best_child_node:
                    self.build_tree(best_child_node.game_manager, depth + 1, max_depth, not is_player_turn, parent_prob, best_child_node)

        return node



    
    def get_highest_value_child(self, node):
        highest_ppo_value = float('-inf')
        best_ppo_child = None
        for child in node.children:
            if child.ppo_value is not None and child.ppo_value > highest_ppo_value:
                highest_ppo_value = child.ppo_value
                best_ppo_child = child
        return best_ppo_child

    # def explore_moves_recursive(self, node, is_maximizing_player, return_best_node=False):
    #     if not node.children:
    #         return node.value if node.is_player_turn else None

    #     best_value = float('-inf') if is_maximizing_player else float('inf')
    #     best_move = None
    #     best_node = None

    #     for child in node.children:
    #         value = self.explore_moves_recursive(child, not is_maximizing_player, return_best_node=return_best_node)

    #         if value is not None:
    #             if is_maximizing_player and value > best_value:
    #                 best_value = value
    #                 best_move = child.action
    #                 best_node = child
    #             elif not is_maximizing_player and value < best_value:
    #                 best_value = value
    #                 best_move = child.action
    #                 best_node = child

    #     if return_best_node:
    #         return best_move, best_node
    #     else:
    #         return best_value if node.is_player_turn else best_move


    def evaluate_board_state(self, node):
        board_state = node.game_manager.gather_ia_board_state(0)  # Assuming player 0
        obs = node.game_manager.from_board_state_to_obs('player2', 'player1', board_state)
        print(obs)

        _, _, _, action_logprobs_np = self.ppo_critic.select_action(torch.tensor(obs, dtype=torch.float), board_state)

        return action_logprobs_np

    def play_move(self, game_manager, action, player_id):
        if player_id == 0:
            player_string = 'player2'
            opponent_string = 'player1'
        else:
            player_string = 'player2'
            opponent_string = 'player1'
            
        
        state = game_manager.gather_ia_board_state(player_id)
        obs = game_manager.from_board_state_to_obs(
        opponent_string, player_string, state)
        # print("action = ", action)
        # print(obs)
        # print("=====================================")
        action_description = game_manager.apply_action(action)
        state2 = game_manager.gather_ia_board_state(player_id)
        new_obs = game_manager.from_board_state_to_obs(
            opponent_string, player_string, state2)
        # print(new_obs)
        # if np.array_equal(obs, new_obs):
        #     print("alerte generale")
        # print("=====================================")
        # print("=====================================")
        # print(action_description)
        
        return game_manager
    
    def get_enemy_moves(self, game_manager):
        legal_moves = self.get_legal_moves(game_manager, 1)
        return legal_moves

    def build_and_explore_tree(self, initial_game_manager, max_depth):
        highest_value_holder = [None]  # To keep track of the highest value
        self.root = self.build_tree(initial_game_manager, 0, max_depth, is_player_turn=True)
        # best_move, best_node = self.explore_moves_recursive(self.root, is_maximizing_player=True, return_best_node=True)

        # print("Value of best_node:", best_node)

        # best_node_children = best_node.children if best_node is not None else []

        # return best_move, best_node_children
        best_ppo = self.get_highest_value_child(self.root)
        
        return best_ppo.action
    
    def get_legal_moves(self, game_manager, player_id=0):
        """
        Get a list of legal moves for the current player.

        Returns:
            List[int]: List of legal moves.
        """
        
        if player_id == 0:
            player_string = 'player2'
            opponent_string = 'player1'
        else:
            player_string = 'player2'
            opponent_string = 'player1'
            
        board_state = game_manager.gather_ia_board_state(player_id)
        obs = game_manager.from_board_state_to_obs(opponent_string, player_string, board_state)

        mask = self.get_mask(board_state, player_id)

        legal_moves = [i for i, val in enumerate(mask) if val == 1]
        return legal_moves

    def get_mask(self, state, playerId):
        if playerId == 0:
            player_str = 'player2'
        else:
            player_str = 'player2'
        mask = np.zeros(88)
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

        return mask
    
    def print_tree(self, node, depth=0):
        if node is None:
            return

        print("  " * depth + f"Depth: {depth}, Action: {node.action}, Prob: {node.prob}, Card_id: {node.card_id}, Number of Children: {len(node.children)}")
        
        for child in node.children:
            self.print_tree(child, depth + 1)
            
            
    def sum_probabilities_by_action(self, node, is_best_child=False, depth=0):
        if node is None:
            return defaultdict(float)

        prob_sum_by_action = defaultdict(float)

        if depth % 2 == 1 and not node.children and is_best_child:
            prob_sum_by_action[node.action] += node.prob

        best_child = self.get_highest_value_child(node)

        for child in node.children:
            child_prob_sums = self.sum_probabilities_by_action(child, child is best_child, depth + 1)
            for action, prob in child_prob_sums.items():
                prob_sum_by_action[action] += prob

        return prob_sum_by_action
    
    def sum_probabilities_by_card_id(self, node, is_best_child=False, depth=0):
        if node is None:
            return defaultdict(float)

        prob_sum_by_card_id = defaultdict(float)

        if depth % 2 == 1 and not node.children and is_best_child and node.card_id is not None:
            prob_sum_by_card_id[node.card_id] += node.prob

        best_child = self.get_highest_value_child(node)

        for child in node.children:
            child_prob_sums = self.sum_probabilities_by_card_id(child, child is best_child, depth + 1)
            for card_id, prob in child_prob_sums.items():
                prob_sum_by_card_id[card_id] += prob

        return prob_sum_by_card_id

    def get_card_id(self, game_manager, action):
        if action == 15:
            return game_manager.shop1_cards[0].cardId
        elif action == 16:
            return game_manager.shop1_cards[1].cardId
        elif action == 17:
            return game_manager.shop1_cards[2].cardId
        elif action == 18:
            return game_manager.shop1_cards[3].cardId
        elif action == 19:
            return game_manager.shop2_cards[0].cardId
        elif action == 20:
            return game_manager.shop2_cards[1].cardId
        elif action == 21:
            return game_manager.shop2_cards[2].cardId
        elif action == 22:
            return game_manager.shop2_cards[3].cardId
        elif action == 23:
            return game_manager.shop3_cards[0].cardId
        elif action == 24:
            return game_manager.shop3_cards[1].cardId
        elif action == 25:
            return game_manager.shop3_cards[2].cardId
        elif action == 26:
            return game_manager.shop3_cards[3].cardId
        elif action == 27:
            return game_manager.reserved_cards[0]
        elif action == 28:
            return game_manager.reserved_cards[1]
        elif action == 29:
            return game_manager.reserved_cards[2]


# game_manager_instance = GameManager(nbPlayer=2)
# environment_instance = SplendorEnv(game_manager_instance)

# explainer_tree = ExplainByCriticTree(game_manager_instance)

# initial_game_manager = game_manager_instance  # Set the initial game state
# max_depth = 2  # Maximum depth for the search tree

# best_move, best_node_children = explainer_tree.build_and_explore_tree(initial_game_manager, max_depth)
# print("Best Move:", best_move)
# print("Children of Best Node:")
# explainer_tree.print_tree(best_node_children)
