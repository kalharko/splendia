import pickle
import os
from model.game_manager import GameManager
from ex.critic_explainer import ExplainByCriticTree
import heapq 


def read_and_print_pickle(directory_path):
    files = os.listdir(directory_path)
    success_count_k1 = 0
    success_count_k2 = 0
    success_count_k3 = 0
    total_length = 0
    for file in files:
        if file.endswith('.pkl') and file.startswith('card_data_10'):
            try:
                with open(os.path.join(directory_path, file), 'rb') as f:
                    datas = pickle.load(f)
                    for game in datas:
                        for turn in game:
                            action = turn["action"]
                            game_state = turn ["game_state"]
                            explain_by_critic_tree = ExplainByCriticTree(game_state)
                            best_ppo = explain_by_critic_tree.build_and_explore_tree(game_state, 5)
        
                            # explain_by_critic_tree.print_tree(explain_by_critic_tree.root)
                            probs = explain_by_critic_tree.sum_probabilities_by_card_id(explain_by_critic_tree.root)
                            filtered_keys = [key for key in probs if 0 <= key <= 89]
                            
                            # print('filtered_keys: ', filtered_keys)
                            if filtered_keys:
                                # K = 3  # Set K to your desired number
                                # max_action = max(filtered_keys, key=probs.get)
                                top_k1_actions = heapq.nlargest(1, filtered_keys, key=probs.get)
                                top_k2_actions = heapq.nlargest(2, filtered_keys, key=probs.get)
                                top_k3_actions = heapq.nlargest(3, filtered_keys, key=probs.get)
                                
                                card_id = turn["card_id"]
                                # print('card_id: ', turn["card_id"], 'top_k_actions: ', top_k_actions)
                                if card_id in top_k3_actions:
                                    success_count_k3 += 1
                                    if card_id in top_k2_actions:
                                        success_count_k2 += 1
                                        if card_id in top_k1_actions:
                                            success_count_k1 += 1
                                total_length += 1
                            else:
                                pass
                                # print("No keys in the range [15, 29] found.")
                           
            except Exception as e:
                print(f"Error loading pickle file {file}: {e}")

    if total_length > 0:
        print(f"Success rate for k3: {success_count_k3}/{total_length} ({success_count_k3/total_length*100:.2f}%)")
        print(f"Success rate for k2: {success_count_k2}/{total_length} ({success_count_k2/total_length*100:.2f}%)")
        print(f"Success rate for k1: {success_count_k1}/{total_length} ({success_count_k1/total_length*100:.2f}%)")
        
    else:
        print("No data to calculate success rate.")

if __name__ == "__main__":
    directory_path = "ex/data" 
    read_and_print_pickle(directory_path)

