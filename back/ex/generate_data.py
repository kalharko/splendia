import numpy as np
import pickle
import copy
from model.game_manager import GameManager
from ai.model_ppo import PPO
from model.token_array import TokenArray
import os
import torch
from model.checker import Checker

def store_state_and_action(game_data, game_manager, action):
    game_state = copy.deepcopy(game_manager)
    game_data.append({"game_state": game_state, "action": action})

def save_data_list(data_list, filename="ex/data/game_state_data_3.pkl"):
    print("Saving data list")
    print("Length of data list: ", len(data_list))
    with open(filename, "wb") as file:
        pickle.dump(data_list, file, protocol=pickle.HIGHEST_PROTOCOL)

def play_game(ppo_agent_1, game_manager, max_steps_per_episode):
    data_list = []
    game_data = []
    temp_game_data_list = []

    for episode in range(max_steps_per_episode):
        try:
            print("Game: ", episode)
            game_manager.launch_game(2)
            done = False
            pass_count = 0

            while not done:
                currentPlayer = game_manager.currentPlayer
                state = game_manager.gather_ia_board_state(currentPlayer)
                player_string = 'player2'
                opponent_string = 'player1'                
                obs = game_manager.from_board_state_to_obs(opponent_string, player_string, state)

                if currentPlayer == 0:
                    action, _, _, _ = ppo_agent_1.select_action(torch.tensor(obs, dtype=torch.float), state)
                    if 15 <= action <= 29:
                        temp_game_data_list.append({"game_state": copy.deepcopy(game_manager), "action": None})
                        for temp_game_data in temp_game_data_list:
                            temp_game_data['action'] = action
                            game_data.append(temp_game_data)
                        temp_game_data_list.clear() 
                    else:
                  
                        temp_game_data_list.append({"game_state": copy.deepcopy(game_manager), "action": None})
                else:
                    mask = get_mask(state, currentPlayer)
                    valid_actions = np.where(mask == 1)[0]
                    if len(valid_actions) > 0:
                        action = np.random.choice(valid_actions)
                    else:
                        action = 65  

                if action == 65:
                    pass_count += 1
                else:
                    pass_count = 0

                if pass_count == 2:
                    print('Game got stuck, ending game')
                    done = True
                    break

                if not isinstance(action, int):
                    action = int(action)

                game_manager.apply_action(action)
                done = game_manager.is_last_turn()

        except Exception as e:
            print(f"Error encountered in game {episode}: {e}")

        data_list.append(game_data)
    save_data_list(data_list)

def main():
    game_manager = GameManager(nbPlayer=2)
    state_dim = 88  
    action_dim = 66 

    # PPO hyperparameters (adjust as needed)
    lr_actor = 0.0002
    lr_critic = 0.001
    gamma = 0.99
    K_epochs = 80
    eps_clip = 0.2
    action_std = 0.6

    ppo_agent_1 = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip, False, action_std, 1)

    champion_path = "Champion/champion_0.pth"
    if os.path.exists(champion_path):
        ppo_agent_1.load(champion_path)

    play_game(ppo_agent_1, game_manager, max_steps_per_episode=3)
    
def normalize_obs(obs):
    new_obs = np.zeros(88)
    """
    Player 1 state:
    5 tokens: 0-4
    1 gold token: 5
    20 player cards: 6-25
    5 noble cards: 26-30
    3 reserved cards: 31-33

    Player 2 state:
    5 tokens: 34-38
    1 gold token: 39
    20 player cards: 40-59
    5 noble cards: 60-64
    3 reserved cards: 65-67

    Shop state:
    12 cards: 68-79
    5 noble cards: 80-84
    1 tier 1 number of cards: 85
    1 tier 2 number of cards: 86
    1 tier 3 number of cards: 87

    """
    new_obs[0:6] = obs[0:6] / 10
    new_obs[6:26] = obs[6:26] / 90
    new_obs[26:31] = obs[26:31] / 10
    new_obs[31:34] = obs[31:34] / 90

    new_obs[34:40] = obs[34:40] / 10
    new_obs[40:60] = obs[40:60] / 90
    new_obs[60:65] = obs[60:65] / 10
    new_obs[65:68] = obs[65:68] / 90

    new_obs[68:80] = obs[68:80] / 90
    new_obs[80:85] = obs[80:85] / 10
    new_obs[85:88] = obs[85:88] / 30

    return new_obs
  
def denormalize_obs(obs):
    new_obs = np.zeros(88)
    new_obs[0:6] = obs[0:6] * 10
    new_obs[6:26] = obs[6:26] * 90
    new_obs[26:31] = obs[26:31] * 10
    new_obs[31:34] = obs[31:34] * 90

    new_obs[34:40] = obs[34:40] * 10
    new_obs[40:60] = obs[40:60] * 90
    new_obs[60:65] = obs[60:65] * 10
    new_obs[65:68] = obs[65:68] * 90

    new_obs[68:80] = obs[68:80] * 90
    new_obs[80:85] = obs[80:85] * 10
    new_obs[85:88] = obs[85:88] * 30

    return new_obs
  
def get_mask(state, playerId):
    if playerId == 0:
        player_str = 'player2'
    else:
        player_str = 'player2'
    # read the pickle
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
  

if __name__ == '__main__':
    main()
