import os
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from model.game_manager import GameManager
from ai.model_ppo import PPO
from model.token_array import TokenArray
from model.checker import Checker
import copy
import matplotlib.pyplot as plt

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

class Classifier(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(Classifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes),
            # nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)

# Custom dataset
class GameDataset(Dataset):
    def __init__(self, data_list):
        self.data = data_list

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data[idx]
        game_state = data['game_state']
        card_id = data['card_id']
        obs = game_state.from_board_state_to_obs('player2', 'player1', game_state.gather_ia_board_state(0))
        return torch.tensor(self.normalize_obs(obs), dtype=torch.float32), torch.tensor(card_id, dtype=torch.long).to(device)

    def normalize_obs(self, obs):
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
    
def play_game(ppo_agent_1, game_manager, max_steps_per_episode):
    data_list = []
    game_data = []
    temp_game_data_list = []  

    for episode in range(max_steps_per_episode):
        try:
            # print("Game: ", episode)
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
                        card_id = get_card_id(game_manager, action)
                        temp_game_data_list.append({"game_state": copy.deepcopy(game_manager), "action": None, "card_id": None})
                        for temp_game_data in temp_game_data_list:
                            temp_game_data['action'] = action
                            temp_game_data['card_id'] = card_id
                            game_data.append(temp_game_data)
                        temp_game_data_list.clear()  
                    else:
                        temp_game_data_list.append({"game_state": copy.deepcopy(game_manager), "action": None, "card_id": None})
                else:
                    mask = get_mask(state, currentPlayer)
                    valid_actions = np.where(mask == 1)[0]  # Get indices of valid actions
                    if len(valid_actions) > 0:
                        action = np.random.choice(valid_actions)  # Choose random valid action
                    else:
                        action = 65  # Default action if no valid actions are available


                if action == 65:
                    pass_count += 1
                else:
                    pass_count = 0

                if pass_count == 2:
                    # print('Game got stuck, ending game')
                    done = True
                    break

                if not isinstance(action, int):
                    action = int(action)

                game_manager.apply_action(action)
                done = game_manager.is_last_turn()

        except Exception as e:
            pass
            # print(f"Error encountered in game {episode}: {e}")

    data_list.append(game_data)
    flattened_data = [item for sublist in data_list for item in sublist]
    return flattened_data

def generate_data_for_epoch(ppo_agent, game_manager, steps_per_episode):
    return play_game(ppo_agent, game_manager, steps_per_episode)

def evaluate_model(model, data_loader):
    model.eval() 
    total = 0
    correct = 0
    with torch.no_grad():
        for game_states, actions in data_loader:
          
            game_states = game_states.to(device)
            actions = actions.to(device) 
            
            outputs = model(game_states)
            _, predicted = torch.max(outputs.data, 1)
            total += actions.size(0)
            correct += (predicted == actions).sum().item()

    accuracy = 100 * correct / total
    return accuracy    
 
def main():
    game_manager = GameManager(nbPlayer=2)
    state_dim = 88  # Update this based on your state dimension
    action_dim = 66  # Update this if your action space size is different

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
        
    training_data = generate_data_for_epoch(ppo_agent_1, game_manager, steps_per_episode=500)
    validation_data = generate_data_for_epoch(ppo_agent_1, game_manager, steps_per_episode= 100)

    train_dataset = GameDataset(training_data)
    train_loader = DataLoader(train_dataset, batch_size=500, shuffle=True)

    validation_dataset = GameDataset(validation_data)
    validation_loader = DataLoader(validation_dataset, batch_size=100)
    
    
    model_path = 'ex/classifier_model.pth'
    if os.path.exists(model_path):
        model = Classifier(input_dim=88, num_classes=90).to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        print("Loaded existing model.")
    else:
        model = Classifier(input_dim=88, num_classes=90).to(device)
        print("Created new model.")
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0002)

    training_losses = []
    validation_losses = []
    validation_accuracies = []

    num_epochs = 500
    regenerate_interval = 30
    # regenerate_validation_interval = 10
    
    for epoch in range(num_epochs):
        # Regenerate training data at specified intervals
        if epoch % regenerate_interval == 0:
            training_data = generate_data_for_epoch(ppo_agent_1, game_manager, steps_per_episode=500)
            train_dataset = GameDataset(training_data)
            train_loader = DataLoader(train_dataset, batch_size=500, shuffle=True)
        # if epoch % regenerate_validation_interval == 0:
        #     validation_data = generate_data_for_epoch(ppo_agent_1, game_manager, steps_per_episode=100)
        #     validation_dataset = GameDataset(validation_data)
        #     validation_loader = DataLoader(validation_dataset, batch_size=32)
      
        model.train()
        epoch_loss = 0.0
        for game_states, actions in train_loader:
          
            game_states = game_states.to(device)
            actions = actions.to(device)
            
            optimizer.zero_grad()
            outputs = model(game_states)
            loss = criterion(outputs, actions)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        avg_epoch_loss = epoch_loss / len(train_loader)
        training_losses.append(avg_epoch_loss)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_epoch_loss}")
        
        if validation_loader:
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for game_states, actions in validation_loader:
                    game_states = game_states.to(device)
                    actions = actions.to(device)
                    outputs = model(game_states)
                    loss = criterion(outputs, actions)
                    val_loss += loss.item()

            avg_val_loss = val_loss / len(validation_loader)
            validation_losses.append(avg_val_loss)
            print(f"Validation Loss: {avg_val_loss}")

            accuracy = evaluate_model(model, validation_loader)
            validation_accuracies.append(accuracy)
            print(f"Validation Accuracy: {accuracy}%")

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, num_epochs+1), training_losses, label='Training Loss')
    plt.plot(range(1, num_epochs+1), validation_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(range(1, num_epochs+1), validation_accuracies, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Validation Accuracy')
    plt.legend()

    plt.show()

    torch.save(model.state_dict(), 'ex/classifier_model.pth')

def get_mask(state, playerId):
    if playerId == 0:
        player_str = 'player2'
    else:
        player_str = 'player2'
    mask = np.zeros(88)
    shop_cards_rank1 = state['shop']['rank1_cards']
    shop_cards_rank2 = state['shop']['rank2_cards']
    shop_cards_rank3 = state['shop']['rank3_cards']
    if len(shop_cards_rank1) != 4:
        for i in range(4 - len(state['shop']['rank1_cards'])):
            shop_cards_rank1.append(None)

    if len(shop_cards_rank2) != 4:
        for i in range(4 - len(state['shop']['rank2_cards'])):
            shop_cards_rank2.append(None)
    if len(shop_cards_rank3) != 4:
        for i in range(4 - len(state['shop']['rank3_cards'])):
            shop_cards_rank3.append(None)
    number_card_reserved = len(
        [x for x in state[player_str]['reserved'] if x is not None])
    shop_cards = [shop_cards_rank1, shop_cards_rank2, shop_cards_rank3]

    mask = Checker.get_mask(state[player_str]['cards'], shop_cards, state['shop']['rank1_size'],
                            state['shop']['rank2_size'], state['shop']['rank3_size'], number_card_reserved,
                            TokenArray(state[player_str]['tokens']), state['shop']['tokens'],
                            state[player_str]['reserved'],
                            state[player_str]['object'])

    return mask

  
def get_card_id(game_manager, action):
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

if __name__ == '__main__':
    main()